# Plugin to list every redirect for Cloudflare Bulk Redirects
#
# redirects.json and redirects.csv at the site root list every page using
# `redirect:` front matter (the stubs in redirects/), and send /<page>.html to
# /<page> for each page the "/:title" permalink serves at /<page> (GitHub
# Pages serves the same file at both, and can't redirect /<page>.html itself:
# it is the page). They are in the formats Cloudflare Bulk Redirects take: the
# JSON is the body of the API's list-items calls, and the CSV is the
# dashboard's import format. Both always use the production hostname from
# `url`, without any preview baseurl. Bulk Redirects match paths exactly, so
# each redirect is listed under every path GitHub Pages serves it at.
#
# The first entry records the revision the list was built from: /revision
# redirects (302) to the commit on GitHub, and in the JSON its comment is
# `git describe` for that commit (v0.0-<commits since v0.0>-g<hash>). The
# redirects sync Worker (github.com/wafer-space/cloudflare-redirects-sync)
# uses it to tell which list is newer, so a late or cached copy never
# replaces a newer one. It needs the v0.0 tag and full history: check out
# with fetch-depth 0. Production builds fail without it; other builds leave
# the entry out with a warning.

require 'csv'
require 'json'
require 'open3'
require 'uri'

module RedirectList
  SKIP = %w[index.html 404.html].freeze
  REVISION_PATH = '/revision'
  COMMIT_URL = 'https://github.com/wafer-space/wafer-space.github.io/commit/'

  module_function

  # Output paths relative to the site root (not URLs, which the "/:title"
  # permalink strips of ".html")
  def output_path(site, item)
    item.destination(site.dest).delete_prefix(File.join(site.dest, ''))
  end

  # Pages written to <page>.html and served at "/<page>": the "<page>" of each
  def canonical_pages(site)
    site.pages.filter_map do |page|
      next if page.is_a?(Jekyll::PageWithoutAFile) || !File.file?(site.in_source_dir(page.relative_path))
      next if page.data['redirect'] || page.data['layout'] == 'none'
      # jekyll-paginate-v2 later writes these as <page>/index.html (the news
      # index is served at /news/)
      next if page.data.dig('pagination', 'enabled')

      path = output_path(site, page)
      next if SKIP.include?(path) || !path.end_with?('.html')

      name = path.delete_suffix('.html')
      name if page.url == "/#{name}"
    end
  end

  # The paths GitHub Pages serves a written file at
  def source_paths(site, item)
    path = "/#{output_path(site, item)}"
    if path.end_with?('/index.html')
      dir = path.delete_suffix('index.html')
      [dir, dir.chomp('/'), path]
    elsif path.end_with?('.html')
      [path, path.delete_suffix('.html')]
    else
      [path]
    end
  end

  # Redirect targets carry the build's baseurl by now; the lists are for
  # production, so strip it and make root-relative targets absolute
  def absolute_target(target, base, origin)
    if !base.empty? && (target == base || target.start_with?("#{base}/", "#{base}#"))
      target = target.delete_prefix(base)
      target = "/#{target}" unless target.start_with?('/')
    end
    target.start_with?('/') && !target.start_with?('//') ? "#{origin}#{target}" : target
  end

  def entry(host, path, target)
    entry = { 'source_url' => "#{host}#{path}", 'target_url' => target, 'status_code' => 301 }
    # Preserving the query string replaces the target's own, so only do it
    # for targets without one (checked as a string: URI() rejects some real
    # targets, such as Matrix links with a second "#")
    entry['preserve_query_string'] = true unless target.split('#', 2).first.include?('?')
    entry
  end

  def entries(site)
    origin = site.config['url'].to_s.chomp('/')
    host = URI(origin).host
    base = BaseurlLinks.baseurl(site)

    # The page itself is the only thing at /<page>.html, so that one comes
    # from the page, not from a redirect page
    items = canonical_pages(site).map { |name| entry(host, "/#{name}.html", "#{origin}/#{name}") }
    items += (site.pages + site.documents).flat_map do |item|
      target = item.data['redirect']
      next [] unless target.is_a?(String)

      target = absolute_target(target, base, origin)
      source_paths(site, item).filter_map do |path|
        entry(host, path, target) unless "#{origin}#{path}" == target # would redirect to itself
      end
    end
    items = items.uniq { |item| item['source_url'] }.sort_by { |item| item['source_url'] }
    taken = items.find { |item| item['source_url'] == "#{host}#{REVISION_PATH}" }
    raise Jekyll::Errors::FatalException, "#{REVISION_PATH} is reserved for the redirect list's revision" if taken

    items
  end

  # git describe and the full hash of the commit being built, or nil
  def revision(site)
    describe, status = Open3.capture2('git', 'describe', '--tags', '--long', '--match', 'v[0-9]*', 'HEAD',
                                      chdir: site.source)
    return nil unless status.success?

    commit, status = Open3.capture2('git', 'rev-parse', 'HEAD', chdir: site.source)
    return nil unless status.success?

    { 'describe' => describe.strip, 'commit' => commit.strip }
  rescue SystemCallError
    nil
  end

  def revision_item(site, revision)
    host = URI(site.config['url'].to_s).host
    {
      'comment' => revision['describe'],
      'redirect' => {
        'source_url' => "#{host}#{REVISION_PATH}",
        'target_url' => "#{COMMIT_URL}#{revision['commit']}",
        'status_code' => 302
      }
    }
  end

  def json(entries, revision_item)
    items = entries.map { |entry| { 'redirect' => entry } }
    items.unshift(revision_item) if revision_item
    JSON.pretty_generate(items) + "\n"
  end

  # No header row; columns are source, target, status, preserve query string
  def csv(entries, revision_item)
    CSV.generate do |rows|
      rows << revision_item['redirect'].values_at('source_url', 'target_url', 'status_code') + ['FALSE'] if revision_item
      entries.each do |entry|
        rows << [entry['source_url'], entry['target_url'], entry['status_code'],
                 entry['preserve_query_string'] ? 'TRUE' : 'FALSE']
      end
    end
  end
end

# Hook to write the redirect lists once the rest of the site is in place
Jekyll::Hooks.register :site, :post_write do |site|
  entries = RedirectList.entries(site)
  revision = RedirectList.revision(site)
  if revision.nil?
    message = 'git describe failed: the redirect list needs the v0.0 tag and full history (fetch-depth: 0)'
    raise Jekyll::Errors::FatalException, message if Jekyll.env == 'production'

    Jekyll.logger.warn 'Redirects:', "#{message}; leaving out its revision"
  end
  revision_item = revision && RedirectList.revision_item(site, revision)
  File.write(File.join(site.dest, 'redirects.json'), RedirectList.json(entries, revision_item))
  File.write(File.join(site.dest, 'redirects.csv'), RedirectList.csv(entries, revision_item))
  Jekyll.logger.info 'Redirects:', "wrote #{entries.size} redirect list entries" \
                                   "#{" at #{revision['describe']}" if revision}"
end

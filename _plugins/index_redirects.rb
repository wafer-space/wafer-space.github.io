# Plugin to keep the old "/page.html" URLs working for pages kept as
# "page/index.html"
#
# A page whose source is <dir>/index.html (or .md) and whose URL is "/<dir>/"
# gets a generated <dir>.html that uses the redirect layout to send visitors
# to "/<dir>/", so links and bookmarks to the old flat URL still land on it.
#
# The target keeps its trailing slash on purpose: GitHub Pages serves "/<dir>"
# from <dir>.html when that file exists, so redirecting to "/<dir>" would load
# the redirect page again, forever.
#
# Pages without such a source file (redirect stubs, archives, later pages of
# the paginated news index) are skipped, and so is any <dir>.html the site
# already outputs, such as a hand-written stub with a different target.
#
# Every page using `redirect:` front matter (these generated pages and the
# stubs in redirects/) is also listed in redirects.json and redirects.csv at
# the site root, in the formats Cloudflare Bulk Redirects take: the JSON is
# the body of the API's list-items calls, and the CSV is the dashboard's
# import format. Both always use the production hostname from `url`, without
# any preview baseurl. Bulk Redirects match paths exactly, so each redirect is
# listed under both the URL it is served at and the URL GitHub Pages also
# serves it at ("/x.html" and "/x", or "/x/" and "/x").

require 'csv'
require 'json'
require 'uri'

module IndexRedirects
  SOURCE = %r{\A([^/]+(?:/[^/]+)*)/index\.(?:html|md)\z}

  module_function

  # Output paths relative to the site root (not URLs, which the "/:title"
  # permalink can strip of ".html")
  def output_path(site, item)
    item.destination(site.dest).delete_prefix(File.join(site.dest, ''))
  end

  def outputs(site)
    (site.pages + site.static_files).map { |item| output_path(site, item) }
  end

  # Only pages read from a real source file: generated pages such as tag and
  # category archives also report a ".../index.html" relative_path
  def candidates(site)
    site.pages.filter_map do |page|
      next if page.is_a?(Jekyll::PageWithoutAFile) || !File.file?(site.in_source_dir(page.relative_path))

      match = SOURCE.match(page.relative_path)
      dir = match && match[1]
      dir if dir && page.url == "/#{dir}/"
    end
  end

  # The paths GitHub Pages serves a written file at. Taken from the output
  # path, not page.url: the site's "/:title" permalink drops ".html" from the
  # generated pages' URLs, and stubs in redirects/ use ".../index.html"
  # permalinks
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

  def entries(site)
    origin = site.config['url'].to_s.chomp('/')
    host = URI(origin).host
    base = BaseurlLinks.baseurl(site)

    items = (site.pages + site.documents).flat_map do |item|
      target = item.data['redirect']
      next [] unless target.is_a?(String)

      target = absolute_target(target, base, origin)
      source_paths(site, item).filter_map do |path|
        next if "#{origin}#{path}" == target # would redirect to itself

        entry = { 'source_url' => "#{host}#{path}", 'target_url' => target, 'status_code' => 301 }
        # Preserving the query string replaces the target's own, so only do it
        # for targets without one (checked as a string: URI() rejects some real
        # targets, such as Matrix links with a second "#")
        entry['preserve_query_string'] = true unless target.split('#', 2).first.include?('?')
        entry
      end
    end
    items.uniq { |entry| entry['source_url'] }.sort_by { |entry| entry['source_url'] }
  end

  def json(entries)
    JSON.pretty_generate(entries.map { |entry| { 'redirect' => entry } }) + "\n"
  end

  # No header row; columns are source, target, status, preserve query string
  def csv(entries)
    CSV.generate do |rows|
      entries.each do |entry|
        rows << [entry['source_url'], entry['target_url'], entry['status_code'],
                 entry['preserve_query_string'] ? 'TRUE' : 'FALSE']
      end
    end
  end
end

class IndexRedirectGenerator < Jekyll::Generator
  safe true
  priority :lowest

  def generate(site)
    base = BaseurlLinks.baseurl(site)
    taken = IndexRedirects.outputs(site)

    IndexRedirects.candidates(site).each do |dir|
      next if taken.include?("#{dir}.html")

      page = Jekyll::PageWithoutAFile.new(site, site.source, File.dirname(dir), "#{File.basename(dir)}.html")
      page.data['layout'] = 'redirect'
      # The baseurl_links post_read hook has already run, so prefix here
      page.data['redirect'] = BaseurlLinks.prefix("/#{dir}/", base)
      page.data['sitemap'] = false
      site.pages << page
    end
  end
end

# Hook to write the redirect lists once the rest of the site is in place
Jekyll::Hooks.register :site, :post_write do |site|
  entries = IndexRedirects.entries(site)
  File.write(File.join(site.dest, 'redirects.json'), IndexRedirects.json(entries))
  File.write(File.join(site.dest, 'redirects.csv'), IndexRedirects.csv(entries))
  Jekyll.logger.info 'Redirects:', "wrote #{entries.size} redirect list entries"
end

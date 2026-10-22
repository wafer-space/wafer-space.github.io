# Plugin to send "/page/" and "/page/index.html" to "/page", and to list
# every redirect for Cloudflare Bulk Redirects
#
# The site's "/:title" permalink writes about.html, which GitHub Pages serves
# at /about: that is the page's canonical URL. GitHub Pages also serves the
# same file at /about.html, and /about/ would 404, so for every such page:
#
# - a <page>/index.html using the redirect layout is generated, sending
#   /about/ and /about/index.html to /about (GitHub Pages serves /about from
#   about.html before it looks at the directory, so this can't loop);
# - /about.html, /about/ and /about/index.html are listed in redirects.json
#   and redirects.csv, so Cloudflare can answer all three with a real 301.
#   GitHub Pages can't redirect /about.html itself: it is the page.
#
# Only pages read from a real source file count (not archives, redirect pages
# or paginated pages such as the news index), and a <page>/index.html the site
# already outputs is left alone.
#
# redirects.json and redirects.csv at the site root also list every other page
# using `redirect:` front matter (the stubs in redirects/), in the formats
# Cloudflare Bulk Redirects take: the JSON is the body of the API's list-items
# calls, and the CSV is the dashboard's import format. Both always use the
# production hostname from `url`, without any preview baseurl. Bulk Redirects
# match paths exactly, so each redirect is listed under every path GitHub
# Pages serves it at.

require 'csv'
require 'json'
require 'uri'

module IndexRedirects
  SKIP = %w[index.html 404.html].freeze

  module_function

  # Output paths relative to the site root (not URLs, which the "/:title"
  # permalink strips of ".html")
  def output_path(site, item)
    item.destination(site.dest).delete_prefix(File.join(site.dest, ''))
  end

  def outputs(site)
    (site.pages + site.static_files).map { |item| output_path(site, item) }
  end

  # Pages written to <page>.html and served at "/<page>": the "<page>" of each
  def canonical_pages(site)
    site.pages.filter_map do |page|
      next if page.is_a?(Jekyll::PageWithoutAFile) || !File.file?(site.in_source_dir(page.relative_path))
      next if page.data['redirect'] || page.data['layout'] == 'none'
      # jekyll-paginate-v2 later writes these as <page>/index.html (the news
      # index is served at /news/), so a stub there would collide with it
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
    items.uniq { |item| item['source_url'] }.sort_by { |item| item['source_url'] }
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

    IndexRedirects.canonical_pages(site).each do |name|
      next if taken.include?("#{name}/index.html")

      page = Jekyll::PageWithoutAFile.new(site, site.source, name, 'index.html')
      page.data['permalink'] = "/#{name}/index.html"
      page.data['layout'] = 'redirect'
      # The baseurl_links post_read hook has already run, so prefix here
      page.data['redirect'] = BaseurlLinks.prefix("/#{name}", base)
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

# Plugin to send "/page/" and "/page/index.html" to "/page"
#
# The site's "/:title" permalink writes about.html, which GitHub Pages serves
# at /about: that is the page's canonical URL. GitHub Pages also serves the
# same file at /about.html, and /about/ would 404, so for every such page a
# <page>/index.html using the redirect layout is generated, sending /about/
# and /about/index.html to /about (GitHub Pages serves /about from about.html
# before it looks at the directory, so this can't loop). redirect_list.rb
# then lists those generated redirects, with /about.html, for Cloudflare.
#
# Only pages read from a real source file count (not archives, redirect pages
# or paginated pages such as the news index), and a <page>/index.html the site
# already outputs is left alone.

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

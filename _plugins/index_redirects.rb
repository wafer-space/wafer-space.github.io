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

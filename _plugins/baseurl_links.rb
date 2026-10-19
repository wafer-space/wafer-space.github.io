# Plugin to make root-relative links honour site.baseurl
#
# Markdown links such as [Discord](/discord), and HTML written as href="/x"
# without relative_url, are emitted verbatim, so they only work when the site
# is served from the domain root. The per-PR preview builds use
# --baseurl /pr-NNN, where those links escape the preview directory and 404.
# Front matter `redirect:` targets used by the redirect layout have the same
# problem.
#
# The hooks run on every build so production exercises the same code as the
# previews; with an empty baseurl every root-relative URL counts as already
# prefixed, so the output is unchanged.

module BaseurlLinks
  URL_ATTRIBUTE = /(\s(?:href|src|poster)\s*=\s*)(["'])(.*?)\2/i
  SRCSET_ATTRIBUTE = /(\ssrcset\s*=\s*)(["'])(.*?)\2/im

  module_function

  def baseurl(site)
    site.config['baseurl'].to_s.chomp('/')
  end

  # Root-relative URLs ("/foo") get the baseurl; protocol-relative ("//host"),
  # relative, absolute and already-prefixed URLs are left alone.
  def prefix(url, base)
    return url unless url.start_with?('/') && !url.start_with?('//')
    return url if url == base || url.start_with?("#{base}/", "#{base}?", "#{base}#")

    "#{base}#{url}"
  end

  def rewrite_html(html, base)
    html = html.gsub(URL_ATTRIBUTE) do
      attribute, quote, url = Regexp.last_match.captures
      "#{attribute}#{quote}#{prefix(url, base)}#{quote}"
    end
    html.gsub(SRCSET_ATTRIBUTE) do
      # Capture before the nested sub below replaces Regexp.last_match
      attribute, quote, srcset = Regexp.last_match.captures
      # -1 keeps trailing empty candidates so the attribute round-trips exactly
      candidates = srcset.split(',', -1).map do |candidate|
        candidate.sub(/\A(\s*)(\S+)/) { "#{Regexp.last_match(1)}#{prefix(Regexp.last_match(2), base)}" }
      end
      "#{attribute}#{quote}#{candidates.join(',')}#{quote}"
    end
  end
end

# Hook to prefix redirect targets before any layout renders them
Jekyll::Hooks.register :site, :post_read do |site|
  base = BaseurlLinks.baseurl(site)
  (site.pages + site.documents).each do |item|
    target = item.data['redirect']
    item.data['redirect'] = BaseurlLinks.prefix(target, base) if target.is_a?(String)
  end
end

# Hook to prefix links in converted content, before it is placed in layouts;
# jekyll-feed and anything else reading `content` only see this version
Jekyll::Hooks.register [:pages, :documents], :post_convert do |item|
  base = BaseurlLinks.baseurl(item.site)
  next if item.output_ext != '.html'

  item.content = BaseurlLinks.rewrite_html(item.content, base)
end

# Hook to prefix links in the fully rendered HTML, covering layouts, includes
# and HTML in front matter (URLs already built with relative_url, or prefixed
# by the hook above, carry the baseurl and are left alone)
Jekyll::Hooks.register [:pages, :documents], :post_render do |item|
  base = BaseurlLinks.baseurl(item.site)
  next if item.output_ext != '.html' || item.output.nil?

  item.output = BaseurlLinks.rewrite_html(item.output, base)
end

# Plugin to make root-relative links honour site.baseurl
#
# Markdown links such as [Discord](/discord) are emitted verbatim by kramdown,
# so they only work when the site is served from the domain root. The per-PR
# preview builds use --baseurl /pr-NNN, where those links escape the preview
# directory and 404. Front matter `redirect:` targets used by the redirect
# layout have the same problem.
#
# With an empty baseurl (production) nothing is changed.

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
      candidates = srcset.split(',').map do |candidate|
        candidate.sub(/\A(\s*)(\S+)/) { "#{Regexp.last_match(1)}#{prefix(Regexp.last_match(2), base)}" }
      end
      "#{attribute}#{quote}#{candidates.join(',')}#{quote}"
    end
  end
end

# Hook to prefix redirect targets before any layout renders them
Jekyll::Hooks.register :site, :post_read do |site|
  base = BaseurlLinks.baseurl(site)
  next if base.empty?

  (site.pages + site.documents).each do |item|
    target = item.data['redirect']
    item.data['redirect'] = BaseurlLinks.prefix(target, base) if target.is_a?(String)
  end
end

# Hook to prefix links in converted Markdown, before it is placed in layouts
# (theme layouts and includes already use relative_url)
Jekyll::Hooks.register [:pages, :documents], :post_convert do |item|
  base = BaseurlLinks.baseurl(item.site)
  next if base.empty?
  next unless item.site.config['markdown_ext'].split(',').include?(item.extname.delete_prefix('.'))

  item.content = BaseurlLinks.rewrite_html(item.content, base)
end

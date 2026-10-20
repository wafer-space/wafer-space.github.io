# Plugin to give headings a hover-revealed "#" permalink
#
# Every heading in a rendered HTML page or document gets an id (its own, or
# one made from its text) and the same "#" link the theme's
# components/heading-anchor.html include renders, so the theme's
# .heading-anchor CSS styles both alike.
#
# Listing pages are skipped: any page whose layout is named in the
# `heading_anchors_skip_layouts` config list (the news index and its later
# pages, tag and category archives, author pages), where the headings are
# post-card titles and repeated "Read More"s. Front matter
# `heading_anchors: false` turns the plugin off for one page, and
# `heading_anchors: true` turns it on for a page with a skipped layout.
#
# A heading is left alone when:
# - it already has a "#" link (theme partials that use the include);
# - it is footer/sidebar chrome (class "widget-title");
# - it has a data-no-anchor attribute;
# - its text has no word of two or more letters (countdown digits, "450+" or
#   "22k" statistics);
# - it is a subtitle: one level below an anchored heading, with only tags in
#   between (a section's display-3 tagline, a team card's role); the heading
#   above it carries the link.
#
# A heading without an id links to an existing element whose id matches its
# slug (e.g. a section wrapper div) rather than duplicating that id; otherwise
# it gets the slug, with -2, -3, ... appended when the id is already taken.
# Give a heading an explicit id where its text alone is ambiguous, such as the
# "Early Bird" heading repeated in every pricing slot.

require 'cgi'
require 'set'

module HeadingAnchors
  HEADING = /<h([1-6])(\s[^>]*)?>(.*?)<\/h\1\s*>/im
  ID_ATTRIBUTE = /\sid\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))/i
  CLASS_ATTRIBUTE = /\sclass\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))/i
  # Comments and scripts are copied through untouched
  SKIPPED_BLOCK = /(<!--.*?-->|<script\b.*?<\/script\b[^>]*>)/im

  module_function

  def attribute(attrs, pattern)
    match = attrs.to_s.match(pattern)
    match && match.captures.compact.first
  end

  # Plain text of a fragment, used only for slugs and emptiness checks: the
  # runs of text between tags, so no "<" survives (an unclosed tag swallows
  # the rest of the fragment). Angle brackets decoded from entities are
  # dropped too. Named entities CGI does not know (&nbsp;, &mdash;, &sup2;,
  # ...) become spaces, which slugify treats as word breaks.
  def text_of(html)
    text = CGI.unescapeHTML(html.split(/<[^>]*>?/).join)
    text.gsub(/[<>]/, '').gsub(/&[a-z][a-z0-9]*;/i, ' ').strip
  end

  def enabled?(item)
    return false unless item.output_ext == '.html' && item.output
    return item.data['heading_anchors'] unless item.data['heading_anchors'].nil?

    !Array(item.site.config['heading_anchors_skip_layouts']).include?(item.data['layout'])
  end

  def anchor_link(id)
    %(<a class="heading-anchor" href="##{id}" aria-label="Permalink to this heading" title="Copy link to this heading">#</a>)
  end

  def skip?(attrs, inner, text)
    inner.include?('class="heading-anchor"') ||
      attribute(attrs, CLASS_ATTRIBUTE).to_s.split.include?('widget-title') ||
      attrs.to_s.match?(/\sdata-no-anchor\b/i) ||
      !text.match?(/\p{L}{2}/)
  end

  def ids_in(html)
    html.scan(ID_ATTRIBUTE).map { |captures| captures.compact.first }
  end

  def add_anchors(html)
    # Blank out comments and scripts (keeping offsets) so headings inside them
    # are ignored and they count as empty space between headings
    masked = html.gsub(SKIPPED_BLOCK) { |block| ' ' * block.length }
    headings = masked.to_enum(:scan, HEADING).map { Regexp.last_match }
    page_ids = ids_in(masked).to_set
    # Ids on non-heading elements, such as section wrapper divs, that a
    # heading may link to instead of duplicating
    wrapper_ids = page_ids - headings.flat_map { |match| ids_in(match[0][/\A<[^>]*>/]) }
    linked_ids = Set.new

    output = +''
    position = 0
    previous = nil
    headings.each_with_index do |match, index|
      level, attrs, inner = match.captures
      subtitle = previous && previous[:anchored] && level.to_i == previous[:level] + 1 &&
                 text_of(masked[previous[:end]...match.begin(0)]).empty?
      text = text_of(inner)
      previous = { level: level.to_i, end: match.end(0), anchored: inner.include?('class="heading-anchor"') }
      next if subtitle || skip?(attrs, inner, text)

      previous[:anchored] = true

      id = attribute(attrs, ID_ATTRIBUTE)
      if id.nil?
        slug = Jekyll::Utils.slugify(text)
        if wrapper_ids.include?(slug) && !linked_ids.include?(slug)
          id = slug
        else
          id = slug
          suffix = 1
          id = "#{slug}-#{suffix += 1}" while page_ids.include?(id)
          attrs = %( id="#{id}"#{attrs})
          page_ids << id
        end
      end
      linked_ids << id
      output << html[position...match.begin(0)]
      # The link goes after the last content, not after trailing whitespace,
      # which would render as a gap before the "#"
      content = html[match.begin(3)...match.end(3)]
      trailing = content[/\s*\z/]
      output << "<h#{level}#{attrs}>#{content.rstrip}#{anchor_link(id)}#{trailing}</h#{level}>"
      position = match.end(0)
    end
    output << html[position..]
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_render do |item|
  next unless HeadingAnchors.enabled?(item)

  item.output = HeadingAnchors.add_anchors(item.output)
end

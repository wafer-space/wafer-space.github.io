# Plugin to inject git commit hash into site generation
Jekyll::Hooks.register :site, :after_init do |site|
  begin
    # Get the current git commit hash
    commit_hash = `git rev-parse HEAD`.strip
    
    # Add commit hash to site data for use in templates
    site.data['git'] ||= {}
    site.data['git']['commit_hash'] = commit_hash
    site.data['git']['short_hash'] = commit_hash[0..7] if commit_hash.length >= 8
    
    # Also add to site config for global access
    site.config['git_commit_hash'] = commit_hash
    site.config['git_short_hash'] = commit_hash[0..7] if commit_hash.length >= 8
    
    Jekyll.logger.info "Git commit hash loaded: #{commit_hash[0..7]}"
  rescue StandardError => e
    Jekyll.logger.warn "Warning: Could not load git commit hash: #{e.message}"
    # Set fallback values
    site.data['git'] ||= {}
    site.data['git']['commit_hash'] = 'unknown'
    site.data['git']['short_hash'] = 'unknown'
    site.config['git_commit_hash'] = 'unknown'
    site.config['git_short_hash'] = 'unknown'
  end
end

# Hook to add commit hash meta tag to HTML pages  
Jekyll::Hooks.register :site, :post_render do |site|
  # Process both pages and documents (posts, collections, etc.)
  (site.pages + site.documents).each do |doc|
    if doc.output_ext == '.html'
      commit_hash = site.config['git_commit_hash'] || 'unknown'
      
      # Add meta tag if not already present
      unless doc.output.nil? || doc.output.include?('name="git-commit"')
        meta_tag = %Q(  <meta name="git-commit" content="#{commit_hash}">)
        
        # Try to insert after the first meta tag in head
        if doc.output && doc.output.match(/<meta[^>]*>/i)
          doc.output = doc.output.sub(/(<meta[^>]*>)/i) do |match|
            "#{match}\n#{meta_tag}"
          end
        # Fallback: insert after <head> tag when no meta tags are present
        elsif doc.output && doc.output.match(/<head[^>]*>/i)
          doc.output = doc.output.sub(/(<head[^>]*>)/i) do |match|
            "#{match}\n#{meta_tag}"
          end
        end
      end
    end
  end
end

# Helper method to add commit hash comment to HTML output
def add_commit_hash_comment(output, site)
  commit_hash = site.config['git_commit_hash'] || 'unknown'
  short_hash = site.config['git_short_hash'] || 'unknown'
  
  # Add HTML comment with commit info
  comment = %Q(<!-- Generated from git commit: #{commit_hash} (#{short_hash}) -->)
  
  # Add comment at the end of the document, before closing </html> tag
  unless output.include?('Generated from git commit:')
    if output.match(/<\/html>/i)
      output = output.sub(/<\/html>/i, "#{comment}\n</html>")
    else
      # Fallback if no closing html tag found
      output = "#{output}\n#{comment}"
    end
  end
  output
end

# Unified hook to add commit hash comment to HTML documents and pages
Jekyll::Hooks.register [:documents, :pages], :post_render do |item|
  if item.output_ext == '.html'
    item.output = add_commit_hash_comment(item.output, item.site)
  end
end
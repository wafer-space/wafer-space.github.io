# Plugin to support theme in submodule
Jekyll::Hooks.register :site, :after_init do |site|
  theme_path = site.config['theme_path'] || '_theme'
  
  # Add theme includes directory (with lower priority than local includes)
  theme_includes = File.join(site.source, theme_path, '_includes')
  if Dir.exist?(theme_includes)
    site.includes_load_paths.push(theme_includes)
  end
  
  # Add theme assets to sass paths
  theme_sass = File.join(site.source, theme_path, 'assets')
  if Dir.exist?(theme_sass)
    site.config['sass'] ||= {}
    site.config['sass']['load_paths'] ||= []
    site.config['sass']['load_paths'] << theme_sass
  end
  
end

# Hook to load layouts from theme directory and add theme demo pages
Jekyll::Hooks.register :site, :post_read do |site|
  theme_path = site.config['theme_path'] || '_theme'
  theme_layouts_dir = File.join(site.source, theme_path, '_layouts')
  
  # Load theme layouts
  if Dir.exist?(theme_layouts_dir)
    Dir.glob(File.join(theme_layouts_dir, '**', '*.html')).each do |layout_file|
      # Get relative path from layouts directory
      relative_path = Pathname.new(layout_file).relative_path_from(Pathname.new(theme_layouts_dir))
      layout_name = relative_path.to_s.sub(/\.html$/, '')
      
      # Only add if layout doesn't already exist
      unless site.layouts.key?(layout_name)
        site.layouts[layout_name] = Jekyll::Layout.new(site, theme_layouts_dir, relative_path.to_s)
      end
    end
  end
  
  # Load theme collections
  theme_collections_dir = File.join(site.source, theme_path)
  
  if Dir.exist?(theme_collections_dir)
    # Find all collection directories in theme (start with _)
    Dir.glob(File.join(theme_collections_dir, '_*')).each do |collection_dir|
      next unless File.directory?(collection_dir)
      
      collection_name = File.basename(collection_dir)[1..-1] # Remove leading _
      
      # Skip if collection already exists in main site
      main_collection_path = File.join(site.source, File.basename(collection_dir))
      next if File.exist?(main_collection_path)
      
      # Check if collection is configured in Jekyll
      if site.config['collections'] && site.config['collections'][collection_name]
        # Load collection items from theme
        collection = site.collections[collection_name]
        
        # Find all files in theme collection directory
        Dir.glob(File.join(collection_dir, '**', '*')).each do |item_file|
          next unless File.file?(item_file)
          
          # Get relative path from collection directory
          relative_path = Pathname.new(item_file).relative_path_from(Pathname.new(collection_dir))
          
          # Create document and add to collection
          doc = Jekyll::Document.new(item_file, { :site => site, :collection => collection })
          collection.docs << doc
        end
      end
    end
  end
  
  # Add theme demo pages to site pages collection
  # This is needed to match the original site output exactly
  theme_pages_dir = File.join(site.source, theme_path)
  
  if Dir.exist?(theme_pages_dir)
    # Find all HTML files in theme that should be pages (excluding _layouts, _includes, etc.)
    Dir.glob(File.join(theme_pages_dir, '**', '*.html')).each do |page_file|
      # Skip internal directories
      relative_to_theme = Pathname.new(page_file).relative_path_from(Pathname.new(theme_pages_dir))
      next if relative_to_theme.to_s.start_with?('_')
      
      # Create a Jekyll Page for each theme demo page
      page_dir = File.dirname(relative_to_theme)
      page_name = File.basename(relative_to_theme)
      
      # Skip if page already exists in main site
      main_page_path = File.join(site.source, relative_to_theme)
      next if File.exist?(main_page_path)
      
      # Create Jekyll Page and add to site
      theme_page = Jekyll::Page.new(site, theme_pages_dir, page_dir == '.' ? '' : page_dir, page_name)
      site.pages << theme_page
    end
  end
end

# Hook to copy theme demo content and assets after site generation
Jekyll::Hooks.register :site, :post_write do |site|
  theme_path = site.config['theme_path'] || '_theme'
  theme_source = File.join(site.source, theme_path)
  
  require 'fileutils'
  
  # Copy theme assets
  theme_assets_source = File.join(theme_source, 'assets')
  theme_assets_dest = File.join(site.dest, 'assets')
  
  if Dir.exist?(theme_assets_source)
    # Copy theme assets to destination, preserving directory structure
    Dir.glob(File.join(theme_assets_source, '**', '*')).each do |source_file|
      if File.file?(source_file)
        relative_path = Pathname.new(source_file).relative_path_from(Pathname.new(theme_assets_source))
        dest_file = File.join(theme_assets_dest, relative_path)
        
        # Only copy if destination doesn't exist (site assets take precedence)
        unless File.exist?(dest_file)
          FileUtils.mkdir_p(File.dirname(dest_file))
          FileUtils.cp(source_file, dest_file)
        end
      end
    end
  end
  
  # Note: Auto-copy functionality disabled to maintain identical output
  
  # Copy theme configuration files (only if site doesn't have them)
  %w[cloudflare.toml netlify.toml github.toml].each do |config_file|
    theme_config = File.join(theme_source, config_file)
    site_config = File.join(site.dest, config_file)
    main_config = File.join(site.source, config_file)
    
    # Copy from theme if file exists in theme and not in main site
    if File.exist?(theme_config) && !File.exist?(main_config)
      FileUtils.cp(theme_config, site_config)
    end
  end
  
  # Remove _theme from build output
  theme_dest = File.join(site.dest, '_theme')
  if Dir.exist?(theme_dest)
    FileUtils.rm_rf(theme_dest)
  end
end
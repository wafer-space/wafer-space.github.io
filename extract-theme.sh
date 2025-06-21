#!/bin/bash

# Create a temporary directory for theme extraction
THEME_DIR="../wafer-space-jekyll-theme"
TEMP_DIR="../wafer-space-jekyll-theme-temp"

# Remove existing directories if they exist
rm -rf "$THEME_DIR" "$TEMP_DIR"

# Clone the repository
git clone . "$TEMP_DIR"

# Move to the temp directory and switch branch
cd "$TEMP_DIR"
git checkout new-website

# Remove all non-theme files and directories
# Keep only theme-related files
find . -maxdepth 1 -type f -not -name ".git*" -not -name "Gemfile*" -not -name "_config.yml" -delete
find . -maxdepth 1 -type d -not -name "." -not -name ".git" -not -name "_includes" -not -name "_layouts" -not -name "assets" -not -name "_portfolio" -not -name "_data" -exec rm -rf {} +

# Remove site-specific content from assets
cd assets
find . -maxdepth 1 -not -name "." -not -name "css" -not -name "js" -not -name "revolution" -not -name "type" -not -name "images" -exec rm -rf {} +
cd images
find . -maxdepth 1 -not -name "." -not -name "art" -not -name "blob" -not -name "concept" -not -name "icon" -exec rm -rf {} +
cd ../..

# Remove site-specific data files
cd _data
find . -not -name "navigation.yml" -not -name "one_page_nav.yml" -not -name "." -delete
cd ..

# Create theme gemspec
cat > jekyll-theme-wafer-space.gemspec << 'EOF'
# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "jekyll-theme-wafer-space"
  spec.version       = "0.1.0"
  spec.authors       = ["Wafer Space"]
  spec.email         = ["info@wafer.space"]

  spec.summary       = "A professional Jekyll theme for business websites"
  spec.homepage      = "https://github.com/wafer-space/jekyll-theme-wafer-space"
  spec.license       = "MIT"

  spec.files         = `git ls-files -z`.split("\x0").select { |f| f.match(%r!^(assets|_layouts|_includes|_data|LICENSE|README)!i) }

  spec.add_runtime_dependency "jekyll", ">= 3.9", "< 5.0"
  spec.add_runtime_dependency "jekyll-paginate-v2", "~> 3.0"
  spec.add_runtime_dependency "jekyll-archives", "~> 2.2"
  spec.add_runtime_dependency "jekyll-feed", "~> 0.12"

  spec.add_development_dependency "bundler"
end
EOF

# Create theme README
cat > README.md << 'EOF'
# Jekyll Theme Wafer Space

A professional Jekyll theme for business websites with multiple layout options.

## Installation

Add this line to your Jekyll site's `Gemfile`:

```ruby
gem "jekyll-theme-wafer-space"
```

And add this line to your Jekyll site's `_config.yml`:

```yaml
theme: jekyll-theme-wafer-space
```

And then execute:

    $ bundle

## Usage

### Layouts

The theme provides various layouts:
- Multiple blog layouts (blog-1 through blog-8)
- Portfolio layouts (grid, masonry, mosaic, fullscreen)
- Shop layouts
- Team layouts
- Contact layouts

### Includes

The theme includes various components:
- Navigation (multiple styles)
- Footer variations
- Portfolio displays
- Team carousels
- Contact forms
- Social media links

## Contributing

Bug reports and pull requests are welcome on GitHub.

## License

The theme is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
EOF

# Update Gemfile for theme
cat > Gemfile << 'EOF'
source "https://rubygems.org"
gemspec
EOF

# Create LICENSE file if it doesn't exist
if [ ! -f LICENSE ]; then
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 Wafer Space

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
fi

# Commit the changes
git add -A
git commit -m "Extract Jekyll theme from wafer-space.github.io

This commit extracts the theme components from the main website repository
to create a standalone Jekyll theme that can be used as a git submodule.

The theme includes:
- All layouts (_layouts/)
- All includes (_includes/)  
- Theme assets (css, js, fonts, theme images)
- Navigation data files
- Portfolio collection structure

Site-specific content has been removed."

# Move to final directory
cd ..
mv "$TEMP_DIR" "$THEME_DIR"

echo "Theme extracted successfully to $THEME_DIR"
echo "The theme repository preserves the full git history of theme files"
# Wafer Space

The official website for Wafer Space - democratizing silicon design and manufacturing.

## About

Wafer Space is on a mission to make custom silicon accessible to everyone. This repository contains the source code for our website at [wafer.space](https://wafer.space).

## Building the Site

This is a Jekyll-based website that uses a proprietary theme stored as a git submodule.

### Prerequisites

- Ruby (with Bundler)
- Jekyll
- Git (with submodule support)

### Quick Start

```bash
# Clone the repository with submodules
git clone --recursive https://github.com/wafer-space/wafer-space.github.io.git
cd wafer-space.github.io

# Install dependencies
make install

# Build the site
make build

# Serve locally (http://localhost:4000)
make serve
```

### Available Make Commands

- `make help` - Show all available commands
- `make build` - Build the Jekyll site
- `make serve` - Serve the site locally with auto-regeneration
- `make dev` - Alias for 'serve'
- `make production` - Build site in production mode
- `make clean` - Remove generated files and caches
- `make install` - Install Ruby dependencies
- `make update` - Update Ruby dependencies
- `make test` - Build site and run tests

### Manual Build (without Make)

```bash
# Set up Ruby path
export PATH=$PATH:/home/tim/.local/share/gem/ruby/3.2.0/bin

# Install dependencies
bundle install

# Build the site
bundle exec jekyll build

# Serve locally
bundle exec jekyll serve
```

## Theme

The website uses a proprietary Jekyll theme that is included as a git submodule in the `_theme` directory. The theme is not open source and is licensed separately.

### Theme Updates

To update the theme submodule to the latest version:

```bash
git submodule update --remote _theme
git add _theme
git commit -m "Update theme to latest version"
```

## Site Structure

- `_advisors/` - Advisor profiles
- `_authors/` - Author information
- `_friends/` - Partner organizations
- `_posts/` - Blog posts and news
- `_data/` - Site configuration and navigation
- `_includes/` - Site-specific overrides for theme components
- `_plugins/` - Custom Jekyll plugins (includes theme loader)
- `assets/` - Site-specific assets (images, etc.)

## Deployment

The site is automatically deployed via GitHub Pages when changes are pushed to the main branch.

### GitHub Actions Setup

Since the theme is stored as a private git submodule, GitHub Actions requires special configuration to access it during builds. See [`.github/SUBMODULE_SETUP.md`](.github/SUBMODULE_SETUP.md) for detailed setup instructions.

**Quick setup:**
1. Create a Personal Access Token with `repo` permissions
2. Add it as a repository secret named `SUBMODULE_TOKEN`
3. The workflow will automatically use it to access the private theme repository

## Contributing

For site content updates, please submit a pull request. For theme-related issues, please contact the Wafer Space team as the theme is proprietary.

## License

The website content (excluding the theme) is copyright Wafer Space. The Jekyll theme in `_theme/` is proprietary and not licensed for redistribution.
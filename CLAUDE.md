# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

First-time setup for Claude Code:
```bash
cp .claude/settings.local.json.template .claude/settings.local.json
```

The `settings.local.json` file is gitignored to prevent rebase conflicts and allow personalized configurations.

## Development Commands

### CRITICAL: Working Directory Verification

**ALWAYS verify your current working directory before running any commands.** This repository has a complex architecture with theme submodules and various working directories. Always check `pwd` and ensure you're in the expected location:

- **Main repository root**: `./` (top-level directory with _config.yml)
- **Theme submodule**: `./_theme/` (contains Jekyll theme files)
- **Temporary directories**: `./_tmp` (relative to repository root)

Common mistakes:
- Running Jekyll commands from wrong directory
- Editing theme files when not in `_theme/` directory
- Git operations in wrong repository context

### Environment Setup
Set Ruby path before running any Jekyll commands:
```bash
export PATH=$PATH:~/.local/share/gem/ruby/3.2.0/bin
```

### Essential Commands
- `make build` - Build the Jekyll site
- `make serve` - Serve site locally with auto-regeneration at http://localhost:4000
- `make dev` - Alias for serve (development mode)
- `make production` - Build for production with JEKYLL_ENV=production
- `make clean` - Remove generated files and caches
- `make install` - Install Ruby dependencies via bundle install
- `make test` - Build and run basic validation (checks for 17 HTML files)
- `make verify` - Run comprehensive output verification script

### Manual Commands (if Make unavailable)
```bash
bundle install
bundle exec jekyll serve --watch --incremental
bundle exec jekyll build
```

## Architecture Overview

This is a Jekyll-based website for Wafer Space with a **unique submodule theme architecture**:

### Core Architecture
- **Main Repository**: Contains site-specific content (posts, collections, overrides)
- **Theme Submodule**: Proprietary Jekyll theme in `_theme/` directory
- **Custom Plugin**: `_plugins/theme_plugin.rb` bridges Jekyll with the submodule theme

### Theme Integration System
The `theme_plugin.rb` file implements a sophisticated system to load theme components:

1. **Layouts Loading**: Dynamically loads layouts from `_theme/_layouts/` via Jekyll::Layout.new
2. **Includes Path**: Adds `_theme/_includes/` to Jekyll's include search paths
3. **Collections Merging**: Loads theme collections (like shop_items, portfolio) when not overridden
4. **Demo Pages**: Demo pages are excluded from production site
5. **Asset Copying**: Copies theme assets to build output with site assets taking precedence
6. **Override System**: Site files always override theme files when both exist

### Collections Architecture
- `_advisors/` - Advisor profiles (site-specific)
- `_authors/` - Author information (site-specific)
- `_friends/` - Partner organizations (site-specific)
- `_posts/` - Blog posts and news (site-specific)
- `_shop_items/` - E-commerce products (loaded from theme if not overridden)
- `_portfolio/` - Portfolio items (loaded from theme if not overridden)

### Override Hierarchy
1. **Site files** (main repo) take highest precedence
2. **Theme files** (`_theme/`) are fallback defaults
3. **Navigation override**: Custom `_includes/layouts/nav/_btn-header.html` changes button text from "Free Trial" to "Free Silicon?"

### Build Output Validation
The site generates **17 HTML files** for the production wafer.space website. The test system verifies:
- Correct file count (17 HTML files)
- Theme plugin presence
- Theme submodule availability

### Configuration Files
- `_config.yml` - Main Jekyll configuration with `theme_path: "_theme"`
- `Gemfile` - Ruby dependencies including jekyll-paginate-v2, jekyll-archives
- `Makefile` - Build automation and development commands

### GitHub Actions Deployment
- Deploys from `main` branch via GitHub Pages
- Uses SSH deploy key (`JEKYLL_THEME_KEY` secret) for private theme repository access
- Requires SSH key setup: public key as deploy key on theme repo, private key as repository secret
- Submodule checkout via SSH: `git@github.com:wafer-space/wafer-space-jekyll-theme.git`

### Private Submodule Setup
The theme is proprietary and stored as a private git submodule. For development:
```bash
git clone --recursive https://github.com/wafer-space/wafer-space.github.io.git
```

### File Precedence Rules
- Site assets in `assets/` override theme assets
- Site includes in `_includes/` override theme includes
- Site layouts override theme layouts (though none currently exist)
- Site collections override theme collections entirely
- Site pages override theme demo pages

### Critical Plugin Hooks
1. `after_init` - Sets up include paths and sass paths
2. `post_read` - Loads theme layouts, collections, and demo pages
3. `post_write` - Copies theme assets and removes `_theme` from output

This architecture allows the main repository to focus on Wafer Space content while leveraging a full-featured proprietary theme for design and functionality.

## PR Preview Verification

### Critical: Verification Errors are Real

**NEVER assume verification failures are "timing issues" or "deployment lag".** The preview site verification (`verify-preview` workflow) runs comprehensive checks including muffet link validation. If muffet reports 404 errors or broken links, they are **real bugs** that need to be fixed.

Common causes of verification failures:
1. **Absolute paths without baseurl**: Using `/assets/...` instead of `{{ site.baseurl }}/assets/...` or relative paths
2. **Missing images**: Images referenced but not committed/pushed
3. **Broken internal links**: Links to pages that don't exist
4. **External link issues**: External URLs that return errors (may need exclusion rules if legitimate)

### Asset and Link Path Requirements

For the preview site (served at `/pr-{number}/`), all asset and link paths must be relative or use Jekyll's `{{ site.baseurl }}` variable:

```markdown
<!-- WRONG - will 404 on preview site -->
![Image](/assets/images/example.png)

<!-- CORRECT - works on both preview and production -->
![Image]({{ site.baseurl }}/assets/images/example.png)

<!-- Also correct for posts - relative to site root -->
![Image](../assets/images/example.png)
```

In Markdown files, prefer using the `{{ site.baseurl }}` approach or proper relative paths to ensure compatibility with PR preview deployments.

## Git Workflow

Make sure you are on the right branch before doing any work.

### Working Practices

- When making changes, start a new git branch and then make sure to commit to the git repository frequently as you work.
- Once the work has been completed, create a new pull request on GitHub.
- Once the pull request has been created, wait for the GitHub Action checks to run and fix any issues they find.
- Wait for GitHub Copilot to review your pull request and then use the GitHub GraphQL API to find all code suggestions, fix the issues and then resolve the threads.


# Makefile for Jekyll site
# wafer-space.github.io

# Variables
JEKYLL := bundle exec jekyll
BUNDLE := bundle
SITE_DIR := _site
PATH := ${PATH}:/home/tim/.local/share/gem/ruby/3.2.0/bin

# Default target
.DEFAULT_GOAL := help

# Phony targets
.PHONY: help build serve clean install update verify dev production test

# Help target - shows available commands
help:
	@echo "Available commands:"
	@echo "  make build       - Build the Jekyll site"
	@echo "  make serve       - Build and serve the site locally (default: http://localhost:4000)"
	@echo "  make dev         - Alias for 'serve' - development mode with auto-regeneration"
	@echo "  make production  - Build site in production mode (with JEKYLL_ENV=production)"
	@echo "  make clean       - Remove generated site and caches"
	@echo "  make install     - Install Ruby dependencies"
	@echo "  make update      - Update Ruby dependencies"
	@echo "  make verify      - Run verification script to check site output"
	@echo "  make test        - Build site and run basic tests"

# Build the Jekyll site
build:
	@echo "Building Jekyll site..."
	@$(JEKYLL) build
	@echo "✅ Site built successfully to $(SITE_DIR)/"

# Serve the site locally with auto-regeneration
serve:
	@echo "Starting Jekyll server..."
	@echo "Site will be available at http://localhost:4000"
	@echo "Press Ctrl+C to stop"
	@$(JEKYLL) serve --watch --incremental

# Alias for serve - development mode
dev: serve

# Build for production
production:
	@echo "Building Jekyll site for production..."
	@JEKYLL_ENV=production $(JEKYLL) build
	@echo "✅ Production site built successfully to $(SITE_DIR)/"

# Clean generated files and caches
clean:
	@echo "Cleaning generated files..."
	@rm -rf $(SITE_DIR)
	@rm -rf .jekyll-cache
	@rm -rf .sass-cache
	@rm -rf _site_reference _site_refactored_verify
	@echo "✅ Clean complete"

# Install dependencies
install:
	@echo "Installing Ruby dependencies..."
	@$(BUNDLE) install
	@echo "✅ Dependencies installed"

# Update dependencies
update:
	@echo "Updating Ruby dependencies..."
	@$(BUNDLE) update
	@echo "✅ Dependencies updated"

# Run verification script if it exists
verify:
	@if [ -f verify_identical_output.sh ]; then \
		echo "Running verification script..."; \
		./verify_identical_output.sh; \
	else \
		echo "❌ Verification script not found"; \
		exit 1; \
	fi

# Basic tests
test: build
	@echo "Running basic tests..."
	@echo -n "Checking HTML file count: "
	@HTML_COUNT=$$(find $(SITE_DIR) -name "*.html" | wc -l); \
	if [ $$HTML_COUNT -eq 17 ]; then \
		echo "✅ $$HTML_COUNT HTML files (expected: 17)"; \
	else \
		echo "❌ $$HTML_COUNT HTML files (expected: 17)"; \
		exit 1; \
	fi
	@echo -n "Checking theme plugin: "
	@if [ -f _plugins/theme_plugin.rb ]; then \
		echo "✅ Found"; \
	else \
		echo "❌ Not found"; \
		exit 1; \
	fi
	@echo -n "Checking theme submodule: "
	@if [ -d _theme ]; then \
		echo "✅ Found"; \
	else \
		echo "❌ Not found"; \
		exit 1; \
	fi
	@echo "✅ All tests passed"

# Quick build and serve (builds first, then serves)
quick: build serve
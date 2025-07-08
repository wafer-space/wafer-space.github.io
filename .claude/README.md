# Claude Code Configuration

This directory contains configuration files for Claude Code (claude.ai/code).

## Setup

To set up Claude Code for this repository:

1. Copy the template file:
   ```bash
   cp .claude/settings.local.json.template .claude/settings.local.json
   ```

2. The `settings.local.json` file is gitignored and won't be committed, so you can customize it for your local environment.

## Files

- `settings.local.json.template` - Template with common permissions for this repository
- `settings.local.json` - Your local settings (gitignored, not committed)

## Note

The `settings.local.json` file is intentionally gitignored to prevent conflicts during rebases and to allow each developer to have their own local Claude Code configuration.
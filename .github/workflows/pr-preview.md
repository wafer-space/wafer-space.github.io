# PR Preview Deployment

Automatic preview deployments for pull requests using GitHub Pages with custom domain.

## Features

- **Live preview URLs** - `https://preview.wafer.space/pr-123/`
- **Automatic updates** - Rebuilds on every commit
- **Preview index** - All active previews at `https://preview.wafer.space/`
- **Deployment tracking** - GitHub deployment status integration
- **Automatic cleanup** - Removed when PR closes

## How It Works

When you open a pull request:
1. Jekyll site is built automatically
2. Deployed to custom domain at `/pr-[number]/`
3. PR is commented with preview URL
4. Updates on new commits
5. Cleaned up when PR closes

## Viewing Previews

Click the preview URL in the PR comment:
```
https://preview.wafer.space/pr-123/
```

Browse all active previews:
```
https://preview.wafer.space/
```

## Troubleshooting

### Preview not appearing
- Check GitHub Actions tab for workflow status
- Ensure custom domain DNS is configured for `preview.wafer.space`
- Wait up to 2 minutes for GitHub Pages deployment to complete
- Verify SSH deploy key is configured for theme submodule access

### Preview shows 404 error
- Check if Jekyll build completed successfully in workflow logs
- Verify PR base URL configuration in workflow
- Ensure theme submodule initialized correctly

### Preview index missing PRs
- Check script validation warnings in workflow logs
- Ensure preview directories contain `index.html` file
- Verify PR numbers are numeric format only

### Deployment failures
- Check for merge conflicts in gh-pages branch
- Verify GitHub Pages is enabled for repository
- Ensure workflow has required permissions (contents, pages, deployments)
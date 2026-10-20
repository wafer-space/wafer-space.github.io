# PR Preview Deployment

Automatic preview deployments for pull requests using GitHub Pages with custom domain.

## Features

- **Live preview URLs** - `https://preview.wafer.space/pr-123/`
- **Automatic updates** - Rebuilds on every commit
- **Preview index** - All active previews at `https://preview.wafer.space/`
- **Deployment tracking** - GitHub deployment status integration
- **Automatic cleanup** - Removed when PR closes

## How It Works

Previews are built in two stages so that pull requests from forks get previews too, without giving fork code access to secrets:

1. **Stage 1, `pr-preview-build.yml` (`pull_request`, untrusted):** runs on every PR, including forks, with no secrets. It produces nothing Stage 2 uses. Finishing is what triggers Stage 2, and it warns early if a fork PR changes executable code.
2. **Stage 2, `pr-preview-deploy.yml` (`workflow_run`, trusted):** runs from `main` with the secrets once Stage 1 finishes. It finds the PR using only the event's head repository, branch and SHA, checked against the GitHub API, and then:
   - blocks fork PRs that change `_plugins/` or `.github/`, and comments to explain why;
   - takes every script and template it runs from a separate checkout of `main`, never from the PR;
   - for other fork PRs, replaces `_plugins/`, `Gemfile` and `.gitmodules` with the copies from `main`, removes `.bundle/` and any `Gemfile.lock` (it is gitignored, so `main` has none), and pins `plugins_dir`, `source` and `destination`;
   - builds with the private theme, deploys to `/pr-[number]/`, comments the preview URL and starts the link check.
3. **Verification, `preview-verification.yml` (`workflow_dispatch`):** started by Stage 2 with the PR number, preview URL and commit, and comments the link check results. It can also be run by hand from the Actions tab.
4. Previews update on every push and are removed by `cleanup-previews.yml` when the PR closes.

GitHub runs Stage 2 from `main` because it's a `workflow_run` workflow, and Stage 2 starts the verification on `main` too. So changes to either in a PR only take effect after merging, and their runs appear in the Actions tab rather than in the PR's checks.

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
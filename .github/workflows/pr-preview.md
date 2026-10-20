# PR Preview Deployment

Automatic preview deployments for pull requests using GitHub Pages with custom domain.

## Features

- **Live preview URLs** - `https://preview.wafer.space/pr-123/`
- **Automatic updates** - Rebuilds on every commit
- **Preview index** - All active previews at `https://preview.wafer.space/`
- **Deployment tracking** - GitHub deployment status integration
- **Automatic cleanup** - Removed when PR closes

## How It Works

Previews are built in two stages so that pull requests from forks get previews too, without the PR's code ever running next to a secret. Every step is an action from [wafer-space/github-actions](https://github.com/wafer-space/github-actions/tree/main/pr-preview), pinned to a commit, so a PR here can't change what the privileged jobs run.

1. **Stage 1, `pr-preview-build.yml` (`pull_request`, untrusted):** runs on every PR, including forks, with no secrets. It produces nothing Stage 2 uses. Finishing is what triggers Stage 2, and it warns early if a fork PR changes executable code.
2. **Stage 2, `pr-preview-deploy.yml` (`workflow_run`, trusted):** runs from `main` once Stage 1 finishes, as separate jobs:
   - **find-pr** finds the PR using only the event's head repository, branch and SHA, checked against the GitHub API. It blocks fork PRs that change `_plugins/` or `.github/` (the **blocked** job comments to explain why), and works out the preview directory and the theme commit the PR's `_theme` points at.
   - **fetch-theme** checks out the private theme with `JEKYLL_THEME_KEY` and uploads it as an artifact. It runs no PR code.
   - **build** checks out the PR, adds the theme and builds the site, uploading it as an artifact. It is the only job that runs the PR's content, and it has **no secrets** and a read-only token. For fork PRs it first puts back `main`'s `_plugins/` and `Gemfile`, removes `.bundle/` and any `Gemfile.lock`, and pins `plugins_dir`, `source` and `destination`.
   - **deploy** downloads the built site and pushes it to `/pr-[number]/` in the preview repository with `PREVIEW_KEY`, treating it purely as data. It then comments the preview URL and starts the link check.
3. **Verification, `preview-verification.yml` (`workflow_dispatch`):** started by Stage 2 with the PR number, preview URL and commit, and comments the link check results. It can also be run by hand from the Actions tab. The link check's excluded URLs are listed in this workflow.
4. Previews update on every push and are removed by `cleanup-previews.yml` when the PR closes.

No job caches gems: jobs in a `workflow_run` workflow share `main`'s Actions cache, so the build job could otherwise poison it, and the production build in `jekyll.yml` installs gems fresh for the same reason.

GitHub runs Stage 2 from `main` because it's a `workflow_run` workflow, and Stage 2 starts the verification on `main` too. So changes to either in a PR only take effect after merging, and their runs appear in the Actions tab rather than in the PR's checks. To change what the steps do, change the actions in wafer-space/github-actions, then update the commit they're pinned to here.

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
- Verify the `JEKYLL_THEME_KEY` deploy key can read the theme repository (the fetch-theme job)

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
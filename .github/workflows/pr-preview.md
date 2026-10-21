# PR Preview Deployment

Automatic preview deployments for pull requests using GitHub Pages with custom domain.

## Features

- **Live preview URLs** - `https://preview.wafer.space/pr-123/`
- **Automatic updates** - Rebuilds on every commit
- **Preview index** - All active previews at `https://preview.wafer.space/`
- **Automatic cleanup** - Removed when PR closes
- **Checks on the PR** - the `PR preview` and `PR preview / link check` commit statuses

## How It Works

Previews are built in two stages so that pull requests from forks get previews too, without the PR's code ever running next to a secret. Every step is an action from [wafer-space/actions](https://github.com/wafer-space/actions/tree/main/pr-preview), pinned to a commit, so a PR here can't change what the privileged jobs run.

1. **Stage 1, `pr-preview-build.yml` (`pull_request`, untrusted):** runs on every PR, including forks, with no secrets and no permissions. It does nothing itself: finishing is what triggers Stage 2.
2. **Stage 2, `pr-preview-deploy.yml` (`workflow_run`, trusted):** runs from `main` once Stage 1 finishes, as separate jobs:
   - **find-pr** finds the PR using only the event's head repository, branch and SHA, checked against the GitHub API, and works out the preview directory and the theme commit the PR's `_theme` points at.
   - **fetch-theme** checks out the private theme at that commit with `JEKYLL_THEME_KEY` and uploads it as an artifact. It runs no PR code. The commit can be in the PR author's own fork of the theme: GitHub serves every commit in a fork network from the theme repository.
   - **build** checks out the PR, adds the theme and builds the site, uploading it as an artifact. It is the only job that runs the PR's code (content, plugins and Gemfile alike), and it has **no secrets** and a read-only token, so fork PRs are built like any other.
   - **deploy** downloads the built site and pushes it to `/pr-[number]/` in the preview repository with `PREVIEW_KEY`, treating it purely as data, unless the PR has moved on to a newer commit. It waits until the preview serves that commit, then comments and sets the `PR preview` status, and starts the link check. If the build failed, it reports that instead.
3. **Verification, `preview-verification.yml` (`workflow_dispatch`):** started by Stage 2 with the PR number, preview URL and commit. It comments the link check results and sets the `PR preview / link check` status. It can also be run by hand from the Actions tab. The link check's excluded URLs are listed in this workflow.
4. Previews update on every push and are removed by `cleanup-previews.yml` when the PR closes.

**Never add an Actions cache to this repository's workflows.** Jobs in a `workflow_run` workflow share `main`'s cache, so a PR's build could write a poisoned one. That's why neither the preview build nor the production build in `jekyll.yml` caches gems.

GitHub runs Stage 2 from `main` because it's a `workflow_run` workflow, and Stage 2 starts the verification on `main` too. So changes to either in a PR only take effect after merging, and their runs appear in the Actions tab; their results reach the PR as the two commit statuses. To change what the steps do, change the actions in wafer-space/actions, then update the commit they're pinned to here.

## Copies of this repository

The theme and `wafer-space/preview.wafer.space` are only used for PRs to wafer-space/wafer-space.github.io. A copy of this repository in your own account (e.g. to test changes to these workflows) builds previews of its own PRs only if you set it up:

- Fork the theme to `<you>/wafer-space-jekyll-theme`, or set the `THEME_REPOSITORY` variable, and add a read-only deploy key on it whose private key is the copy's `JEKYLL_THEME_KEY` secret.
- Fork `wafer-space/preview.wafer.space`, delete its `CNAME` and turn on Pages. Set the `PREVIEW_REPOSITORY` variable to it and `PREVIEW_BASE_URL` to where Pages serves it, e.g. `https://<you>.github.io/preview.wafer.space`. Add a deploy key with write access on it whose private key is the copy's `PREVIEW_KEY` secret.

Without the variables, the copy's preview and cleanup workflows do nothing. Never give a copy a key to the wafer-space theme.

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
- Check the `PR preview` status on the PR, and the PR Preview Deploy run in the Actions tab
- Ensure custom domain DNS is configured for `preview.wafer.space`
- Verify the `JEKYLL_THEME_KEY` deploy key can read the theme repository (the fetch-theme job)

### Preview shows 404 error
- Check if Jekyll build completed successfully in workflow logs
- Ensure the PR's `_theme` points at a commit in the theme repository or a fork of it

### Preview index missing PRs
- Ensure preview directories are named `pr-<number>` and contain an `index.html` file

# GitHub Scripts

- `verify-preview-site.sh`: Runs the preview checks by hand (see `.github/docs/preview-verification.md`)

The PR preview workflows (`pr-preview-build.yml`, `pr-preview-deploy.yml`, `preview-verification.yml` and `cleanup-previews.yml`) run actions from [wafer-space/actions](https://github.com/wafer-space/actions/tree/main/pr-preview), pinned to a commit. Their scripts and templates live there, so the privileged preview jobs never run code from the pull request being previewed. See `.github/workflows/pr-preview.md`.

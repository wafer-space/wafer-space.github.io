# GitHub Actions Setup for Private Theme Submodule

This document explains how to configure GitHub Actions to access the private theme submodule during the build process.

## Problem

By default, GitHub Actions' `GITHUB_TOKEN` cannot access private repositories, including private git submodules. This causes the build to fail when trying to clone the private theme repository.

## Solution

We use a Personal Access Token (PAT) with appropriate permissions to access the private theme repository.

## Setup Instructions

### Step 1: Create a Personal Access Token

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token" > "Generate new token (classic)"
3. Give it a descriptive name like "Wafer Space Theme Access"
4. Set an appropriate expiration date
5. Select the following scopes:
   - `repo` (Full control of private repositories)
   - `read:org` (if the theme repo is in an organization)

### Step 2: Add Token as Repository Secret

1. Go to your repository: `wafer-space/wafer-space.github.io`
2. Navigate to **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Name: `SUBMODULE_TOKEN`
5. Value: Paste the PAT you created in Step 1
6. Click **Add secret**

### Step 3: Verify the Setup

1. Push a commit to the `new-website` branch
2. Go to the **Actions** tab in your repository
3. Watch the build process - it should now successfully clone the private theme submodule
4. Look for the log message: "Using SUBMODULE_TOKEN for private repository access"

## Troubleshooting

### Build Still Fails with "Repository not found"

- Ensure the PAT has `repo` scope
- Verify the token hasn't expired
- Check that the PAT owner has access to the private theme repository

### Token Not Being Used

- Verify the secret is named exactly `SUBMODULE_TOKEN`
- Check that the secret is set at the repository level, not environment level

### Alternative: Organization-Level Token

If the theme repository is in an organization:

1. Create a machine user account
2. Add the machine user to the organization with appropriate permissions
3. Create a PAT for the machine user
4. Use that PAT as the `SUBMODULE_TOKEN`

## Security Considerations

- **Least Privilege**: Only grant the minimum necessary permissions
- **Expiration**: Set a reasonable expiration date and rotate tokens regularly
- **Monitoring**: Regularly audit token usage and access logs
- **Scope**: The token only needs `repo` access, not admin permissions

## How It Works

The workflow does the following:

1. Checks out the main repository with `submodules: recursive`
2. Configures Git to use the PAT for GitHub URLs
3. Updates and initializes all submodules
4. Builds the Jekyll site with the theme available

## Manual Testing

To test locally with the same setup:

```bash
# Set your PAT as an environment variable
export GITHUB_TOKEN="your_pat_here"

# Clone with submodules
git clone --recursive https://github.com/wafer-space/wafer-space.github.io.git

# Or if already cloned, update submodules
git submodule update --init --recursive
```
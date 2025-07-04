// Create GitHub deployment for PR preview
// This module exports a function that can be safely called by actions/github-script

module.exports = async function createDeployment(github, context, core) {
  // Validate inputs
  if (!context.payload.pull_request) {
    throw new Error('No pull request data available');
  }
  
  const prNumber = context.payload.pull_request.number;
  if (!Number.isInteger(prNumber) || prNumber < 1 || prNumber > 99999) {
    throw new Error('Invalid PR number');
  }

  // Sanitize PR title to prevent code injection
  const rawTitle = context.payload.pull_request.title || '';
  const prTitle = rawTitle.replace(/[^\w\s-_.]/g, '').substring(0, 100);
  
  // Validate ref format
  const ref = context.payload.pull_request.head.ref;
  if (!ref || ref.length > 255) {
    throw new Error('Invalid ref format');
  }

  const deployment = await github.rest.repos.createDeployment({
    owner: context.repo.owner,
    repo: context.repo.repo,
    ref: ref,
    environment: `pr-preview-${prNumber}`,
    transient_environment: true,
    production_environment: false,
    required_contexts: [],
    description: `PR #${prNumber}: ${prTitle}`,
    auto_merge: false
  });

  await github.rest.repos.createDeploymentStatus({
    owner: context.repo.owner,
    repo: context.repo.repo,
    deployment_id: deployment.data.id,
    state: 'in_progress',
    description: 'Building preview...'
  });

  core.setOutput('deployment_id', deployment.data.id);
  console.log(`Created deployment ${deployment.data.id} for PR #${prNumber}`);
};
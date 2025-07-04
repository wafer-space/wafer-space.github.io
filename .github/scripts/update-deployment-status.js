// Update GitHub deployment status for PR preview
// This module exports a function that can be safely called by actions/github-script

module.exports = async function updateDeploymentStatus(github, context, core) {
  const deploymentId = process.env.DEPLOYMENT_ID;
  const jobStatus = process.env.JOB_STATUS;
  
  // Validate inputs
  if (!deploymentId) {
    throw new Error('DEPLOYMENT_ID environment variable is required');
  }
  
  if (!deploymentId.match(/^\d+$/)) {
    throw new Error('Invalid deployment ID format');
  }
  
  if (!context.payload.pull_request) {
    throw new Error('No pull request data available');
  }
  
  const prNumber = context.payload.pull_request.number;
  if (!Number.isInteger(prNumber) || prNumber < 1 || prNumber > 99999) {
    throw new Error('Invalid PR number');
  }

  const validStates = ['success', 'failure'];
  const state = jobStatus === 'success' ? 'success' : 'failure';
  
  if (!validStates.includes(state)) {
    throw new Error(`Invalid deployment state: ${state}`);
  }

  const previewUrl = `https://preview.wafer.space/pr-${prNumber}/`;

  await github.rest.repos.createDeploymentStatus({
    owner: context.repo.owner,
    repo: context.repo.repo,
    deployment_id: deploymentId,
    state: state,
    environment_url: previewUrl,
    description: state === 'success' ? 'Preview deployed to custom domain' : 'Preview deployment failed'
  });

  console.log(`Updated deployment ${deploymentId} status to: ${state}`);
};
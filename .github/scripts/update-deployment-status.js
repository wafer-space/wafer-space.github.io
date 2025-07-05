// Update GitHub deployment status for PR preview
// This module exports a function that can be safely called by actions/github-script

module.exports = async function updateDeploymentStatus(github, context, core) {
  const deploymentId = process.env.DEPLOYMENT_ID;
  const jobStatus = process.env.JOB_STATUS;
  const verificationStatus = process.env.VERIFICATION_STATUS;
  
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

  // Determine deployment state based on job status and verification results
  let state, description;
  
  if (jobStatus === 'failure') {
    state = 'failure';
    description = 'Preview deployment failed';
  } else if (verificationStatus === 'success') {
    state = 'success';
    description = 'Preview deployed and verified';
  } else if (verificationStatus === 'partial') {
    state = 'success'; // GitHub deployment API doesn't have 'partial' state
    description = 'Preview deployed but verification incomplete';
  } else if (verificationStatus === 'failed') {
    state = 'failure';
    description = 'Preview deployment verification failed';
  } else {
    // Fallback to old behavior if verification status not available
    state = jobStatus === 'success' ? 'success' : 'failure';
    description = state === 'success' ? 'Preview deployed to custom domain' : 'Preview deployment failed';
  }

  const validStates = ['success', 'failure', 'error', 'pending'];
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
    description: description
  });

  console.log(`Updated deployment ${deploymentId} status to: ${state} (${description})`);
};
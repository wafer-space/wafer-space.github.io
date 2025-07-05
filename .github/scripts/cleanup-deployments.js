// Mark GitHub deployments as inactive when PR is closed
// This module exports a function that can be safely called by actions/github-script

module.exports = async function cleanupDeployments(github, context, core) {
  // Validate inputs
  if (!context.payload.pull_request) {
    throw new Error('No pull request data available');
  }
  
  const prNumber = context.payload.pull_request.number;
  if (!Number.isInteger(prNumber) || prNumber < 1 || prNumber > 99999) {
    throw new Error('Invalid PR number');
  }
  
  const environment = `pr-preview-${prNumber}`;

  // Get all deployments for this PR environment
  const { data: deployments } = await github.rest.repos.listDeployments({
    owner: context.repo.owner,
    repo: context.repo.repo,
    environment: environment,
  });

  console.log(`Found ${deployments.length} deployments for environment: ${environment}`);

  // Mark each deployment as inactive
  for (const deployment of deployments) {
    // Validate deployment ID
    if (!deployment.id || !Number.isInteger(deployment.id)) {
      console.log(`Skipping invalid deployment ID: ${deployment.id}`);
      continue;
    }
    
    await github.rest.repos.createDeploymentStatus({
      owner: context.repo.owner,
      repo: context.repo.repo,
      deployment_id: deployment.id,
      state: 'inactive',
      description: 'PR closed - preview removed'
    });
    console.log(`Marked deployment ${deployment.id} as inactive`);
  }

  console.log(`Cleanup completed for PR #${prNumber}`);
};
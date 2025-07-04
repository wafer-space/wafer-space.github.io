// Comment on PR when preview is cleaned up
// This module exports a function that can be safely called by actions/github-script

module.exports = async function commentPrCleanup(github, context, core) {
  // Validate inputs
  if (!context.payload.pull_request) {
    throw new Error('No pull request data available');
  }
  
  const prNumber = context.payload.pull_request.number;
  if (!Number.isInteger(prNumber) || prNumber < 1 || prNumber > 99999) {
    throw new Error('Invalid PR number');
  }

  // Read comment template with path validation
  const fs = require('fs');
  const path = require('path');
  const templatePath = '.github/templates/pr-cleanup-template.md';
  
  // Validate template path to prevent directory traversal
  const resolvedPath = path.resolve(templatePath);
  if (!resolvedPath.includes('.github/templates/pr-cleanup-template.md')) {
    throw new Error('Invalid template path');
  }
  
  if (!fs.existsSync(templatePath)) {
    throw new Error(`Template file ${templatePath} not found`);
  }

  const commentBody = fs.readFileSync(templatePath, 'utf8');

  await github.rest.issues.createComment({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: prNumber,
    body: commentBody
  });

  console.log(`Posted cleanup comment on PR #${prNumber}`);
};
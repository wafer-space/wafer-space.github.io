// Comment on PR with preview deployment information
// This module exports a function that can be safely called by actions/github-script

module.exports = async function commentPrPreview(github, context, core) {
  // Validate inputs
  if (!context.payload.pull_request) {
    throw new Error('No pull request data available');
  }
  
  const prNumber = context.payload.pull_request.number;
  if (!Number.isInteger(prNumber) || prNumber < 1 || prNumber > 99999) {
    throw new Error('Invalid PR number');
  }
  
  const rawCommitSha = context.payload.pull_request.head.sha;
  if (!rawCommitSha || !rawCommitSha.match(/^[a-f0-9]{40}$/)) {
    throw new Error('Invalid commit SHA format');
  }
  
  const previewUrl = `https://preview.wafer.space/pr-${prNumber}/`;
  const commitSha = rawCommitSha.substring(0, 7);

  // Read comment template with path validation
  const fs = require('fs');
  const path = require('path');
  const templatePath = '.github/templates/pr-comment-template.md';
  
  // Validate template path to prevent directory traversal
  const resolvedPath = path.resolve(templatePath);
  if (!resolvedPath.includes('.github/templates/pr-comment-template.md')) {
    throw new Error('Invalid template path');
  }
  
  if (!fs.existsSync(templatePath)) {
    throw new Error(`Template file ${templatePath} not found`);
  }

  let commentBody = fs.readFileSync(templatePath, 'utf8');

  // Sanitize and replace placeholders in template
  const sanitizedPreviewUrl = previewUrl.replace(/[<>&"']/g, (match) => {
    const entityMap = { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#x27;' };
    return entityMap[match];
  });
  
  const sanitizedCommitSha = commitSha.replace(/[<>&"']/g, (match) => {
    const entityMap = { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#x27;' };
    return entityMap[match];
  });

  commentBody = commentBody
    .replace(/\{\{PREVIEW_URL\}\}/g, sanitizedPreviewUrl)
    .replace(/\{\{COMMIT_SHA\}\}/g, sanitizedCommitSha);

  // Find existing comment
  const { data: comments } = await github.rest.issues.listComments({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: prNumber,
  });

  const botComment = comments.find(comment => 
    comment.user.type === 'Bot' && 
    (comment.body.includes('Preview Deployment Ready!') || 
     comment.body.includes('Preview Deployment Partially Ready') ||
     comment.body.includes('Preview Deployment Failed'))
  );

  if (botComment) {
    await github.rest.issues.updateComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      comment_id: botComment.id,
      body: commentBody
    });
    console.log(`Updated existing comment ${botComment.id} on PR #${prNumber}`);
  } else {
    await github.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      body: commentBody
    });
    console.log(`Created new comment on PR #${prNumber}`);
  }
};
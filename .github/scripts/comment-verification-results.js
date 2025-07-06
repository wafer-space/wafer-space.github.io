// Comment verification results with lifecycle management
// This module manages verification comment creation and archival of obsolete comments

module.exports = async function commentVerificationResults(github, context, core) {
  // Validate inputs
  if (!context.payload.pull_request) {
    throw new Error('No pull request data available');
  }
  
  const prNumber = context.payload.pull_request.number;
  if (!Number.isInteger(prNumber) || prNumber < 1 || prNumber > 99999) {
    throw new Error('Invalid PR number');
  }
  
  const verificationStatus = process.env.VERIFICATION_STATUS;
  const reportContent = process.env.REPORT_CONTENT;
  const runId = process.env.GITHUB_RUN_ID;
  
  if (!verificationStatus || !reportContent) {
    throw new Error('Missing verification status or report content');
  }
  
  // Create comment with verification results
  const statusIcon = verificationStatus === 'success' ? '✅' : '❌';
  const statusText = verificationStatus === 'success' ? 'PASSED' : 'FAILED';
  
  const newCommentBody = `## ${statusIcon} Preview Site Verification ${statusText}

${reportContent}

---
<sub>🔍 Automated verification • Run ID: ${runId} • ${new Date().toISOString()}</sub>
<!-- VERIFICATION_COMMENT_MARKER -->`;

  // Get all comments on the PR
  const { data: comments } = await github.rest.issues.listComments({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: prNumber,
  });

  // Find existing verification comments (marked with our identifier)
  const verificationComments = comments.filter(comment => 
    comment.user.type === 'Bot' && 
    comment.body.includes('<!-- VERIFICATION_COMMENT_MARKER -->')
  );

  // Archive old verification comments by updating them
  for (const oldComment of verificationComments) {
    // Skip if this is already archived
    if (oldComment.body.includes('**📋 Previous verification results (archived)**')) {
      continue;
    }
    
    // Extract the original content and archive it
    const originalContent = oldComment.body.replace('<!-- VERIFICATION_COMMENT_MARKER -->', '');
    
    const archivedCommentBody = `**📋 Previous verification results (archived)**

<details>
<summary>Click to view archived verification results</summary>

${originalContent}

</details>

---
<sub>⏰ This verification result has been archived • A newer verification is available below</sub>
<!-- VERIFICATION_COMMENT_MARKER -->`;

    try {
      await github.rest.issues.updateComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        comment_id: oldComment.id,
        body: archivedCommentBody
      });
      console.log(`Archived verification comment ${oldComment.id} on PR #${prNumber}`);
    } catch (error) {
      console.error(`Failed to archive comment ${oldComment.id}:`, error);
      // Continue processing other comments even if one fails
    }
  }

  // Create new verification comment
  try {
    const { data: newComment } = await github.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      body: newCommentBody
    });
    
    console.log(`Created new verification comment ${newComment.id} on PR #${prNumber}`);
    console.log(`Archived ${verificationComments.length} previous verification comments`);
    
    return {
      commentId: newComment.id,
      archivedCount: verificationComments.length
    };
  } catch (error) {
    console.error('Failed to create verification comment:', error);
    throw error;
  }
};
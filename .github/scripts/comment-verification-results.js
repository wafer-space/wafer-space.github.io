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

  // Function to get and filter verification comments with debugging
  const getVerificationComments = async () => {
    console.log(`Fetching comments for PR #${prNumber}...`);
    
    // Get all comments with pagination support
    const allComments = [];
    let page = 1;
    let hasMore = true;
    
    while (hasMore) {
      const { data: pageComments } = await github.rest.issues.listComments({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: prNumber,
        per_page: 100,
        page: page
      });
      
      allComments.push(...pageComments);
      hasMore = pageComments.length === 100;
      page++;
      
    }
    
    // Filter verification comments (exclude deployment ready)
    const filteredComments = allComments.filter(comment => {
      const isBot = comment.user.login === 'github-actions[bot]';
      const hasMarker = comment.body.includes('<!-- VERIFICATION_COMMENT_MARKER -->');
      const hasVerificationText = comment.body.includes('Preview Site Verification');
      const isDeployment = comment.body.includes('🚀 Preview Deployment Ready!');
      
      return isBot && (hasMarker || hasVerificationText) && !isDeployment;
    });
    return filteredComments;
  };

  // Keep archiving until only one unarchived verification comment remains
  let archivedCount = 0;
  let maxIterations = 10; // Safety limit to prevent infinite loops
  let iteration = 0;
  
  while (iteration < maxIterations) {
    iteration++;
    const verificationComments = await getVerificationComments();
    
    // Filter to only unarchived verification comments
    const unarchivedComments = verificationComments.filter(comment => 
      !comment.body.includes('**📋 Previous verification results (archived)**')
    );
    
    console.log(`Iteration ${iteration}: Found ${unarchivedComments.length} unarchived verification comments`);
    
    // If we have 1 or fewer unarchived comments, we're done
    if (unarchivedComments.length <= 1) {
      console.log(`Archive process complete: ${unarchivedComments.length} unarchived verification comments remaining`);
      break;
    }
    
    // Sort by creation date (oldest first) and archive all but the most recent
    unarchivedComments.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
    const commentsToArchive = unarchivedComments.slice(0, -1); // All except the last (most recent)
    
    console.log(`Archiving ${commentsToArchive.length} older verification comments`);
    
    // Archive the older comments
    for (const oldComment of commentsToArchive) {
      // Extract original content and determine comment type
      let originalContent = oldComment.body;
      const hasMarker = originalContent.includes('<!-- VERIFICATION_COMMENT_MARKER -->');
      if (hasMarker) {
        originalContent = originalContent.replace('<!-- VERIFICATION_COMMENT_MARKER -->', '').trim();
      }
      
      // Create archived comment with timestamp from original comment
      const createdAt = new Date(oldComment.created_at).toISOString();
      const archivedCommentBody = `**📋 Previous verification results (archived)**

<details>
<summary>Click to view archived verification results from ${createdAt}</summary>

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
        console.log(`Archived verification comment ${oldComment.id} on PR #${prNumber} (created: ${createdAt})`);
        archivedCount++;
      } catch (error) {
        console.error(`Failed to archive comment ${oldComment.id}:`, error);
        // Continue processing other comments even if one fails
      }
    }
    
    // Small delay to allow GitHub API to catch up
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  if (iteration >= maxIterations) {
    console.warn(`Reached maximum iterations (${maxIterations}) while archiving comments`);
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
    console.log(`Archived ${archivedCount} previous verification comments`);
    
    return {
      commentId: newComment.id,
      archivedCount: archivedCount
    };
  } catch (error) {
    console.error('Failed to create verification comment:', error);
    throw error;
  }
};
// Comment verification results with lifecycle management
// This module manages verification comment creation and archival of obsolete comments

// Helper function for delays
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

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
    core.info(`Fetching comments for PR #${prNumber}...`);
    
    // Get all comments with pagination support
    const allComments = [];
    let page = 1;
    
    while (true) {
      const { data: pageComments } = await github.rest.issues.listComments({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: prNumber,
        per_page: 100,
        page: page
      });
      
      allComments.push(...pageComments);
      
      // Break when we get less than a full page (more efficient)
      if (pageComments.length < 100) {
        break;
      }
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

  // Create new verification comment first
  let newCommentId;
  try {
    const { data: newComment } = await github.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      body: newCommentBody
    });
    
    newCommentId = newComment.id;
    core.info(`Created new verification comment ${newComment.id} on PR #${prNumber}`);
  } catch (error) {
    core.error(`Failed to create verification comment: ${error.message}`);
    throw error;
  }

  // Add delay to allow any concurrent workflows to create their comments first
  // This helps handle rapid-fire pushes where multiple workflows may start simultaneously
  const initialDelay = Math.floor(Math.random() * 2000) + 1000; // 1-3 second random delay
  core.info(`Waiting ${initialDelay}ms before archival to handle concurrent workflows...`);
  await sleep(initialDelay);

  // Now archive ALL existing unarchived verification comments (except the one we just created)
  let archivedCount = 0;
  let maxIterations = 15; // Increased limit for handling rapid-fire scenarios
  let iteration = 0;
  let backoffDelay = 100; // Start with 100ms for exponential backoff
  
  while (iteration < maxIterations) {
    iteration++;
    
    // Refresh comment list each iteration to catch any new comments from concurrent workflows
    const verificationComments = await getVerificationComments();
    
    // Filter to only unarchived verification comments, excluding the one we just created
    const unarchivedComments = verificationComments.filter(comment => 
      !comment.body.includes('**📋 Previous verification results (archived)**') &&
      comment.id !== newCommentId
    );
    
    core.info(`Iteration ${iteration}: Found ${unarchivedComments.length} unarchived verification comments to archive`);
    
    // Debug: Log all unarchived comment IDs and creation times
    if (unarchivedComments.length > 0) {
      core.debug('Unarchived comments details:');
      unarchivedComments.forEach(c => {
        core.debug(`  - Comment ${c.id}: created ${c.created_at}`);
      });
    }
    
    // If no unarchived comments remain (besides our new one), we're done
    if (unarchivedComments.length === 0) {
      core.info(`Archive process complete: Only 1 unarchived verification comment remaining (the new one)`);
      break;
    }
    
    core.info(`Archiving ${unarchivedComments.length} existing verification comments`);
    
    // Archive ALL existing unarchived comments
    for (const oldComment of unarchivedComments) {
      // Double-check that this comment hasn't been archived by another concurrent workflow
      try {
        const { data: currentComment } = await github.rest.issues.getComment({
          owner: context.repo.owner,
          repo: context.repo.repo,
          comment_id: oldComment.id
        });
        
        // Skip if already archived by another workflow
        if (currentComment.body.includes('**📋 Previous verification results (archived)**')) {
          core.debug(`Comment ${oldComment.id} already archived by another workflow, skipping`);
          continue;
        }
      } catch (error) {
        core.debug(`Comment ${oldComment.id} no longer exists, skipping`);
        continue;
      }
      
      // Extract original content and determine comment type
      let originalContent = oldComment.body;
      const hasMarker = originalContent.includes('<!-- VERIFICATION_COMMENT_MARKER -->');
      if (hasMarker) {
        originalContent = originalContent.replace('<!-- VERIFICATION_COMMENT_MARKER -->', '').trim();
      }
      
      // Create archived comment with timestamp from original comment
      const createdAt = new Date(oldComment.created_at).toISOString();
      const workflowInfo = `Run ID: ${runId}`;
      const archivedCommentBody = `**📋 Previous verification results (archived)**

<details>
<summary>Click to view archived verification results from ${createdAt}</summary>

${originalContent}

</details>

---
<sub>⏰ This verification result has been archived by ${workflowInfo} • A newer verification is available below</sub>
<!-- VERIFICATION_COMMENT_MARKER -->`;

      try {
        await github.rest.issues.updateComment({
          owner: context.repo.owner,
          repo: context.repo.repo,
          comment_id: oldComment.id,
          body: archivedCommentBody
        });
        core.info(`Archived verification comment ${oldComment.id} on PR #${prNumber} (created: ${createdAt})`);
        archivedCount++;
      } catch (error) {
        if (error.status === 409) {
          core.debug(`Comment ${oldComment.id} was modified by another workflow, skipping`);
        } else {
          core.error(`Failed to archive comment ${oldComment.id}: ${error.message}`);
        }
        // Continue processing other comments even if one fails
      }
    }
    
    // Exponential backoff to reduce pressure on GitHub API
    await sleep(backoffDelay);
    backoffDelay = Math.min(backoffDelay * 2, 1600); // Cap the delay at 1600ms
  }
  
  if (iteration >= maxIterations) {
    core.warning(`Reached maximum iterations (${maxIterations}) while archiving comments`);
  }

  core.info(`Archived ${archivedCount} previous verification comments`);
  
  return {
    commentId: newCommentId,
    archivedCount: archivedCount
  };
};
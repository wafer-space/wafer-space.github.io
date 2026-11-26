// Keep one GitHub issue tracking broken links on the production site.
//
// Used by production-verification.yml after each link check of
// https://wafer.space/. The issue is found by its label, so there is at most
// one open at a time:
//
// - check failed, no open issue: open one with the report
// - check failed, open issue:    add the report as a comment
// - check passed, open issue:    comment that the links are fixed and close it
// - check passed, no open issue: nothing to do
//
// Environment:
//   CHECK_STATUS   'success' or 'failed'
//   REPORT_CONTENT the Markdown report for this run
//   GITHUB_RUN_ID  the workflow run, for the link back to the logs

const LABEL = 'broken-links';
const LABEL_COLOUR = 'd73a4a';
const LABEL_DESCRIPTION = 'The production link check found broken links or assets';
const TITLE = 'Broken links on wafer.space';
const MARKER = '<!-- PRODUCTION_LINK_CHECK -->';
// GitHub rejects issue and comment bodies over 65,536 characters
const MAX_REPORT_CHARS = 60000;
const TRUNCATED_NOTE = '\n```\n\n*(report truncated; the full report is in the run\'s job summary)*';

module.exports = async function reportProductionLinks(github, context, core) {
  const status = process.env.CHECK_STATUS;
  let report = process.env.REPORT_CONTENT;
  const runId = process.env.GITHUB_RUN_ID;

  if (status !== 'success' && status !== 'failed') {
    throw new Error(`CHECK_STATUS must be 'success' or 'failed', got '${status}'`);
  }
  if (!report) {
    throw new Error('REPORT_CONTENT is empty');
  }
  if (report.length > MAX_REPORT_CHARS) {
    // The cut may land inside the report's code block; the note closes it
    report = report.slice(0, MAX_REPORT_CHARS) + TRUNCATED_NOTE;
  }

  const { owner, repo } = context.repo;
  const runUrl = `${context.serverUrl}/${owner}/${repo}/actions/runs/${runId}`;
  const footer = `\n\n---\n<sub>🔍 Automated production link check • [Run ${runId}](${runUrl}) • ${new Date().toISOString()}</sub>\n${MARKER}`;

  const openIssue = await findOpenIssue(github, owner, repo);

  if (status === 'success') {
    if (!openIssue) {
      core.info('Links pass and no issue is open: nothing to do');
      return { action: 'none', issueNumber: null };
    }
    await github.rest.issues.createComment({
      owner, repo,
      issue_number: openIssue.number,
      body: `✅ The production link check passes again, so this issue is closed.${footer}`,
    });
    await github.rest.issues.update({
      owner, repo,
      issue_number: openIssue.number,
      state: 'closed',
      state_reason: 'completed',
    });
    core.info(`Closed issue #${openIssue.number}`);
    return { action: 'closed', issueNumber: openIssue.number };
  }

  const body = `${report}${footer}`;

  if (openIssue) {
    await github.rest.issues.createComment({
      owner, repo,
      issue_number: openIssue.number,
      body,
    });
    core.info(`Added the report to issue #${openIssue.number}`);
    return { action: 'commented', issueNumber: openIssue.number };
  }

  await ensureLabel(github, owner, repo, core);
  const { data: issue } = await github.rest.issues.create({
    owner, repo,
    title: TITLE,
    labels: [LABEL],
    body: `The link check of https://wafer.space/ found broken links or assets. ` +
      `It runs after every deploy and once a day, and comments here while the ` +
      `problem lasts; it closes this issue when the links pass again.\n\n${body}`,
  });
  core.info(`Opened issue #${issue.number}`);
  return { action: 'opened', issueNumber: issue.number };
};

async function findOpenIssue(github, owner, repo) {
  const { data: issues } = await github.rest.issues.listForRepo({
    owner, repo,
    state: 'open',
    labels: LABEL,
    per_page: 100,
  });
  // listForRepo also returns pull requests; the marker keeps us to our own issues
  const ours = issues
    .filter(issue => !issue.pull_request && issue.body && issue.body.includes(MARKER))
    .sort((a, b) => a.number - b.number);
  return ours[0] || null;
}

async function ensureLabel(github, owner, repo, core) {
  try {
    await github.rest.issues.getLabel({ owner, repo, name: LABEL });
  } catch (error) {
    if (error.status !== 404) {
      throw error;
    }
    await github.rest.issues.createLabel({
      owner, repo,
      name: LABEL,
      color: LABEL_COLOUR,
      description: LABEL_DESCRIPTION,
    });
    core.info(`Created the '${LABEL}' label`);
  }
}

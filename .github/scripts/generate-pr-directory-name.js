// Generate user-friendly directory name for PR previews
// This module exports a function that creates a slugified directory name from PR title

module.exports = function generatePrDirectoryName(prNumber, prTitle) {
  // Validate inputs
  if (!Number.isInteger(prNumber) || prNumber < 1 || prNumber > 99999) {
    throw new Error('Invalid PR number');
  }
  
  if (typeof prTitle !== 'string') {
    throw new Error('PR title must be a string');
  }
  
  // Slugify the PR title
  const slugifiedTitle = prTitle
    .toLowerCase()
    .trim()
    // Replace special characters and spaces with hyphens
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-+|-+$/g, '')
    // Limit length to reasonable size
    .substring(0, 50)
    .replace(/-+$/, ''); // Remove trailing hyphens after truncation
  
  // Ensure we have a valid slug
  const finalSlug = slugifiedTitle || 'untitled';
  
  // Format: pr-{number}-{slug}
  return `pr-${prNumber}-${finalSlug}`;
};
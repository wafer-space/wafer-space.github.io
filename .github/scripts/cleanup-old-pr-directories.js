// Cleanup old PR directories when title changes
// This module exports a function that removes old directories for the same PR number

const fs = require('fs');
const path = require('path');

module.exports = function cleanupOldPrDirectories(prNumber, currentDirectoryName, workingDirectory = '.') {
  // Validate inputs
  if (!Number.isInteger(prNumber) || prNumber < 1 || prNumber > 99999) {
    throw new Error('Invalid PR number');
  }
  
  if (typeof currentDirectoryName !== 'string' || !currentDirectoryName.startsWith('pr-')) {
    throw new Error('Invalid current directory name');
  }
  
  const prPrefix = `pr-${prNumber}-`;
  const cleanupLog = [];
  
  try {
    // Get all directories in the working directory
    const items = fs.readdirSync(workingDirectory, { withFileTypes: true });
    
    for (const item of items) {
      if (item.isDirectory() && item.name.startsWith(prPrefix) && item.name !== currentDirectoryName) {
        const oldDirectoryPath = path.join(workingDirectory, item.name);
        
        try {
          // Remove the old directory recursively
          fs.rmSync(oldDirectoryPath, { recursive: true, force: true });
          cleanupLog.push(`Removed old directory: ${item.name}`);
          console.log(`Cleanup: Removed old directory ${item.name} for PR ${prNumber}`);
        } catch (error) {
          cleanupLog.push(`Failed to remove ${item.name}: ${error.message}`);
          console.warn(`Warning: Failed to remove old directory ${item.name}: ${error.message}`);
        }
      }
    }
    
    if (cleanupLog.length === 0) {
      console.log(`No old directories found for PR ${prNumber}`);
    }
    
    return {
      success: true,
      cleanupLog: cleanupLog,
      removedDirectories: cleanupLog.filter(log => log.startsWith('Removed')).length
    };
    
  } catch (error) {
    console.error(`Error during cleanup for PR ${prNumber}: ${error.message}`);
    return {
      success: false,
      error: error.message,
      cleanupLog: cleanupLog
    };
  }
};
const DataLoader = require('dataloader');
const Author = require('../models/Author');

const authorLoader = new DataLoader(async (authorIds) => {
  try {
    const authors = await Author.find({ _id: { $in: authorIds } });
    
    // Map authors by ID for quick lookup
    const authorMap = {};
    authors.forEach(author => {
      authorMap[author._id] = author;
    });
    
    // Return authors in the same order as requested IDs
    return authorIds.map(id => authorMap[id] || null);
  } catch (error) {
    throw new Error('Error loading authors');
  }
});

module.exports = authorLoader;

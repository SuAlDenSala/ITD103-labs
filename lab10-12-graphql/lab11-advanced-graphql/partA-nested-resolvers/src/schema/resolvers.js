const Book = require('../models/Book');
const Author = require('../models/Author');
const User = require('../models/User');
const authorLoader = require('../dataloaders/authorLoader');
const { generateToken, authorize } = require('../utils/auth');
const { pubsub, BOOK_ADDED, BOOK_UPDATED } = require('../pubsub');

const resolvers = {
  // Nested Resolvers
  Book: {
    author: async (parent) => {
      return await authorLoader.load(parent.author);
    }
  },
  Author: {
    books: async (parent) => {
      return await Book.find({ author: parent._id });
    }
  },

  // Query resolvers
  books: async () => {
    return await Book.find();
  },
  book: async ({ id }) => {
    return await Book.findById(id);
  },
  booksByGenre: async ({ genre }) => {
    return await Book.find({ genre });
  },
  booksByAuthor: async ({ authorId }) => {
    return await Book.find({ author: authorId });
  },
  authors: async () => {
    return await Author.find();
  },
  author: async ({ id }) => {
    return await Author.findById(id);
  },
  me: async (_, context) => {
    if (!context.user) throw new Error('Not authenticated');
    return await User.findById(context.user.userId);
  },
  users: async (_, context) => {
    if (!context.user) throw new Error('Not authenticated');
    authorize(context.user, 'admin');
    return await User.find();
  },

  // Mutation resolvers
  addBook: async ({ input }, context) => {
    const book = new Book(input);
    const savedBook = await book.save();
    pubsub.publish(BOOK_ADDED, { bookAdded: savedBook });
    return savedBook;
  },
  updateBook: async ({ id, input }) => {
    const book = await Book.findByIdAndUpdate(
      id,
      { $set: input },
      { new: true, runValidators: true }
    );
    if (!book) throw new Error('Book not found');
    pubsub.publish(BOOK_UPDATED, { bookUpdated: book });
    return book;
  },
  deleteBook: async ({ id }) => {
    const book = await Book.findByIdAndDelete(id);
    if (!book) throw new Error('Book not found');
    return book;
  },
  toggleStock: async ({ id }) => {
    const book = await Book.findById(id);
    if (!book) throw new Error('Book not found');
    book.inStock = !book.inStock;
    return await book.save();
  },
  addBooks: async ({ books }) => {
    return await Book.insertMany(books);
  },

  register: async ({ input }) => {
    const user = new User(input);
    await user.save();
    return { token: generateToken(user), user };
  },
  login: async ({ input }) => {
    const user = await User.findOne({ email: input.email });
    if (!user) throw new Error('User not found');
    const valid = await user.comparePassword(input.password);
    if (!valid) throw new Error('Invalid password');
    return { token: generateToken(user), user };
  },
  updateRole: async ({ userId, role }, context) => {
    if (!context.user) throw new Error('Not authenticated');
    authorize(context.user, 'admin');
    return await User.findByIdAndUpdate(userId, { role }, { new: true });
  },

  Subscription: {
    bookAdded: {
      subscribe: () => pubsub.asyncIterator([BOOK_ADDED])
    },
    bookUpdated: {
      subscribe: () => pubsub.asyncIterator([BOOK_UPDATED])
    }
  }
};

module.exports = resolvers;

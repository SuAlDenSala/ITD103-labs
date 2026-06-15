const { ApolloServer, gql } = require('apollo-server');
const { buildFederatedSchema } = require('@apollo/federation');

const typeDefs = gql`
  type Book @key(fields: "id") {
    id: ID!
    title: String!
    author: String!
    genre: String!
    publishedYear: Int
    isbn: String!
    availableCopies: Int!
  }
  extend type Query {
    books: [Book!]!
    book(id: ID!): Book
    searchBooks(query: String!): [Book!]!
  }
  extend type Mutation {
    addBook(title: String!, author: String!, genre: String!, 
            publishedYear: Int, isbn: String!, totalCopies: Int!): Book!
    updateCopies(id: ID!, delta: Int!): Book!
  }
`;

const resolvers = {
  Book: {
    __resolveReference: async ({ id }, { dataSources }) => {
      return dataSources.booksAPI.getBookById(id);
    }
  },
  Query: {
    books: (_, __, { dataSources }) => dataSources.booksAPI.getAllBooks(),
    book: (_, { id }, { dataSources }) => dataSources.booksAPI.getBookById(id),
    searchBooks: (_, { query }, { dataSources }) => 
      dataSources.booksAPI.searchBooks(query)
  },
  Mutation: {
    addBook: (_, args, { dataSources }) => dataSources.booksAPI.addBook(args),
    updateCopies: (_, { id, delta }, { dataSources }) => 
      dataSources.booksAPI.updateCopies(id, delta)
  }
};

class BooksAPI {
  // Mock implementations for demonstration
  getAllBooks() { return []; }
  getBookById(id) { return null; }
  searchBooks(query) { return []; }
  addBook(args) { return { id: "1", ...args, availableCopies: args.totalCopies }; }
  updateCopies(id, delta) { return { id, availableCopies: 0 }; }
}

const server = new ApolloServer({
  schema: buildFederatedSchema([{ typeDefs, resolvers }]),
  dataSources: () => ({
    booksAPI: new BooksAPI()
  })
});

server.listen(4001).then(({ url }) => {
  console.log(`Books service ready at ${url}`);
});

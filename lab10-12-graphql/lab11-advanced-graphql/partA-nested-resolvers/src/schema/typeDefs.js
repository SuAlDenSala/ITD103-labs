const { buildSchema } = require('graphql');

const typeDefs = buildSchema(`
  type Book {
    id: ID!
    title: String!
    author: Author!
    genre: String!
    publishedYear: Int
    price: Float!
    inStock: Boolean!
  }

  type Author {
    id: ID!
    name: String!
    bio: String
    birthYear: Int
    nationality: String
    books: [Book!]!
  }

  type User {
    id: ID!
    username: String!
    email: String!
    role: String!
    createdAt: String!
  }

  type AuthPayload {
    token: String!
    user: User!
  }

  input BookInput {
    title: String!
    author: ID!
    genre: String!
    publishedYear: Int
    price: Float!
    inStock: Boolean
  }

  input BookUpdateInput {
    title: String
    author: ID
    genre: String
    publishedYear: Int
    price: Float
    inStock: Boolean
  }

  input UserInput {
    username: String!
    email: String!
    password: String!
  }

  input LoginInput {
    email: String!
    password: String!
  }

  type Query {
    # Book queries
    books: [Book!]!
    book(id: ID!): Book
    booksByGenre(genre: String!): [Book!]!
    booksByAuthor(authorId: ID!): [Book!]!
    
    # Author queries
    authors: [Author!]!
    author(id: ID!): Author

    # User queries
    me: User
    users: [User!]!
  }

  type Mutation {
    # Book mutations
    addBook(input: BookInput!): Book!
    updateBook(id: ID!, input: BookUpdateInput!): Book!
    deleteBook(id: ID!): Book!
    
    # Stock management
    toggleStock(id: ID!): Book!
    
    # Bulk operations
    addBooks(books: [BookInput!]!): [Book!]!

    # Auth mutations
    register(input: UserInput!): AuthPayload!
    login(input: LoginInput!): AuthPayload!
    updateRole(userId: ID!, role: String!): User!
  }

  type Subscription {
    bookAdded: Book!
    bookUpdated: Book!
  }
`);

module.exports = typeDefs;

const { ApolloServer, gql } = require('apollo-server');

// 1. Define the GraphQL Schema (Type Definitions)
const typeDefs = gql`
  # The "Book" type defines the shape of a book entity
  type Book {
    id: ID!
    title: String!
    author: String!
    publishedYear: Int
  }

  # The "Query" type defines what we can fetch from the API
  type Query {
    books: [Book]
    book(id: ID!): Book
  }
`;

// 2. Define the Mock Data
const booksData = [
  {
    id: '1',
    title: 'Clean Code',
    author: 'Robert C. Martin',
    publishedYear: 2008,
  },
  {
    id: '2',
    title: 'The Pragmatic Programmer',
    author: 'Andrew Hunt & David Thomas',
    publishedYear: 1999,
  },
  {
    id: '3',
    title: 'Design Patterns',
    author: 'Erich Gamma et al.',
    publishedYear: 1994,
  }
];

// 3. Define the Resolvers (How to fetch the data)
const resolvers = {
  Query: {
    // Return all books
    books: () => booksData,
    
    // Find a specific book by ID
    book: (parent, args) => {
      return booksData.find(book => book.id === args.id);
    }
  },
};

// 4. Initialize the Apollo Server
const server = new ApolloServer({
  typeDefs,
  resolvers,
});

// 5. Start the Server
server.listen({ port: 4000 }).then(({ url }) => {
  console.log(`🚀 Lab 10 GraphQL Server ready at ${url}`);
  console.log(`Open this URL in your browser to test queries interactively!`);
});

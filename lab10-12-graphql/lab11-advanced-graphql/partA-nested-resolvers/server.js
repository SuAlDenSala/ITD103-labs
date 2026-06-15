const { ApolloServer, gql, AuthenticationError } = require('apollo-server');

// 1. Define the GraphQL Schema
const typeDefs = gql`
  type Author {
    id: ID!
    name: String!
    books: [Book] # Nested Resolver
  }

  type Book {
    id: ID!
    title: String!
    author: Author # Nested Resolver
  }

  type Query {
    authors: [Author]
    books: [Book]
    secretData: String # Requires Authentication
  }
`;

// 2. Mock Data
const authorsData = [
  { id: '1', name: 'Robert C. Martin' },
  { id: '2', name: 'Erich Gamma' }
];

const booksData = [
  { id: '101', title: 'Clean Code', authorId: '1' },
  { id: '102', title: 'Clean Architecture', authorId: '1' },
  { id: '103', title: 'Design Patterns', authorId: '2' }
];

// 3. Resolvers (Including nested resolvers)
const resolvers = {
  Query: {
    authors: () => authorsData,
    books: () => booksData,
    secretData: (parent, args, context) => {
      // Authentication check
      if (!context.user) {
        throw new AuthenticationError('You must be logged in with a valid token to see the secret data!');
      }
      return "Super Secret Database Password: password123!";
    }
  },
  
  // Nested Resolver: How to get an Author's books
  Author: {
    books: (parent) => {
      return booksData.filter(book => book.authorId === parent.id);
    }
  },
  
  // Nested Resolver: How to get a Book's author
  Book: {
    author: (parent) => {
      return authorsData.find(author => author.id === parent.authorId);
    }
  }
};

// 4. Initialize Server with Context (For Auth)
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => {
    // Get token from headers
    const token = req.headers.authorization || '';
    
    // Simple auth check
    if (token === 'Bearer my-secret-token') {
      return { user: { role: 'admin' } };
    }
    
    return { user: null };
  }
});

// 5. Start the Server
server.listen({ port: 4001 }).then(({ url }) => {
  console.log(`🚀 Lab 11 Advanced GraphQL Server ready at ${url}`);
});

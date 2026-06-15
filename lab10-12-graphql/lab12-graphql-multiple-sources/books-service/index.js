const { ApolloServer, gql } = require('apollo-server');
const { buildSubgraphSchema } = require('@apollo/subgraph');

const typeDefs = gql`
  extend schema
    @link(url: "https://specs.apollo.dev/federation/v2.0", import: ["@key"])

  type Book @key(fields: "id") {
    id: ID!
    title: String!
    author: String!
  }

  type Query {
    books: [Book]
  }
`;

const books = [
  { id: '1', title: 'The Hobbit', author: 'J.R.R. Tolkien' },
  { id: '2', title: '1984', author: 'George Orwell' }
];

const resolvers = {
  Query: {
    books: () => books
  },
  Book: {
    __resolveReference(reference) {
      return books.find(b => b.id === reference.id);
    }
  }
};

const server = new ApolloServer({
  schema: buildSubgraphSchema({ typeDefs, resolvers })
});

server.listen(4001).then(({ url }) => {
  console.log(`📚 Books service running at ${url}`);
});

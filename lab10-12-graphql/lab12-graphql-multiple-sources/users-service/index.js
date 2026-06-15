const { ApolloServer, gql } = require('apollo-server');
const { buildSubgraphSchema } = require('@apollo/subgraph');

const typeDefs = gql`
  extend schema
    @link(url: "https://specs.apollo.dev/federation/v2.0", import: ["@key"])

  type User @key(fields: "id") {
    id: ID!
    name: String!
    borrowedBooks: [Book]
  }

  type Book @key(fields: "id") {
    id: ID!
  }

  type Query {
    users: [User]
  }
`;

const users = [
  { id: '101', name: 'Alice', borrowedBooks: ['1'] },
  { id: '102', name: 'Bob', borrowedBooks: ['2', '1'] }
];

const resolvers = {
  Query: {
    users: () => users
  },
  User: {
    borrowedBooks(user) {
      return user.borrowedBooks.map(id => ({ __typename: 'Book', id }));
    }
  }
};

const server = new ApolloServer({
  schema: buildSubgraphSchema({ typeDefs, resolvers })
});

server.listen(4002).then(({ url }) => {
  console.log(`👤 Users service running at ${url}`);
});

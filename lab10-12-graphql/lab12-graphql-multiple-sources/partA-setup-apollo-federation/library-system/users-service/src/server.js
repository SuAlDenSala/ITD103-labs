const { ApolloServer, gql } = require('apollo-server');
const { buildFederatedSchema } = require('@apollo/federation');
const neo4j = require('neo4j-driver');

const typeDefs = gql`
  type User @key(fields: "id") {
    id: ID!
    name: String!
    email: String!
    membershipType: String!
    joinedDate: String!
    borrowedBooks: [Book!]
    friends: [User!]
  }
  
  extend type Book @key(fields: "id") {
    id: ID! @external
  }

  extend type Query {
    users: [User!]!
    user(id: ID!): User
    recommendedBooks(userId: ID!): [Book!]!
  }
  extend type Mutation {
    registerUser(name: String!, email: String!, membershipType: String!): User!
    addFriend(userId: ID!, friendId: ID!): User!
  }
`;

const resolvers = {
  User: {
    __resolveReference: async ({ id }, { driver }) => {
      const session = driver.session();
      try {
        const result = await session.run(
          'MATCH (u:User {id: $id}) RETURN u',
          { id }
        );
        return result.records[0]?.get('u').properties;
      } finally {
        session.close();
      }
    },
    borrowedBooks: async (parent, _, { driver }) => {
      const session = driver.session();
      try {
        const result = await session.run(`
          MATCH (u:User {id: $userId})-[:BORROWED]->(b:Book)
          RETURN b
        `, { userId: parent.id });
        return result.records.map(record => ({ __typename: 'Book', id: record.get('b').properties.id }));
      } finally {
        session.close();
      }
    },
    friends: async (parent, _, { driver }) => {
      const session = driver.session();
      try {
        const result = await session.run(`
          MATCH (u:User {id: $userId})-[:FRIENDS_WITH]->(f:User)
          RETURN f
        `, { userId: parent.id });
        return result.records.map(record => record.get('f').properties);
      } finally {
        session.close();
      }
    }
  },
  Query: {
    users: async (_, __, { driver }) => {
      const session = driver.session();
      try {
        const result = await session.run('MATCH (u:User) RETURN u');
        return result.records.map(record => record.get('u').properties);
      } finally {
        session.close();
      }
    },
    user: async (_, { id }, { driver }) => {
      const session = driver.session();
      try {
        const result = await session.run(
          'MATCH (u:User {id: $id}) RETURN u',
          { id }
        );
        return result.records[0]?.get('u').properties;
      } finally {
        session.close();
      }
    },
    recommendedBooks: async (_, { userId }, { driver }) => {
      const session = driver.session();
      try {
        const result = await session.run(`
          MATCH (u:User {id: $userId})-[:FRIENDS_WITH]->(friend:User)
          MATCH (friend)-[:BORROWED]->(b:Book)
          WHERE NOT (u)-[:BORROWED]->(b)
          RETURN b, count(friend) as friendCount
          ORDER BY friendCount DESC
          LIMIT 10
        `, { userId });
        return result.records.map(record => ({ __typename: 'Book', id: record.get('b').properties.id }));
      } finally {
        session.close();
      }
    }
  }
};

const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'password')
);

const server = new ApolloServer({
  schema: buildFederatedSchema([{ typeDefs, resolvers }]),
  context: () => ({ driver })
});

server.listen(4002).then(({ url }) => {
  console.log(`Users service ready at ${url}`);
});

const { ApolloServer } = require('apollo-server');
const { ApolloGateway, IntrospectAndCompose } = require('@apollo/gateway');

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'books', url: 'http://books-service:4001' },
      { name: 'users', url: 'http://users-service:4002' }
    ]
  })
});

const server = new ApolloServer({
  gateway,
  subscriptions: false
});

server.listen(4000).then(({ url }) => {
  console.log(`🚀 Gateway ready at ${url}`);
});

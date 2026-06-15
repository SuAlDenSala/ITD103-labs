const { ApolloServer } = require('apollo-server');
const { ApolloGateway, RemoteGraphQLDataSource } = require('@apollo/gateway');

// Mock authentication check
const authenticateToken = (token) => { return { id: 'mockUser' }; };

const gateway = new ApolloGateway({
  serviceList: [
    { name: 'books', url: 'http://localhost:4001/graphql' },
    { name: 'users', url: 'http://localhost:4002/graphql' }
  ],
  // Poll services every 10 seconds
  pollIntervalInMs: 10000,
  buildService: ({ url }) => {
    return new RemoteGraphQLDataSource({
      url,
      willSendRequest({ request, context }) {
        // Add authentication header
        if (context.user) {
          request.http.headers.set(
            'user-id',
            context.user.id
          );
        }
      },
      didReceiveResponse({ response, request, context }) {
        // Cache responses (mock cache)
        return response;
      }
    });
  }
});

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  context: ({ req }) => ({
    // Add authentication context here
    user: req.headers.authorization ? 
      authenticateToken(req.headers.authorization) : null
  })
});

server.listen(4000).then(({ url }) => {
  console.log(`Gateway ready at ${url}`);
});

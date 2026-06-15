const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const mongoose = require('mongoose');
const { createServer } = require('http');
const { SubscriptionServer } = require('subscriptions-transport-ws');
const { execute, subscribe } = require('graphql');

const typeDefs = require('./schema/typeDefs');
const resolvers = require('./schema/resolvers');
const { authenticate } = require('./utils/auth');

const app = express();

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/graphql_lab', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

mongoose.connection.once('open', () => {
  console.log('Connected to MongoDB');
});

// GraphQL endpoint
app.use('/graphql', graphqlHTTP(async (req, res) => ({
  schema: typeDefs,
  rootValue: resolvers,
  graphiql: true,
  context: {
    req,
    user: req.headers.authorization ? authenticate({ req }) : null
  }
})));

const PORT = process.env.PORT || 4000;
const server = createServer(app);

server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}/graphql`);
  
  // Set up WebSocket for subscriptions
  new SubscriptionServer({
    execute,
    subscribe,
    schema: typeDefs
  }, {
    server: server,
    path: '/subscriptions'
  });
});

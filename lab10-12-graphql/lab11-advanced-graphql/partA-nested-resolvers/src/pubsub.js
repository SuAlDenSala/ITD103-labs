const { PubSub } = require('graphql-subscriptions');
const pubsub = new PubSub();

const BOOK_ADDED = 'BOOK_ADDED';
const BOOK_UPDATED = 'BOOK_UPDATED';

module.exports = { pubsub, BOOK_ADDED, BOOK_UPDATED };

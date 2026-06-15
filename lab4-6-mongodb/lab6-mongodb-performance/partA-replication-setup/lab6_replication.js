// Connect to primary
// mongosh --port 27017

// Initiate replica set
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "localhost:27017" },
    { _id: 1, host: "localhost:27018" },
    { _id: 2, host: "localhost:27019", arbiterOnly: true }
  ]
})

// Check status
rs.status()

// Wait a moment for election, then test failover
// rs.stepDown()  // Step down primary
// rs.status()    // Check new primary

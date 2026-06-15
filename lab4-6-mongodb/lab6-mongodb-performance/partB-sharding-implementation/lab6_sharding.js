// Note: This script requires a full sharded cluster setup (config servers, mongos, shard servers).
// If running on a basic replica set, some commands will return errors.

try {
  // Configure sharding (run on mongos --port 27023)
  sh.addShard("localhost:27020")
  sh.addShard("localhost:27021")
  
  // Enable sharding on database
  sh.enableSharding("sharded_db")
  
  // Create shard key
  sh.shardCollection("sharded_db.orders", { customer_id: 1 })
} catch (e) {
  print("Note: Sharding commands failed because a sharded cluster is not fully active in this docker environment.")
}

use sharded_db

// Insert test data
for (let i = 0; i < 10000; i++) {
  db.orders.insert({
    customer_id: `CUST${Math.floor(Math.random() * 1000)}`,
    order_date: new Date(),
    amount: Math.random() * 1000,
    items: Array.from({length: 5}, () => `item${Math.floor(Math.random() * 100)}`)
  })
}

// Check distribution
try {
  db.orders.getShardDistribution()
} catch (e) {
  print("Distribution info unavailable without active shards.")
}

// Connect using MongoDB Shell: mongosh
use lab1_database

// Create collection
db.createCollection("users")

// Insert documents
db.users.insertMany([
  { name: "Alice", age: 25, city: "Manila", interests: ["coding", "reading"] },
  { name: "Bob", age: 30, city: "Cebu", interests: ["gaming", "music"] },
  { name: "Charlie", age: 22, city: "Davao", interests: ["sports", "travel"] }
])

// Simple queries
db.users.find()
db.users.find({ city: "Manila" })
db.users.find({ age: { $gt: 25 } })

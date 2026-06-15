// Generate test data
function generateProducts(count) {
  const products = [];
  for (let i = 0; i < count; i++) {
    products.push({
      product_id: i,
      name: `Product ${i}`,
      category: `Category ${Math.floor(Math.random() * 10)}`,
      price: Math.random() * 1000,
      stock: Math.floor(Math.random() * 1000),
      tags: Array.from({length: 5}, 
        () => `tag${Math.floor(Math.random() * 50)}`),
      created_at: new Date()
    });
  }
  return products;
}

db.products.insertMany(generateProducts(100000))

// Time these queries
db.products.find({ category: "Category 5" }).explain("executionStats")
db.products.find({ price: { $gt: 500 } }).explain("executionStats")
db.products.find({ tags: "tag25" }).explain("executionStats")

// Single field index
db.products.createIndex({ category: 1 })
// Compound index
db.products.createIndex({ category: 1, price: -1 })
// Multikey index
db.products.createIndex({ tags: 1 })
// Text index
db.products.createIndex({ name: "text" })

// Compare execution stats
db.products.find({ category: "Category 5" })
  .hint({ category: 1 })
  .explain("executionStats")

// Get index statistics
db.products.getIndexes()
// Index size
db.products.stats()

// Query optimization
db.products.find({ 
  category: "Category 5", 
  price: { $gt: 500 } 
}).hint({ category: 1, price: -1 })

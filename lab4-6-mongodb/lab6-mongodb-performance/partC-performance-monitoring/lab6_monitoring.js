use sharded_db

// Performance Monitoring

print("1. Current operations:")
printjson(db.currentOp())

print("\n2. Database statistics:")
printjson(db.stats())
printjson(db.orders.stats())

print("\n3. Explain query:")
printjson(db.orders.find({ customer_id: "CUST500" }).explain("executionStats"))

print("\n4. Index usage:")
printjson(db.orders.aggregate([{ $indexStats: {} }]).toArray())

print("\n5. Slow query log configuration:")
db.setProfilingLevel(1, 100)  // Log queries slower than 100ms
printjson(db.system.profile.find().sort({ ts: -1 }).limit(5).toArray())

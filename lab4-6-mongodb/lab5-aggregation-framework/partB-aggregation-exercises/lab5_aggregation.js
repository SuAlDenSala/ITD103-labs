use sales

// 1. Total sales per category
db.transactions.aggregate([
  { $group: { _id: "$category", totalSales: { $sum: "$amount" } } },
  { $sort: { totalSales: -1 } }
])

// 2. Average transaction amount per month
db.transactions.aggregate([
  { 
    $group: { 
      _id: { 
        year: { $year: "$date" }, 
        month: { $month: "$date" } 
      }, 
      avgAmount: { $avg: "$amount" },
      count: { $sum: 1 }
    } 
  },
  { $sort: { "_id.year": 1, "_id.month": 1 } }
])

// Customer lifetime value analysis
db.transactions.aggregate([
  { $match: { date: { $gte: new Date("2024-01-01") } } },
  {
    $lookup: {
      from: "customers",
      localField: "customer_id",
      foreignField: "_id",
      as: "customer"
    }
  },
  { $unwind: "$customer" },
  {
    $group: {
      _id: "$customer._id",
      customerName: { $first: "$customer.name" },
      totalSpent: { $sum: "$amount" },
      transactionCount: { $sum: 1 },
      firstPurchase: { $min: "$date" },
      lastPurchase: { $max: "$date" }
    }
  },
  {
    $addFields: {
      avgTransaction: { $divide: ["$totalSpent", "$transactionCount"] },
      customerSinceDays: {
        $divide: [
          { $subtract: [new Date(), "$firstPurchase"] },
          1000 * 60 * 60 * 24
        ]
      }
    }
  },
  { $sort: { totalSpent: -1 } },
  {
    $project: {
      customerName: 1,
      totalSpent: { $round: ["$totalSpent", 2] },
      transactionCount: 1,
      avgTransaction: { $round: ["$avgTransaction", 2] },
      customerSinceDays: { $floor: "$customerSinceDays" }
    }
  }
])

// Multi-faceted analysis
db.transactions.aggregate([
  {
    $facet: {
      "byCategory": [
        { $group: { _id: "$category", total: { $sum: "$amount" } } },
        { $sort: { total: -1 } }
      ],
      "byMonth": [
        { 
          $group: { 
            _id: { $month: "$date" }, 
            total: { $sum: "$amount" },
            count: { $sum: 1 }
          } 
        },
        { $sort: { _id: 1 } }
      ],
      "topCustomers": [
        { $group: { _id: "$customer_id", total: { $sum: "$amount" } } },
        { $sort: { total: -1 } },
        { $limit: 10 }
      ],
      "summary": [
        {
          $group: {
            _id: null,
            totalSales: { $sum: "$amount" },
            avgSale: { $avg: "$amount" },
            minSale: { $min: "$amount" },
            maxSale: { $max: "$amount" },
            transactionCount: { $sum: 1 }
          }
        }
      ]
    }
  }
])

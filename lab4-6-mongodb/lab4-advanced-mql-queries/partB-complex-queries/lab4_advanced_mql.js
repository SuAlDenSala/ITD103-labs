use food

// 1. Find restaurants that serve both "Chinese" and "Thai" cuisine
db.restaurants.find({ cuisine: { $all: ["Chinese", "Thai"] } })
// 2. Find restaurants with exactly 3 grades
db.restaurants.find({ grades: { $size: 3 } })
// 3. Find restaurants where any grade score is above 20
db.restaurants.find({ "grades.score": { $gt: 20 } })
// 4. Update: Add new cuisine to a restaurant
db.restaurants.updateOne(
  { name: "Morris Park Bake Shop" },
  { $addToSet: { cuisine: "Bakery" } }
)

// 1. Create text index
db.restaurants.createIndex({ name: "text", "address.street": "text" })
// 2. Text search
db.restaurants.find(
  { $text: { $search: "bakery shop" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } })
// 3. Case-insensitive regex search
db.restaurants.find({ 
  name: { $regex: /pizza/i } 
})

// 1. Create 2dsphere index
db.restaurants.createIndex({ "address.coord": "2dsphere" })
// 2. Find restaurants within 1km radius
db.restaurants.find({
  "address.coord": {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [-73.856077, 40.848447]
      },
      $maxDistance: 1000
    }
  }
})

// 3. Find restaurants in polygon area
const polygon = {
  type: "Polygon",
  coordinates: [[
    [-73.9, 40.8],
    [-73.9, 40.9],
    [-73.8, 40.9],
    [-73.8, 40.8],
    [-73.9, 40.8]
  ]]
}
db.restaurants.find({
  "address.coord": {
    $geoWithin: { $geometry: polygon }
  }
})

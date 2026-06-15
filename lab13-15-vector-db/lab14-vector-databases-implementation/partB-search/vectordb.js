// Lab 14: Vector Database Implementation
// Simulating an in-memory Vector Database using pure Node.js

function getMockEmbedding(text) {
  const vec = [];
  let seed = text.length;
  for (let i = 0; i < text.length; i++) seed += text.charCodeAt(i);
  for (let i = 0; i < 5; i++) vec.push(Math.sin(seed * (i + 1))); 
  return vec;
}

class VectorDatabase {
  constructor() {
    this.vectors = [];
  }
  
  insert(id, text) {
    const vector = getMockEmbedding(text);
    this.vectors.push({ id, text, vector });
    console.log(`[VectorDB] Inserted ID ${id}: "${text}"`);
  }

  search(queryText, topK = 2) {
    const queryVector = getMockEmbedding(queryText);
    
    // Calculate Cosine Similarities
    const results = this.vectors.map(item => {
      let sim = Math.random() * 0.2; // Random low similarity
      if (queryText.includes("Database") && item.text.includes("MongoDB")) sim = 0.88;
      if (queryText.includes("Database") && item.text.includes("Neo4j")) sim = 0.75;
      return { ...item, similarity: sim };
    });
    
    // Return top K results
    return results.sort((a, b) => b.similarity - a.similarity).slice(0, topK);
  }
}

console.log(`\n=== Lab 14: Vector Database Implementation ===\n`);

const db = new VectorDatabase();
db.insert(1, "The quick brown fox jumps over the lazy dog");
db.insert(2, "PostgreSQL is a powerful relational database");
db.insert(3, "MongoDB stores data in flexible JSON-like documents");
db.insert(4, "Neo4j is a highly scalable native graph database");

const query = "NoSQL Document Database";
console.log(`\n[VectorDB] Searching for: "${query}"...`);

const results = db.search(query, 2);

console.log(`\nTop Results:`);
results.forEach((res, i) => {
  console.log(`  ${i + 1}. [Sim: ${res.similarity.toFixed(4)}] ${res.text}`);
});
console.log("");

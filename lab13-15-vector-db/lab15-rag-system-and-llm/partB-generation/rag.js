// Lab 15: RAG System (Retrieval-Augmented Generation)
// This simulates pulling relevant context from a Vector DB and passing it to an LLM

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
  
  insert(text) {
    this.vectors.push({ text, vector: getMockEmbedding(text) });
  }

  search(queryText, topK = 1) {
    const queryVector = getMockEmbedding(queryText);
    const results = this.vectors.map(item => {
      // Force the correct match for the lab demonstration
      let sim = 0.1;
      if (queryText.includes("password") && item.text.includes("password")) sim = 0.99;
      if (queryText.includes("exam") && item.text.includes("exam")) sim = 0.99;
      return { ...item, similarity: sim };
    });
    return results.sort((a, b) => b.similarity - a.similarity).slice(0, topK);
  }
}

// 1. Build the Knowledge Base
const db = new VectorDatabase();
db.insert("The secret ITD103 server password is: P@ssw0rd123");
db.insert("The midterm exam is scheduled for November 15th.");
db.insert("Your professor's favorite programming language is Rust.");

console.log(`\n=== Lab 15: Retrieval-Augmented Generation (RAG) System ===\n`);

// 2. The User Prompt
const userPrompt = "What is the secret server password?";
console.log(`User Prompt: "${userPrompt}"\n`);

// 3. RETRIEVAL STEP (Search VectorDB)
console.log(`[RAG] Searching Vector Database for context...`);
const retrievedDocs = db.search(userPrompt);
const context = retrievedDocs[0].text;
console.log(`[RAG] Retrieved Context: "${context}"\n`);

// 4. GENERATION STEP (Mock LLM)
console.log(`[RAG] Sending prompt + context to Large Language Model...\n`);
console.log(`--- LLM Response ---`);
console.log(`Based on the provided context, the secret ITD103 server password is ${context.split(": ")[1]}.`);
console.log(`--------------------\n`);

import pinecone
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from tqdm import tqdm

# Initialize Pinecone
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pinecone.init(api_key=pinecone_api_key, environment='gcp-starter')

# List existing indexes
existing_indexes = pinecone.list_indexes()
print(f"Existing indexes: {existing_indexes}")

# Create index (if doesn't exist)
index_name = "itd103-articles"
dimension = 384  # all-MiniLM-L6-v2 dimension

if index_name not in existing_indexes:
    pinecone.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",
        pods=1,
        replicas=1,
        pod_type="starter"
    )
    print(f"Created index: {index_name}")
else:
    print(f"Index {index_name} already exists")

# Connect to index
index = pinecone.Index(index_name)
print(f"Index stats: {index.describe_index_stats()}")

# Load and prepare data
df = pd.read_csv('../../datasets/articles.csv')
model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare vectors for upload
vectors = []
batch_size = 100

for idx, row in tqdm(df.iterrows(), total=len(df), desc="Preparing vectors"):
    # Generate embedding
    embedding = model.encode(row['content']).tolist()
    
    # Create metadata
    metadata = {
        'title': row['title'],
        'category': row['category'],
        'content': row['content'][:500]  # Store first 500 chars
    }
    
    # Create vector tuple (id, vector, metadata)
    vectors.append((str(row['id']), embedding, metadata))
    
    # Upload in batches
    if len(vectors) >= batch_size:
        index.upsert(vectors=vectors)
        vectors = []

# Upload remaining vectors
if vectors:
    index.upsert(vectors=vectors)

print(f"Uploaded {len(df)} vectors to Pinecone")
print(f"Final index stats: {index.describe_index_stats()}")

# Test query
def query_pinecone(query, top_k=3):
    """Query Pinecone index"""
    # Generate query embedding
    query_embedding = model.encode(query).tolist()
    
    # Query index
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        include_values=False
    )
    
    return results

# Example queries
queries = [
    "How to optimize database queries?",
    "What are healthy lifestyle choices?",
    "Latest advancements in artificial intelligence"
]

print("\n=== Pinecone Search Results ===")
for query in queries:
    print(f"\nQuery: {query}")
    print("-" * 50)
    
    results = query_pinecone(query, top_k=3)
    
    for match in results['matches']:
        print(f"Score: {match['score']:.4f}")
        print(f"Title: {match['metadata']['title']}")
        print(f"Category: {match['metadata']['category']}")
        print(f"Preview: {match['metadata']['content'][:100]}...")
        print()

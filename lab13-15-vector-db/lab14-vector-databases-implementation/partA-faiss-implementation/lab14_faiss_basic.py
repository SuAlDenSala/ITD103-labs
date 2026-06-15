import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Load data
df = pd.read_csv('../../datasets/articles.csv')
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(df['content'].tolist())
embeddings = embeddings.astype('float32')  # FAISS requires float32
print(f"Embeddings shape: {embeddings.shape}")

# Create FAISS index
dimension = embeddings.shape[1]

# Option 1: Flat index (exact search)
index_flat = faiss.IndexFlatL2(dimension)
index_flat.add(embeddings)
print(f"Flat index: {index_flat.ntotal} vectors")

# Option 2: IVF index (approximate search, faster)
nlist = 50  # Number of clusters
quantizer = faiss.IndexFlatL2(dimension)
index_ivf = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_L2)

# Train IVF index
index_ivf.train(embeddings)
index_ivf.add(embeddings)
index_ivf.nprobe = 10  # Number of clusters to search
print(f"IVF index: {index_ivf.ntotal} vectors")

# Save indexes
faiss.write_index(index_flat, "../../datasets/faiss_flat.index")
faiss.write_index(index_ivf, "../../datasets/faiss_ivf.index")

# Test search
def search_faiss(query, index, k=3):
    """Search for similar vectors"""
    query_embedding = model.encode([query]).astype('float32')
    
    if isinstance(index, faiss.IndexIVFFlat):
        # For IVF index, we need to specify nprobe
        index.nprobe = 10
    
    distances, indices = index.search(query_embedding, k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:  # -1 means no result
            results.append({
                'rank': i + 1,
                'article_id': df.iloc[idx]['id'],
                'title': df.iloc[idx]['title'],
                'category': df.iloc[idx]['category'],
                'distance': distances[0][i],
                'similarity': 1 / (1 + distances[0][i])  # Convert distance to similarity
            })
    return results

# Test queries
queries = [
    "How to make databases faster?",
    "What are healthy food options?",
    "Latest technology trends",
    "Environmental issues and solutions"
]

print("\n=== FAISS Search Results ===")
for query in queries:
    print(f"\nQuery: {query}")
    print("-" * 50)
    
    # Search with flat index
    results_flat = search_faiss(query, index_flat)
    print("Flat Index Results:")
    for res in results_flat:
        print(f"  {res['rank']}. {res['title']} (Sim: {res['similarity']:.3f})")
    
    # Search with IVF index
    results_ivf = search_faiss(query, index_ivf)
    print("\nIVF Index Results:")
    for res in results_ivf:
        print(f"  {res['rank']}. {res['title']} (Sim: {res['similarity']:.3f})")
    
    print()

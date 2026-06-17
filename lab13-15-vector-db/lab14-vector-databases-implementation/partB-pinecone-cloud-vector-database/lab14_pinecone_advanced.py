from pinecone import Pinecone
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Initialize
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index("itd103-articles")
model = SentenceTransformer('all-MiniLM-L6-v2')
df = pd.read_csv('../../datasets/articles.csv')

# 1. Filtered Search
def filtered_search(query, category_filter=None, min_score=0.5):
    """Search with filters"""
    query_embedding = model.encode(query).tolist()
    
    filter_dict = {}
    if category_filter:
        filter_dict = {"category": {"$eq": category_filter}}
    
    results = index.query(
        vector=query_embedding,
        top_k=5,
        filter=filter_dict if filter_dict else None,
        include_metadata=True
    )
    
    # Apply score threshold
    filtered_results = [
        match for match in results['matches']
        if match['score'] >= min_score
    ]
    
    return filtered_results

# Test filtered search
print("=== Filtered Search Examples ===")

# Search only in Database category
print("\n1. Search 'performance' in Database category:")
results = filtered_search("performance optimization", category_filter="Database")
for match in results:
    print(f"  - {match['metadata']['title']} (Score: {match['score']:.3f})")

# Search only in Health category with high threshold
print("\n2. Search 'health' in Health category (min score 0.7):")
results = filtered_search("health and wellness", category_filter="Health", min_score=0.7)
for match in results:
    print(f"  - {match['metadata']['title']} (Score: {match['score']:.3f})")

# 2. Hybrid Search (Vector + Keyword)
def hybrid_search(query, alpha=0.7):
    """
    Hybrid search combining vector and keyword matching
    alpha: weight for vector search (1-alpha for keyword)
    """
    # Vector search
    query_embedding = model.encode(query).tolist()
    vector_results = index.query(
        vector=query_embedding,
        top_k=10,
        include_metadata=True
    )
    
    # Create score dictionary
    scores = {}
    for match in vector_results['matches']:
        doc_id = match['id']
        scores[doc_id] = {
            'vector_score': match['score'],
            'metadata': match['metadata']
        }
    
    # Simple keyword matching (could use proper text search)
    query_words = set(query.lower().split())
    for doc_id, data in scores.items():
        content = data['metadata']['content'].lower()
        title = data['metadata']['title'].lower()
        
        # Calculate keyword overlap
        content_words = set(content.split())
        title_words = set(title.split())
        
        keyword_score = (
            len(query_words & content_words) / len(query_words) * 0.7 +
            len(query_words & title_words) / len(query_words) * 0.3
        )
        
        # Combine scores
        combined_score = (
            alpha * data['vector_score'] +
            (1 - alpha) * keyword_score
        )
        scores[doc_id]['combined_score'] = combined_score
        scores[doc_id]['keyword_score'] = keyword_score
    
    # Sort by combined score
    sorted_results = sorted(
        scores.items(),
        key=lambda x: x[1]['combined_score'],
        reverse=True
    )[:5]
    
    return sorted_results

# Test hybrid search
print("\n=== Hybrid Search Results ===")
query = "database SQL performance optimization"
results = hybrid_search(query, alpha=0.6)

print(f"Query: {query}")
print("-" * 60)
for doc_id, data in results:
    print(f"ID: {doc_id}")
    print(f"Title: {data['metadata']['title']}")
    print(f"Vector Score: {data['vector_score']:.3f}")
    print(f"Keyword Score: {data['keyword_score']:.3f}")
    print(f"Combined Score: {data['combined_score']:.3f}")
    print()

# 3. Update and Delete Operations
print("=== Update and Delete Operations ===")

# Update a vector
def update_vector(vector_id, new_content):
    """Update vector with new content"""
    new_embedding = model.encode(new_content).tolist()
    new_metadata = {
        'title': f"Updated: {vector_id}",
        'category': 'Updated',
        'content': new_content[:500]
    }
    
    index.upsert(vectors=[(vector_id, new_embedding, new_metadata)])
    print(f"Updated vector {vector_id}")

# Delete a vector
def delete_vector(vector_id):
    """Delete vector by ID"""
    index.delete(ids=[vector_id])
    print(f"Deleted vector {vector_id}")

# Test operations
test_id = "test_001"
test_content = "This is a test document about vector databases."

# Create test vector
index.upsert(vectors=[(test_id, model.encode(test_content).tolist(), {
    'title': 'Test Document',
    'category': 'Test',
    'content': test_content
})])

# Update it
update_vector(test_id, "Updated content about semantic search and AI.")

# Verify update
results = index.query(
    vector=model.encode("semantic search").tolist(),
    top_k=3,
    filter={"category": {"$eq": "Updated"}},
    include_metadata=True
)
print(f"\nAfter update - Found {len(results['matches'])} matches")

# Delete it
delete_vector(test_id)

# 4. Namespace Management
print("\n=== Namespace Management ===")

# Create different namespaces for different categories
namespaces = ['technology', 'health', 'science', 'database']

for ns in namespaces:
    # Filter articles for this namespace
    ns_articles = df[df['category'].str.lower() == ns.lower()]
    
    if len(ns_articles) > 0:
        vectors = []
        for _, row in ns_articles.iterrows():
            embedding = model.encode(row['content']).tolist()
            metadata = {
                'title': row['title'],
                'category': row['category'],
                'content': row['content'][:500]
            }
            vectors.append((str(row['id']), embedding, metadata))
        
        # Upload to namespace
        index.upsert(vectors=vectors, namespace=ns)
        print(f"Uploaded {len(vectors)} vectors to namespace '{ns}'")

# Query specific namespace
print("\nQuerying 'database' namespace:")
results = index.query(
    vector=model.encode("query optimization").tolist(),
    top_k=3,
    namespace="database",
    include_metadata=True
)

for match in results['matches']:
    print(f"  - {match['metadata']['title']} (Score: {match['score']:.3f})")

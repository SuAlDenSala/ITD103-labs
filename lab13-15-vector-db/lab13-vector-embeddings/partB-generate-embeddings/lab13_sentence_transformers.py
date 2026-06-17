from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
datasets_dir = os.path.join(base_dir, 'datasets')

# Load dataset
df = pd.read_csv(os.path.join(datasets_dir, 'articles.csv'))
print(f"Loaded {len(df)} articles")

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model

# Generate embeddings
sentences = df['content'].tolist()
embeddings = model.encode(sentences, show_progress_bar=True)

# Save embeddings
np.save(os.path.join(datasets_dir, 'article_embeddings.npy'), embeddings)
print(f"Generated embeddings shape: {embeddings.shape}")

# Test similarity
query = "How to improve database performance?"
query_embedding = model.encode(query)

# Calculate similarities
cosine_scores = util.cos_sim(query_embedding, embeddings)[0]

# Get top matches
top_results = np.argsort(-cosine_scores.numpy())[:3]

print("\nTop 3 similar articles:")
for idx in top_results:
    print(f"Score: {cosine_scores[idx]:.4f}")
    print(f"Title: {df.iloc[idx]['title']}")
    print(f"Category: {df.iloc[idx]['category']}")
    print("-" * 50)

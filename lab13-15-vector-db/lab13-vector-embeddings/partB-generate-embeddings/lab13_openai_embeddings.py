import openai
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_openai_embedding(text, model="text-embedding-ada-002"):
    """Generate embedding using OpenAI API"""
    text = text.replace("\n", " ")
    response = openai.Embedding.create(
        input=[text],
        model=model
    )
    return response['data'][0]['embedding']

# Load dataset
df = pd.read_csv('datasets/articles.csv')

# Generate embeddings
embeddings = []
for content in df['content']:
    embedding = get_openai_embedding(content)
    embeddings.append(embedding)
    print(f"Generated embedding for: {content[:50]}...")

embeddings = np.array(embeddings)
np.save('datasets/openai_embeddings.npy', embeddings)

# Test query
query = "database optimization techniques"
query_embedding = get_openai_embedding(query)

# Calculate similarities
similarities = cosine_similarity([query_embedding], embeddings)[0]

df['similarity'] = similarities

# Show results
results = df.nlargest(3, 'similarity')[['title', 'category', 'similarity']]

print("\nOpenAI Embedding Results:")
print(results.to_string(index=False))

import openai
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Set OpenAI API client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_openai_embedding(text, model="text-embedding-ada-002"):
    """Generate embedding using OpenAI API"""
    text = text.replace("\n", " ")
    try:
        response = client.embeddings.create(
            input=[text],
            model=model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
datasets_dir = os.path.join(base_dir, 'datasets')

# Load dataset
df = pd.read_csv(os.path.join(datasets_dir, 'articles.csv'))

# Generate embeddings
embeddings = []
for content in df['content']:
    embedding = get_openai_embedding(content)
    embeddings.append(embedding)
    print(f"Generated embedding for: {content[:50]}...")

embeddings = np.array(embeddings)
np.save(os.path.join(datasets_dir, 'openai_embeddings.npy'), embeddings)

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

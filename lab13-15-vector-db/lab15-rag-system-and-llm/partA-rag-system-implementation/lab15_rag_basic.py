import pinecone
import openai
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import os
from dataclasses import dataclass

@dataclass
class RAGConfig:
    """Configuration for RAG system"""
    top_k: int = 3
    temperature: float = 0.7
    max_tokens: int = 500
    model: str = "gpt-3.5-turbo"

class RAGSystem:
    def __init__(self, config: RAGConfig = None):
        self.config = config or RAGConfig()
        
        # Initialize components
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize Pinecone
        pinecone.init(
            api_key=os.getenv('PINECONE_API_KEY'),
            environment='gcp-starter'
        )
        self.index = pinecone.Index("itd103-articles")
        
        # Initialize OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def retrieve(self, query: str) -> List[Dict]:
        """Retrieve relevant documents"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=self.config.top_k,
            include_metadata=True
        )
        
        # Format results
        documents = []
        for match in results['matches']:
            documents.append({
                'id': match['id'],
                'content': match['metadata']['content'],
                'title': match['metadata']['title'],
                'category': match['metadata']['category'],
                'score': match['score']
            })
        
        return documents
    
    def format_context(self, documents: List[Dict]) -> str:
        """Format retrieved documents as context"""
        context = "Relevant information:\n\n"
        
        for i, doc in enumerate(documents, 1):
            context += f"[Document {i}]: {doc['title']}\n"
            context += f"Category: {doc['category']}\n"
            context += f"Content: {doc['content']}\n\n"
        
        return context
    
    def generate(self, query: str, context: str) -> str:
        """Generate answer using LLM"""
        prompt = f"""You are a helpful assistant. Answer the question based on the provided context.
If the context doesn't contain relevant information, say "I cannot answer based on the provided information."

Context:
{context}

Question: {query}

Answer: """
        
        response = openai.ChatCompletion.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        return response.choices[0].message.content
    
    def answer(self, query: str) -> Dict:
        """Complete RAG pipeline"""
        # Step 1: Retrieve relevant documents
        print(f"Query: {query}")
        print("Retrieving relevant documents...")
        documents = self.retrieve(query)
        
        print(f"\nRetrieved {len(documents)} documents:")
        for doc in documents:
            print(f"  - {doc['title']} (Score: {doc['score']:.3f})")
        
        # Step 2: Format context
        context = self.format_context(documents)
        
        # Step 3: Generate answer
        print("\nGenerating answer...")
        answer = self.generate(query, context)
        
        return {
            'query': query,
            'documents': documents,
            'answer': answer,
            'context_length': len(context)
        }

# Initialize RAG system
config = RAGConfig(top_k=3, temperature=0.5, max_tokens=300)
rag = RAGSystem(config)

# Test queries
test_queries = [
    "What are the best practices for database optimization?",
    "How does artificial intelligence impact healthcare?",
    "What are some healthy eating habits?",
    "Compare SQL and NoSQL databases"
]

print("=== RAG System Test ===\n")

for query in test_queries:
    result = rag.answer(query)
    
    print(f"\n{'='*60}")
    print(f"QUERY: {result['query']}")
    print(f"{'='*60}")
    print(f"\nANSWER:\n{result['answer']}")
    print(f"\nContext used: {result['context_length']} characters")
    print(f"{'='*60}\n")

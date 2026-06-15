import os
import re
from typing import List, Dict, Tuple
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Import RAGSystem and RAGConfig from lab15_rag_basic
from lab15_rag_basic import RAGSystem, RAGConfig

class DocumentProcessor:
    """Process and chunk documents for better retrieval"""
    
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def chunk_document(self, text: str, metadata: Dict = None) -> List[Dict]:
        """Split document into chunks with metadata"""
        chunks = self.text_splitter.split_text(text)
        
        chunk_docs = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = metadata.copy() if metadata else {}
            chunk_metadata.update({
                'chunk_id': i,
                'chunk_total': len(chunks),
                'char_length': len(chunk),
                'word_count': len(chunk.split())
            })
            chunk_docs.append({
                'content': chunk,
                'metadata': chunk_metadata
            })
        
        return chunk_docs

class AdvancedRAGSystem(RAGSystem):
    """Extended RAG system with chunking and re-ranking"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processor = DocumentProcessor(chunk_size=400, chunk_overlap=50)
        self.encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    def calculate_relevance_score(self, query: str, document: str) -> float:
        """Calculate relevance score between query and document"""
        # Simple TF-IDF based scoring
        query_words = set(query.lower().split())
        doc_words = document.lower().split()
        
        if not query_words or not doc_words:
            return 0.0
        
        # Count matching words
        matches = sum(1 for word in query_words if word in doc_words)
        
        # Normalize by query length
        return matches / len(query_words)
    
    def rerank_documents(self, query: str, documents: List[Dict]) -> List[Dict]:
        """Re-rank documents based on relevance"""
        for doc in documents:
            relevance = self.calculate_relevance_score(query, doc['content'])
            doc['relevance_score'] = relevance
            doc['combined_score'] = 0.7 * doc['score'] + 0.3 * relevance
        
        # Sort by combined score
        return sorted(documents, key=lambda x: x['combined_score'], reverse=True)
    
    def smart_context_selection(self, query: str, documents: List[Dict], max_tokens: int = 2000) -> str:
        """Select context chunks intelligently within token limit"""
        selected_chunks = []
        total_tokens = 0
        
        for doc in documents:
            # Calculate tokens for this chunk
            chunk_tokens = len(self.encoder.encode(doc['content']))
            
            # Check if adding this chunk would exceed limit
            if total_tokens + chunk_tokens > max_tokens:
                break
            
            selected_chunks.append(doc)
            total_tokens += chunk_tokens
        
        # Format context
        context = "Relevant information from documents:\n\n"
        for i, chunk in enumerate(selected_chunks, 1):
            context += f"[Chunk {i} - Relevance: {chunk['combined_score']:.3f}]\n"
            context += f"Source: {chunk['title']}\n"
            context += f"Content: {chunk['content']}\n\n"
        
        return context, len(selected_chunks), total_tokens
    
    def answer_with_reranking(self, query: str) -> Dict:
        """Enhanced RAG pipeline with re-ranking"""
        print(f"Query: {query}")
        
        # Step 1: Initial retrieval
        print("1. Retrieving initial documents...")
        documents = self.retrieve(query)
        
        # Step 2: Chunk processing (if documents are too long)
        processed_docs = []
        for doc in documents:
            chunks = self.processor.chunk_document(
                doc['content'],
                {
                    'title': doc['title'],
                    'category': doc['category'],
                    'id': doc['id']
                }
            )
            processed_docs.extend(chunks)
        
        print(f"   Retrieved {len(documents)} documents, split into {len(processed_docs)} chunks")
        
        # Step 3: Re-ranking
        print("2. Re-ranking documents...")
        reranked = self.rerank_documents(query, processed_docs)
        
        print(f"   Top 3 chunks after re-ranking:")
        for i, doc in enumerate(reranked[:3], 1):
            print(f"   {i}. {doc['metadata']['title']} "
                  f"(Vector: {doc['score']:.3f}, "
                  f"Relevance: {doc['relevance_score']:.3f}, "
                  f"Combined: {doc['combined_score']:.3f})")
        
        # Step 4: Smart context selection
        print("3. Selecting context chunks...")
        context, num_chunks, total_tokens = self.smart_context_selection(
            query, reranked, max_tokens=1500
        )
        
        print(f"   Selected {num_chunks} chunks ({total_tokens} tokens)")
        
        # Step 5: Generate answer
        print("4. Generating answer...")
        answer = self.generate(query, context)
        
        return {
            'query': query,
            'original_documents': len(documents),
            'chunks_processed': len(processed_docs),
            'chunks_selected': num_chunks,
            'tokens_used': total_tokens,
            'answer': answer,
            'top_chunks': reranked[:3]
        }

# Test advanced RAG
if __name__ == "__main__":
    print("=== Advanced RAG System Test ===\n")

    advanced_config = RAGConfig(
        top_k=5,
        temperature=0.3,
        max_tokens=400,
        model="gpt-3.5-turbo"
    )

    advanced_rag = AdvancedRAGSystem(advanced_config)

    complex_queries = [
        "Explain the differences between SQL and NoSQL databases and when to use each",
        "Describe how artificial intelligence can be applied in healthcare and what are the challenges",
        "What are the main causes of climate change and what solutions are being implemented?"
    ]

    for query in complex_queries:
        print(f"\n{'#'*80}")
        print(f"Processing: {query}")
        print(f"{'#'*80}")
        
        result = advanced_rag.answer_with_reranking(query)
        
        print(f"\nANSWER:\n{result['answer']}")
        print(f"\nStatistics:")
        print(f"  - Original documents: {result['original_documents']}")
        print(f"  - Chunks processed: {result['chunks_processed']}")
        print(f"  - Chunks selected: {result['chunks_selected']}")
        print(f"  - Tokens used: {result['tokens_used']}")
        
        print(f"\nTop chunks used:")
        for i, chunk in enumerate(result['top_chunks'], 1):
            print(f"  {i}. {chunk['metadata']['title']} "
                  f"(Score: {chunk['combined_score']:.3f})")

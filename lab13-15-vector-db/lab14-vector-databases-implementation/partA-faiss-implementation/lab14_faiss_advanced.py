import faiss
import numpy as np
import pandas as pd
import time
from sentence_transformers import SentenceTransformer

# Load data and model
df = pd.read_csv('../../datasets/articles.csv')
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['content'].tolist()).astype('float32')

# Create different index types
dimension = embeddings.shape[1]

# 1. HNSW Index (Hierarchical Navigable Small World)
index_hnsw = faiss.IndexHNSWFlat(dimension, 32)  # 32 connections per node
index_hnsw.hnsw.efConstruction = 40  # Construction time/accuracy trade-off
index_hnsw.hnsw.efSearch = 16       # Search time/accuracy trade-off
index_hnsw.add(embeddings)
faiss.write_index(index_hnsw, "../../datasets/faiss_hnsw.index")

# 2. Product Quantization Index (for memory efficiency)
nlist = 5
m = 8  # Number of subquantizers (must divide dimension)
quantizer = faiss.IndexFlatL2(dimension)
index_pq = faiss.IndexIVFPQ(quantizer, dimension, nlist, m, 3)  # 3 bits per quantizer
index_pq.train(embeddings)
index_pq.add(embeddings)
faiss.write_index(index_pq, "../../datasets/faiss_pq.index")

# Performance comparison
def benchmark_index(query, index, name):
    """Benchmark search performance"""
    query_embedding = model.encode([query]).astype('float32')
    
    # Warm up
    for _ in range(10):
        index.search(query_embedding, 3)
    
    # Benchmark
    times = []
    for _ in range(100):
        start = time.perf_counter()
        index.search(query_embedding, 3)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms
    
    avg_time = np.mean(times)
    std_time = np.std(times)
    
    # Memory usage
    if hasattr(index, 'ntotal'):
        n_vectors = index.ntotal
    else:
        n_vectors = "N/A"
    
    return {
        'index': name,
        'avg_time_ms': avg_time,
        'std_time_ms': std_time,
        'vectors': n_vectors,
        'dimension': dimension
    }

# Load all indexes
indexes = {
    'Flat': faiss.read_index("../../datasets/faiss_flat.index"),
    'IVF': faiss.read_index("../../datasets/faiss_ivf.index"),
    'HNSW': faiss.read_index("../../datasets/faiss_hnsw.index"),
    'PQ': faiss.read_index("../../datasets/faiss_pq.index")
}

# Run benchmarks
query = "database performance optimization"
results = []

for name, index in indexes.items():
    print(f"Benchmarking {name} index...")
    stats = benchmark_index(query, index, name)
    results.append(stats)

# Display results
print("\n=== Performance Benchmark Results ===")
print("{:<10} {:<12} {:<12} {:<10} {:<10}".format(
    "Index", "Avg Time(ms)", "Std Dev(ms)", "Vectors", "Dimension"
))
print("-" * 60)
for res in results:
    print("{:<10} {:<12.4f} {:<12.4f} {:<10} {:<10}".format(
        res['index'],
        res['avg_time_ms'],
        res['std_time_ms'],
        res['vectors'],
        res['dimension']
    ))

# Accuracy comparison
def compare_accuracy(query, indexes, ground_truth_idx):
    """Compare accuracy against ground truth (flat index)"""
    query_embedding = model.encode([query]).astype('float32')
    
    # Get ground truth from flat index
    _, ground_truth = indexes['Flat'].search(query_embedding, 10)
    ground_truth = ground_truth[0]
    
    accuracy_results = {}
    for name, index in indexes.items():
        if name != 'Flat':
            _, results = index.search(query_embedding, 10)
            results = results[0]
            
            # Calculate overlap with ground truth
            overlap = len(set(results) & set(ground_truth))
            accuracy = overlap / len(ground_truth)
            
            accuracy_results[name] = {
                'accuracy': accuracy,
                'results': results,
                'overlap': overlap
            }
    
    return accuracy_results

# Test accuracy
print("\n=== Accuracy Comparison ===")
accuracy_results = compare_accuracy(query, indexes, indexes['Flat'])
for name, res in accuracy_results.items():
    print(f"{name}: Accuracy = {res['accuracy']:.2%} "
          f"({res['overlap']}/10 overlap with ground truth)")

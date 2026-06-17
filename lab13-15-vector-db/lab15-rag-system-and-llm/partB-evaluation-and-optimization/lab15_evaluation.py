import numpy as np
from typing import List, Dict
import json

# Import RAGSystem and RAGConfig for evaluation
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../partA-rag-system-implementation')))
from lab15_rag_basic import RAGSystem, RAGConfig

class RAGEvaluator:
    """Evaluate RAG system performance"""
    
    def __init__(self, test_dataset_path: str = None):
        if test_dataset_path:
            with open(test_dataset_path, 'r') as f:
                self.test_data = json.load(f)
        else:
            self.test_data = self.create_test_dataset()
    
    def create_test_dataset(self) -> List[Dict]:
        """Create a test dataset for evaluation"""
        return [
            {
                "id": 1,
                "query": "What are NoSQL databases?",
                "expected_answer_contains": ["MongoDB", "document", "schema", "scalable"],
                "expected_category": "Database"
            },
            {
                "id": 2,
                "query": "How does AI help in healthcare?",
                "expected_answer_contains": ["diagnosis", "treatment", "analysis", "prediction"],
                "expected_category": "Technology"
            },
            {
                "id": 3,
                "query": "What is GraphQL?",
                "expected_answer_contains": ["API", "query", "schema", "REST"],
                "expected_category": "API"
            },
            {
                "id": 4,
                "query": "Benefits of healthy eating",
                "expected_answer_contains": ["nutrition", "energy", "prevention", "well-being"],
                "expected_category": "Health"
            }
        ]
    
    def evaluate_retrieval(self, retrieved_docs: List[Dict], expected_category: str) -> Dict:
        """Evaluate retrieval performance"""
        metrics = {
            'precision': 0,
            'recall': 0,
            'f1_score': 0,
            'category_match': 0,
            'avg_score': 0
        }
        
        if not retrieved_docs:
            return metrics
        
        # Calculate scores
        scores = [doc['score'] for doc in retrieved_docs]
        metrics['avg_score'] = np.mean(scores)
        
        # Check category matches
        category_matches = sum(1 for doc in retrieved_docs 
                              if doc['category'].lower() == expected_category.lower())
        metrics['category_match'] = category_matches / len(retrieved_docs)
        
        # Calculate precision (assuming we want at least 1 relevant doc in top 3)
        relevant_in_top = any(doc['category'].lower() == expected_category.lower() 
                             for doc in retrieved_docs[:3])
        metrics['precision'] = 1.0 if relevant_in_top else 0.0
        
        # For recall, we'd need ground truth of all relevant docs
        # Simplified version
        metrics['recall'] = min(category_matches / 3, 1.0)  # Assume max 3 relevant
        
        # Calculate F1
        if metrics['precision'] + metrics['recall'] > 0:
            metrics['f1_score'] = (2 * metrics['precision'] * metrics['recall'] / 
                                  (metrics['precision'] + metrics['recall']))
        
        return metrics
    
    def evaluate_generation(self, generated_answer: str, expected_keywords: List[str]) -> Dict:
        """Evaluate answer quality"""
        metrics = {
            'keyword_coverage': 0,
            'answer_length': len(generated_answer),
            'has_refusal': False
        }
        
        # Check for refusal phrases
        refusal_phrases = [
            "cannot answer", "don't know", "no information",
            "not provided", "unable to"
        ]
        metrics['has_refusal'] = any(phrase in generated_answer.lower() 
                                    for phrase in refusal_phrases)
        
        # Check keyword coverage
        if expected_keywords:
            answer_lower = generated_answer.lower()
            found_keywords = sum(1 for keyword in expected_keywords 
                                if keyword.lower() in answer_lower)
            metrics['keyword_coverage'] = found_keywords / len(expected_keywords)
        
        return metrics
    
    def evaluate_system(self, rag_system, test_cases: int = None) -> Dict:
        """Complete system evaluation"""
        if test_cases:
            test_data = self.test_data[:test_cases]
        else:
            test_data = self.test_data
        
        overall_metrics = {
            'retrieval': {
                'avg_precision': [],
                'avg_recall': [],
                'avg_f1': [],
                'avg_category_match': [],
                'avg_score': []
            },
            'generation': {
                'avg_keyword_coverage': [],
                'avg_answer_length': [],
                'refusal_rate': 0
            },
            'latency': []
        }
        
        total_refusals = 0
        
        for test_case in test_data:
            print(f"\nEvaluating Test Case {test_case['id']}: {test_case['query']}")
            
            # Measure latency
            import time
            start_time = time.time()
            
            # Get RAG result
            result = rag_system.answer(test_case['query'])
            
            latency = time.time() - start_time
            overall_metrics['latency'].append(latency)
            
            # Evaluate retrieval
            retrieval_metrics = self.evaluate_retrieval(
                result['documents'],
                test_case.get('expected_category', '')
            )
            
            # Store retrieval metrics
            for key in retrieval_metrics:
                target_key = f'avg_{key}' if not key.startswith('avg_') else key
                # Wait, f1_score becomes avg_f1_score, but the dict has avg_f1
                if target_key == 'avg_f1_score': target_key = 'avg_f1'
                if target_key in overall_metrics['retrieval']:
                    overall_metrics['retrieval'][target_key].append(retrieval_metrics[key])
            
            # Evaluate generation
            generation_metrics = self.evaluate_generation(
                result['answer'],
                test_case.get('expected_answer_contains', [])
            )
            
            # Store generation metrics
            overall_metrics['generation']['avg_keyword_coverage'].append(
                generation_metrics['keyword_coverage']
            )
            overall_metrics['generation']['avg_answer_length'].append(
                generation_metrics['answer_length']
            )
            
            if generation_metrics['has_refusal']:
                total_refusals += 1
            
            print(f"  Retrieval Precision: {retrieval_metrics['precision']:.3f}")
            print(f"  Keyword Coverage: {generation_metrics['keyword_coverage']:.3f}")
            print(f"  Latency: {latency:.2f}s")
        
        # Calculate averages
        for category in ['retrieval', 'generation']:
            for metric in list(overall_metrics[category].keys()):
                if metric.startswith('avg_'):
                    values = overall_metrics[category][metric]
                    if values:
                        base_name = metric[4:]  # Remove 'avg_' prefix
                        overall_metrics[category][base_name] = np.mean(values)
        
        overall_metrics['generation']['refusal_rate'] = total_refusals / len(test_data)
        overall_metrics['latency_avg'] = np.mean(overall_metrics['latency'])
        overall_metrics['latency_std'] = np.std(overall_metrics['latency'])
        
        # Clean up arrays, keep only averages
        for category in ['retrieval', 'generation']:
            keys_to_remove = [k for k in overall_metrics[category] if k.startswith('avg_')]
            for key in keys_to_remove:
                del overall_metrics[category][key]
        
        return overall_metrics

if __name__ == "__main__":
    # Run evaluation
    print("=== RAG System Evaluation ===\n")
    
    # Initialize basic RAG system
    config = RAGConfig(top_k=3, temperature=0.3, max_tokens=200)
    rag = RAGSystem(config)
    
    # Initialize evaluator
    evaluator = RAGEvaluator()
    # Run evaluation
    results = evaluator.evaluate_system(rag, test_cases=3)
    
    print(f"\n{'='*60}")
    print("EVALUATION RESULTS SUMMARY")
    print(f"{'='*60}")
    print("\nRetrieval Performance:")
    print(f"  Precision: {results['retrieval'].get('precision', 0):.3f}")
    print(f"  Recall: {results['retrieval'].get('recall', 0):.3f}")
    print(f"  F1 Score: {results['retrieval'].get('f1_score', results['retrieval'].get('f1', 0)):.3f}")
    print(f"  Category Match Rate: {results['retrieval'].get('category_match', 0):.3f}")
    print(f"  Average Score: {results['retrieval'].get('avg_score', results['retrieval'].get('score', 0)):.3f}")
    
    print("\nGeneration Performance:")
    print(f"  Keyword Coverage: {results['generation'].get('keyword_coverage', 0):.3f}")
    print(f"  Average Answer Length: {results['generation'].get('avg_answer_length', results['generation'].get('answer_length', 0)):.0f} chars")
    print(f"  Refusal Rate: {results['generation'].get('refusal_rate', 0):.3f}")
    
    print("\nSystem Performance:")
    print(f"  Average Latency: {results['latency_avg']:.2f}s")
    print(f"  Latency Std Dev: {results['latency_std']:.2f}s")
    
    # Calculate overall score
    overall_score = (
        0.4 * results['retrieval'].get('f1_score', results['retrieval'].get('f1', 0)) +
        0.4 * results['generation'].get('keyword_coverage', 0) +
        0.2 * (1.0 - results['generation'].get('refusal_rate', 0)) +
        0.1 * (1 / (1 + results['latency_avg']))  # Inverse of latency
    )
    
    print(f"\nOverall System Score: {overall_score:.3f}/1.0")
    
    if overall_score > 0.8:
        print("Rating: EXCELLENT")
    elif overall_score > 0.6:
        print("Rating: GOOD")
    elif overall_score > 0.4:
        print("Rating: FAIR")
    else:
        print("Rating: NEEDS IMPROVEMENT")

from pymongo import MongoClient
import pymongo
import time
import pandas as pd
import matplotlib.pyplot as plt

class QueryOptimizer:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.query_optimization
    
    def setup_test_data(self):
        """Create test dataset with various distributions"""
        self.db.orders.drop()
        self.db.products.drop()
        self.db.customers.drop()
        
        # Create products collection
        products = []
        for i in range(1000):
            products.append({
                "_id": i,
                "name": f"Product_{i}",
                "category": f"Category_{i % 10}",
                "price": 10 + (i % 100),
                "stock": 1000 - (i % 500),
                "popularity": i % 1000
            })
        self.db.products.insert_many(products)
        
        # Create customers collection
        customers = []
        for i in range(10000):
            customers.append({
                "_id": i,
                "name": f"Customer_{i}",
                "city": f"City_{i % 20}",
                "segment": ["Premium", "Standard", "Basic"][i % 3],
                "join_date": pd.Timestamp("2023-01-01") + pd.Timedelta(days=i % 365)
            })
        self.db.customers.insert_many(customers)
        
        # Create orders collection (largest)
        orders = []
        for i in range(100000):
            orders.append({
                "_id": i,
                "customer_id": i % 10000,
                "product_id": i % 1000,
                "quantity": 1 + (i % 10),
                "price": 10 + (i % 100),
                "order_date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=i % 365),
                "status": ["pending", "completed", "shipped", "cancelled"][i % 4],
                "payment_method": ["credit", "debit", "paypal", "cash"][i % 4]
            })
        self.db.orders.insert_many(orders)
        
        print(f"Created collections:")
        print(f"  products: {self.db.products.count_documents({})}")
        print(f"  customers: {self.db.customers.count_documents({})}")
        print(f"  orders: {self.db.orders.count_documents({})}")
        
    def analyze_query_plan(self):
        print("\n=== Unoptimized Query Plan Analysis ===")
        # Unoptimized query
        explanation = self.db.orders.find(
            {"status": "completed", "payment_method": "credit"}
        ).explain("executionStats")
        
        stats = explanation["executionStats"]
        print(f"Total Docs Examined: {stats['totalDocsExamined']}")
        print(f"Execution Time: {stats['executionTimeMillis']} ms")
        
    def optimize_query(self):
        print("\n=== Optimized Query Plan Analysis ===")
        # Create index
        self.db.orders.create_index([("status", pymongo.ASCENDING), ("payment_method", pymongo.ASCENDING)])
        
        explanation = self.db.orders.find(
            {"status": "completed", "payment_method": "credit"}
        ).explain("executionStats")
        
        stats = explanation["executionStats"]
        print(f"Total Docs Examined: {stats['totalDocsExamined']}")
        print(f"Execution Time: {stats['executionTimeMillis']} ms")

if __name__ == "__main__":
    optimizer = QueryOptimizer()
    print("Setting up database...")
    optimizer.setup_test_data()
    optimizer.analyze_query_plan()
    optimizer.optimize_query()

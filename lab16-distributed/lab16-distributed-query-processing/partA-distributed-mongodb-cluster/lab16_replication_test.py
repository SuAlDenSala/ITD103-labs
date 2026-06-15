from pymongo import MongoClient
from pymongo.read_preferences import ReadPreference
import time
import threading

class ReplicationTester:
    def __init__(self):
        # Connect to replica set
        self.client = MongoClient(
            'mongodb://localhost:27017,localhost:27018,localhost:27019/',
            replicaSet='rs0',
            readPreference='secondaryPreferred'  # Read from secondary if available
        )
        
        self.db = self.client.test_replication
        self.collection = self.db.data
    
    def setup_data(self):
        """Insert test data"""
        self.collection.drop()
        
        # Insert 1000 documents
        documents = [
            {"_id": i, "value": f"data_{i}", "timestamp": time.time()}
            for i in range(1000)
        ]
        
        result = self.collection.insert_many(documents)
        print(f"Inserted {len(result.inserted_ids)} documents")
        
        # Verify replication
        self.verify_replication()
    
    def verify_replication(self):
        """Verify data is replicated across all nodes"""
        primary = self.client.primary
        secondaries = self.client.secondaries
        
        print(f"\nPrimary: {primary}")
        print(f"Secondaries: {secondaries}")
        
        # Check document count on each member
        for member in [primary] + list(secondaries):
            try:
                # Connect directly to member
                member_client = MongoClient(member[0], member[1])
                count = member_client.test_replication.data.count_documents({})
                print(f"Member {member}: {count} documents")
                member_client.close()
            except Exception as e:
                print(f"Error connecting to {member}: {e}")
    
    def test_read_preferences(self):
        """Test different read preferences"""
        print("\n=== Testing Read Preferences ===")
        
        # 1. Primary (default)
        print("\n1. Reading from PRIMARY:")
        start = time.time()
        cursor = self.collection.find().limit(5)
        for doc in cursor:
            print(f"  {doc['_id']}: {doc['value']}")
        print(f"  Time: {time.time() - start:.3f}s")
        
        # 2. Secondary Preferred
        print("\n2. Reading from SECONDARY_PREFERRED:")
        secondary_collection = self.db.get_collection(
            'data',
            read_preference=ReadPreference.SECONDARY_PREFERRED
        )
        start = time.time()
        cursor = secondary_collection.find().limit(5)
        for doc in cursor:
            print(f"  {doc['_id']}: {doc['value']}")
        print(f"  Time: {time.time() - start:.3f}s")
        
        # 3. Nearest (lowest latency)
        print("\n3. Reading from NEAREST:")
        nearest_collection = self.db.get_collection(
            'data',
            read_preference=ReadPreference.NEAREST
        )
        start = time.time()
        cursor = nearest_collection.find().limit(5)
        for doc in cursor:
            print(f"  {doc['_id']}: {doc['value']}")
        print(f"  Time: {time.time() - start:.3f}s")
    
    def test_write_concern(self):
        """Test different write concern levels"""
        print("\n=== Testing Write Concern ===")
        
        test_cases = [
            ("w=1 (Default)", {"w": 1}),
            ("w=majority", {"w": "majority"}),
            ("w=2", {"w": 2}),
            ("w=1, j=true", {"w": 1, "j": True}),
            ("w=majority, j=true", {"w": "majority", "j": True})
        ]
        
        for name, concern in test_cases:
            print(f"\n{name}:")
            start = time.time()
            try:
                result = self.collection.insert_one(
                    {"test": name, "timestamp": time.time()},
                    write_concern=concern
                )
                elapsed = time.time() - start
                print(f"  Inserted document {result.inserted_id}")
                print(f"  Time: {elapsed:.3f}s")
            except Exception as e:
                print(f"  Error: {e}")
    
    def test_failover(self):
        """Simulate failover"""
        print("\n=== Testing Failover ===")
        
        # Step down primary
        print("1. Stepping down primary...")
        try:
            self.client.admin.command("replSetStepDown", 30)  # Step down for 30 seconds
            time.sleep(5)  # Wait for election
        except Exception as e:
            print(f"  Step down resulted in error (expected): {e}")
        
        # Check new primary
        time.sleep(10)  # Wait for election to complete
        new_primary = self.client.primary
        print(f"2. New primary: {new_primary}")
        
        # Test writes during failover
        print("3. Testing write during failover...")
        start = time.time()
        try:
            result = self.collection.insert_one(
                {"failover_test": True, "timestamp": time.time()},
                write_concern={"w": "majority"}
            )
            elapsed = time.time() - start
            print(f"  Write succeeded after {elapsed:.3f}s")
            print(f"  Inserted document: {result.inserted_id}")
        except Exception as e:
            print(f"  Write failed: {e}")
        
        # Verify data consistency
        print("4. Verifying data consistency...")
        count = self.collection.count_documents({})
        print(f"  Total documents: {count}")
    
    def concurrent_read_write_test(self):
        """Test concurrent read and write operations"""
        print("\n=== Concurrent Read/Write Test ===")
        
        def writer(thread_id):
            for i in range(100):
                doc = {
                    "thread": thread_id,
                    "iteration": i,
                    "timestamp": time.time()
                }
                self.collection.insert_one(doc)
                time.sleep(0.01)  # Small delay
        
        def reader(thread_id):
            count = 0
            start = time.time()
            while time.time() - start < 5:  # Read for 5 seconds
                cursor = self.collection.find(
                    {"thread": thread_id}
                ).limit(10)
                list(cursor)  # Force query execution
                count += 1
                time.sleep(0.01)
            return count
        
        # Start writer threads
        writer_threads = []
        for i in range(3):
            t = threading.Thread(target=writer, args=(i,))
            writer_threads.append(t)
            t.start()
        
        # Start reader threads
        reader_threads = []
        reader_results = []
        for i in range(2):
            t = threading.Thread(target=reader, args=(i,))
            reader_threads.append(t)
            t.start()
        
        # Wait for completion
        for t in writer_threads:
            t.join()
        
        for t in reader_threads:
            t.join()
        
        # Check final state
        final_count = self.collection.count_documents({})
        print(f"Final document count: {final_count}")
        
        # Check for duplicates or missing data
        threads_data = {}
        for doc in self.collection.find():
            thread_id = doc.get("thread")
            if thread_id is not None:
                if thread_id not in threads_data:
                    threads_data[thread_id] = 0
                threads_data[thread_id] += 1
        
        print("Documents per thread:", threads_data)

# Run tests
if __name__ == "__main__":
    tester = ReplicationTester()
    
    print("Setting up test data...")
    tester.setup_data()
    
    tester.test_read_preferences()
    tester.test_write_concern()
    tester.test_failover()
    tester.concurrent_read_write_test()

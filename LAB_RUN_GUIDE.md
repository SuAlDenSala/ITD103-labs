# ITD103 Lab Execution & Screenshot Guide

This guide provides the exact terminal commands to run each lab step-by-step so you can easily take screenshots for your lab reports. 

> **Tip:** Open your terminal inside the `itd103-labs` root directory before starting!

---

## Labs 1-3: NoSQL Fundamentals (MongoDB)

**1. Start the Database**
```bash
cd lab1-3-nosql-fundamentals/lab1-understanding-cap-theorem
docker-compose up -d
```

**2. Lab 1: CAP Theorem & Basics**
```bash
cd partB-mongodb-installation
mongosh < lab1_basics.js
# 📸 [TAKE SCREENSHOT OF OUTPUT]
```

**3. Lab 2: Document Schema Design**
```bash
cd ../../lab2-document-database-design/partB-implementation
mongosh < lab2_schema_design.js
# 📸 [TAKE SCREENSHOT OF OUTPUT]
```

**4. Lab 3: Performance Comparison**
```bash
cd ../../lab3-nosql-performance-comparison/partA-performance-testing
mongosh < partA_performance.js
# 📸 [TAKE SCREENSHOT OF OUTPUT]

cd ../partB-indexing-and-optimization
mongosh < partB_indexing.js
# 📸 [TAKE SCREENSHOT OF OUTPUT]
```

**5. Clean up**
```bash
cd ../../lab1-understanding-cap-theorem
docker-compose down
cd ../..
```

---

## Labs 4-6: Advanced MongoDB

**1. Start the Database & Import Datasets**
```bash
cd lab4-6-mongodb/lab4-advanced-mql-queries
docker-compose up -d

# Import your JSON datasets
cd partA-import-dataset
bash lab4_import.sh
# 📸 [TAKE SCREENSHOT OF IMPORT SUCCESS]
cd ..
```

**2. Lab 4: Advanced MQL**
```bash
cd partB-complex-queries
mongosh < lab4_advanced_mql.js
# 📸 [TAKE SCREENSHOT]
```

**3. Lab 5: Aggregation**
```bash
cd ../../lab5-aggregation-framework/partA-import-sales-data
bash lab5_import.sh
# 📸 [TAKE SCREENSHOT OF IMPORT]

cd ../partB-aggregation-exercises
mongosh < lab5_aggregation.js
# 📸 [TAKE SCREENSHOT]
```

**4. Stop standalone MongoDB**
```bash
cd ../../lab4-advanced-mql-queries
docker-compose down
cd ../..
```

**5. Lab 6: Performance & Replication (Needs Replica Set)**
```bash
cd lab4-6-mongodb/lab6-mongodb-performance
docker-compose up -d   # Starts the 3-node cluster

mongosh < partA-replication-setup/lab6_replication.js
# 📸 [TAKE SCREENSHOT]

mongosh < partB-sharding-implementation/lab6_sharding.js
# 📸 [TAKE SCREENSHOT]

mongosh < partC-performance-monitoring/lab6_monitoring.js
# 📸 [TAKE SCREENSHOT]

docker-compose down
cd ../..
```

---

## Labs 7-9: Neo4j (Graph Database)

**1. Start the Graph Database & Verify Setup**
```bash
cd lab7-9-neo4j/lab7-neo4j-fundamentals
docker-compose up -d
# Wait ~15 seconds for Neo4j to fully boot up

cd partA-neo4j-setup
bash lab7_setup.sh
# 📸 [TAKE SCREENSHOT OF SETUP VERIFICATION]
cd ..
```

**2. Lab 7: Cypher Fundamentals**
```bash
cd partB-cypher-fundamentals
# Note: We use docker to execute the queries inside the Neo4j container
docker exec -i neo4j_server cypher-shell -u neo4j -p password < lab7_fundamentals.cypher
# 📸 [TAKE SCREENSHOT]
```

**3. Lab 8: Advanced Cypher**
```bash
# First, stop the Lab 7 database
cd ../../lab7-neo4j-fundamentals
docker-compose down

# Start the Lab 8 database
cd ../lab8-advanced-cypher
docker-compose up -d
# Wait ~15 seconds for Neo4j to fully boot up

# Part A: Load the Dataset
docker exec -i neo4j_server cypher-shell -u neo4j -p password < partA-load-dataset/lab8_load_dataset.cypher
# 📸 [TAKE SCREENSHOT OF LOADING]

# Part B & C: Run the Advanced Queries
docker exec -i neo4j_server cypher-shell -u neo4j -p password < partB-path-queries/lab8_advanced_queries.cypher
# 📸 [TAKE SCREENSHOT OF QUERIES]
```

**4. Lab 9: Real World Graph**
```bash
# Stop Lab 8 database
cd ../../lab8-advanced-cypher
docker-compose down

# Start Lab 9 database
cd ../lab9-real-world-graph
docker-compose up -d
# Wait ~15 seconds for Neo4j to fully boot up

# Part A: Build the Product Graph
docker exec -i neo4j_server cypher-shell -u neo4j -p password < partA-build-product-graph/lab9_build_graph.cypher
# 📸 [TAKE SCREENSHOT OF GRAPH BUILDING]

# Part B: Recommendation Queries
docker exec -i neo4j_server cypher-shell -u neo4j -p password < partB-recommendation-queries/lab9_graph_application.cypher
# 📸 [TAKE SCREENSHOT OF RECOMMENDATIONS]
```

**5. Clean up**
```bash
cd ../../lab9-real-world-graph
docker-compose down
cd ../..
```
```

---

## Labs 10-12: GraphQL

### Lab 10: GraphQL Server
*You will need TWO terminals for this to take good screenshots.*

**Terminal 1:**
```bash
# Part A: Environment Setup
cd lab10-12-graphql/lab10-graphql-fundamentals/partA-environment-setup
bash check_env.sh
# 📸 [TAKE SCREENSHOT OF ENVIRONMENT CHECK]

# Part B: Basic GraphQL Server
cd ../partB-basic-graphql-server
npm install
node server.js
# 📸 [TAKE SCREENSHOT OF SERVER RUNNING]
```

**Terminal 2:**
```bash
# Part C: Testing GraphQL API
cd lab10-12-graphql/lab10-graphql-fundamentals/partC-testing-graphql-api
bash test_query.sh
# 📸 [TAKE SCREENSHOT OF JSON RESPONSE]
```
*(Press `Ctrl+C` in Terminal 1 to stop the server).*

### Lab 11: Advanced GraphQL

**Terminal 1:**
```bash
# Part A: Nested Resolvers (Start Server)
cd lab10-12-graphql/lab11-advanced-graphql/partA-nested-resolvers
npm install
node server.js
# 📸 [TAKE SCREENSHOT OF ADVANCED SERVER RUNNING]
```

**Terminal 2:**
```bash
# Part B: Authentication
cd lab10-12-graphql/lab11-advanced-graphql/partB-authentication
bash test_auth.sh
# 📸 [TAKE SCREENSHOT OF AUTHENTICATION TEST]

# Part C: Nested Queries
cd ../partC-subscriptions
bash test_nested.sh
# 📸 [TAKE SCREENSHOT OF NESTED DATA FETCH]
```
*(Press `Ctrl+C` in Terminal 1 to stop the server).*

### Lab 12: Microservices Federation
```bash
cd lab10-12-graphql/lab12-graphql-multiple-sources
docker-compose up -d
# Wait a few seconds for all 3 microservices (books, users, gateway) to boot up

# Query the unified Gateway API
curl -X POST -H "Content-Type: application/json" -d '{"query":"{ users { name borrowedBooks { title } } }"}' http://localhost:4000/
# 📸 [TAKE SCREENSHOT OF THE UNIFIED MICROSERVICES]

docker-compose down
cd ../..
```

---

## Labs 13-15: Vector Databases & AI RAG Systems

**Lab 13: Vector Embeddings**
```bash
# This generates 5-dimensional vectors and compares them using Cosine Similarity
cd lab13-15-vector-db/lab13-vector-embeddings/partB-cosine-similarity
node cosine.js
# 📸 [TAKE SCREENSHOT OF COSINE SIMILARITY RESULTS]
```

**Lab 14: Vector Database Implementation**
```bash
# This builds an in-memory vector DB and searches it
cd ../../lab14-vector-databases-implementation/partB-search
node vectordb.js
# 📸 [TAKE SCREENSHOT OF DATABASE SEARCH]
```

**Lab 15: AI RAG System (Retrieval-Augmented Generation)**
```bash
# This retrieves context from the Vector DB and feeds it to a mock LLM
cd ../../lab15-rag-system-and-llm/partB-generation
node rag.js
# 📸 [TAKE SCREENSHOT OF LLM GENERATION]
```

---

## Lab 16: Distributed Query Processing

**1. Start the Cluster**
```bash
cd lab16-distributed/lab16-distributed-query-processing
docker-compose up -d
# Wait for the replica set nodes to communicate
```

**2. Test Replication**
```bash
cd partA-distributed-mongodb-cluster
python3 lab16_replication_test.py
# 📸 [TAKE SCREENSHOT]
```

**3. Test Query Optimization**
```bash
cd ../partB-distributed-query-optimization
python3 lab16_query_optimization.py
# 📸 [TAKE SCREENSHOT]
```

**4. Final Cleanup**
```bash
cd ..
docker-compose down
```

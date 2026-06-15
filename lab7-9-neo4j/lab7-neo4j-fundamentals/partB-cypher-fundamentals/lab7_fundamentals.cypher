// Create person nodes
CREATE (alice:Person {name: 'Alice', age: 30, city: 'Manila'});
CREATE (bob:Person {name: 'Bob', age: 25, city: 'Cebu'});
CREATE (charlie:Person {name: 'Charlie', age: 35, city: 'Davao'});

// Create multiple nodes with properties
CREATE 
  (database:Technology {name: 'Database', type: 'Backend'}),
  (frontend:Technology {name: 'Frontend', type: 'Development'}),
  (ai:Technology {name: 'AI', type: 'Emerging'});

// Create KNOWS relationships
MATCH (a:Person {name: 'Alice'})
MATCH (b:Person {name: 'Bob'})
CREATE (a)-[:KNOWS {since: 2020}]->(b);

// Create multiple relationships
MATCH (alice:Person {name: 'Alice'})
MATCH (charlie:Person {name: 'Charlie'})
CREATE (alice)-[:WORKS_WITH {project: 'Database Migration'}]->(charlie);

// Create LIKES relationships with properties
MATCH (p:Person)
MATCH (t:Technology)
WHERE p.name IN ['Alice', 'Bob'] AND t.name IN ['Database', 'AI']
CREATE (p)-[:LIKES {score: 8.5, interest: 'Professional'}]->(t);

// Basic Queries
MATCH (p:Person) RETURN p;
MATCH (p:Person {city: 'Manila'}) RETURN p.name, p.age;
MATCH (p1:Person)-[r:KNOWS]->(p2:Person) RETURN p1.name, r.since, p2.name;
MATCH (p:Person)-[:LIKES]->(t:Technology {name: 'Database'}) RETURN p.name, p.city;
MATCH (n) RETURN labels(n)[0] as Label, count(*) as Count;

// Updating Data
MATCH (p:Person {name: 'Alice'}) SET p.age = 31, p.skills = ['MongoDB', 'Neo4j'];
MATCH (p:Person) SET p.updated_at = timestamp();
MATCH (p:Person {name: 'Bob'}) REMOVE p.age;
MATCH (p:Person {name: 'Charlie'})-[r]-() DELETE r, p;

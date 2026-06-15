// Collaborative Filtering
MATCH (target:Product {name: 'Laptop'})<-[:PURCHASED]-(customer:Customer)-[:PURCHASED]->(other:Product) WHERE target <> other RETURN other.name as RecommendedProduct, count(customer) as CustomerCount, sum( CASE WHEN customer.segment = 'Premium' THEN 2 ELSE 1 END ) as WeightedScore ORDER BY WeightedScore DESC;

MATCH (me:Customer {name: 'Alice'})-[:PURCHASED]->(myProduct:Product) MATCH (other:Customer)-[:PURCHASED]->(myProduct) WHERE me <> other WITH other, count(myProduct) as CommonProducts MATCH (other)-[:PURCHASED]->(theirProduct:Product) WHERE NOT EXISTS { MATCH (me)-[:PURCHASED]->(theirProduct) } RETURN other.name as SimilarCustomer, collect(theirProduct.name) as RecommendedProducts, CommonProducts as SimilarityScore ORDER BY SimilarityScore DESC;

// Content-Based
MATCH (target:Product {name: 'Laptop'}) MATCH (similar:Product {category: target.category}) WHERE target <> similar RETURN similar.name as SimilarProduct, similar.price, abs(target.price - similar.price) as PriceDifference ORDER BY PriceDifference;

MATCH (c:Customer {name: 'Charlie'})-[:VIEWED]->(v:Product) WHERE NOT EXISTS { (c)-[:PURCHASED]->(v) } RETURN v.name as ViewedNotPurchased, v.category, v.price;

MATCH (c:Customer {name: 'Alice'})-[:PURCHASED]->(p:Product) MATCH (p)-[:BOUGHT_WITH]->(recommended:Product) WHERE NOT EXISTS { (c)-[:PURCHASED]->(recommended) } RETURN recommended.name as CrossSell, recommended.category, max(p.name) as OriginallyBoughtWith, sum(p.frequency) as PopularityScore ORDER BY PopularityScore DESC;

// Fraud Detection
CREATE
  (cust1:Customer {id: 201, name: 'User1', signup_date: '2024-01-01'}),
  (cust2:Customer {id: 202, name: 'User2', signup_date: '2024-01-02'}),
  (cust3:Customer {id: 203, name: 'User3', signup_date: '2024-01-03'}),
  (cust1)-[:SHARES_IP {timestamp: '2024-01-15'}]->(cust2),
  (cust1)-[:SHARES_PHONE {timestamp: '2024-01-16'}]->(cust3),
  (cust2)-[:SHARES_ADDRESS]->(cust3),
  (cust1)-[:PURCHASED {amount: 999.99, timestamp: '2024-01-15 10:00'}]->(:Product),
  (cust1)-[:PURCHASED {amount: 899.99, timestamp: '2024-01-15 10:05'}]->(:Product),
  (cust1)-[:PURCHASED {amount: 799.99, timestamp: '2024-01-15 10:10'}]->(:Product),
  (cust2)-[:PURCHASED {amount: 500.00, timestamp: '2024-01-15 10:02'}]->(:Product);

MATCH (c1:Customer)-[r1:SHARES_IP|SHARES_PHONE|SHARES_ADDRESS]-(c2:Customer) WITH c1, c2, count(r1) as SharedAttributes WHERE SharedAttributes >= 2 MATCH (c1)-[p1:PURCHASED]->() MATCH (c2)-[p2:PURCHASED]->() WITH c1, c2, SharedAttributes, count(p1) as c1Purchases, count(p2) as c2Purchases, collect(p1.timestamp)[0] as firstPurchaseTime WHERE c1Purchases > 2 OR c2Purchases > 2 RETURN c1.name as Customer1, c2.name as Customer2, SharedAttributes as SuspiciousLinks, c1Purchases + c2Purchases as TotalRapidPurchases, 'Possible Fraud Ring' as Alert;

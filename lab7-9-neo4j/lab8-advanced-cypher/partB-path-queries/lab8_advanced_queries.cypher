// Path Finding
MATCH path = (alice:Person {name: 'Alice'})-[:FRIENDS_WITH*]-(frank:Person {name: 'Frank'}) RETURN path;
MATCH path = shortestPath((alice:Person {name: 'Alice'})-[:FRIENDS_WITH*]-(frank:Person {name: 'Frank'})) RETURN path, length(path) as degrees;
MATCH path = (alice:Person {name: 'Alice'})-[:FRIENDS_WITH*1..3]-(other:Person) WHERE other.name <> 'Alice' RETURN other.name, length(path) as distance ORDER BY distance;

// Variable Length
MATCH (me:Person {name: 'Alice'})-[:FRIENDS_WITH*2]-(friend_of_friend:Person) WHERE NOT (me)-[:FRIENDS_WITH]-(friend_of_friend) RETURN DISTINCT friend_of_friend.name as SuggestedFriend;
MATCH (a:Person {name: 'Alice'})-[:FRIENDS_WITH]-(mutual)-[:FRIENDS_WITH]-(b:Person {name: 'Frank'}) RETURN mutual.name as MutualFriend;
MATCH (p1:Person {name: 'Alice'})-[:INTERESTED_IN]->(i:Interest)<-[:INTERESTED_IN]-(p2:Person) WHERE p1 <> p2 RETURN p2.name as Person, collect(i.name) as CommonInterests;

// Algorithms
MATCH (p:Person) RETURN p.name, COUNT { (p)-[:FRIENDS_WITH]-() } as degree, COUNT { (p)-[:FRIENDS_WITH]->() } as out_degree, COUNT { (p)<-[:FRIENDS_WITH]-() } as in_degree ORDER BY degree DESC;

MATCH (p:Person) WITH p MATCH path = allShortestPaths((start:Person)-[:FRIENDS_WITH*]-(end:Person)) WHERE start <> end AND p IN nodes(path) RETURN p.name, count(*) as betweenness ORDER BY betweenness DESC;

MATCH (p:Person) WITH p MATCH component = (p)-[:FRIENDS_WITH*]-(other:Person) RETURN p.name as Person, count(DISTINCT other) as ComponentSize ORDER BY ComponentSize DESC;

MATCH (a:Person)-[:FRIENDS_WITH]-(b:Person), (b:Person)-[:FRIENDS_WITH]-(c:Person), (c:Person)-[:FRIENDS_WITH]-(a:Person) WHERE id(a) < id(b) AND id(b) < id(c) RETURN a.name, b.name, c.name;

// Recommendation
MATCH (me:Person {name: 'Alice'})-[:FRIENDS_WITH]-(friend)-[:FRIENDS_WITH]-(potential) WHERE NOT (me)-[:FRIENDS_WITH]-(potential) AND me <> potential RETURN potential.name as RecommendedFriend, count(friend) as MutualFriends ORDER BY MutualFriends DESC;

MATCH (me:Person {name: 'Alice'})-[:INTERESTED_IN]->(myInterest:Interest) MATCH (other:Person)-[:INTERESTED_IN]->(myInterest) WHERE me <> other WITH other, count(myInterest) as CommonInterests MATCH (other)-[:INTERESTED_IN]->(otherInterest:Interest) WHERE NOT EXISTS { MATCH (me)-[:INTERESTED_IN]->(otherInterest) } RETURN other.name as Person, collect(otherInterest.name) as SuggestedInterests, CommonInterests ORDER BY CommonInterests DESC;

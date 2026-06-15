CREATE 
  (alice:Person {id: 1, name: 'Alice', age: 30}),
  (bob:Person {id: 2, name: 'Bob', age: 25}),
  (charlie:Person {id: 3, name: 'Charlie', age: 35}),
  (diana:Person {id: 4, name: 'Diana', age: 28}),
  (eve:Person {id: 5, name: 'Eve', age: 32}),
  (frank:Person {id: 6, name: 'Frank', age: 40}),
  
  (alice)-[:FRIENDS_WITH {since: 2020}]->(bob),
  (alice)-[:FRIENDS_WITH {since: 2021}]->(charlie),
  (bob)-[:FRIENDS_WITH {since: 2019}]->(diana),
  (charlie)-[:FRIENDS_WITH {since: 2022}]->(eve),
  (diana)-[:FRIENDS_WITH {since: 2020}]->(eve),
  (eve)-[:FRIENDS_WITH {since: 2023}]->(frank),
  (bob)-[:FRIENDS_WITH {since: 2021}]->(eve),
  
  (db:Interest {name: 'Databases'}),
  (ai:Interest {name: 'AI'}),
  (web:Interest {name: 'Web Development'}),
  (mobile:Interest {name: 'Mobile Development'}),
  
  (alice)-[:INTERESTED_IN {level: 'High'}]->(db),
  (alice)-[:INTERESTED_IN {level: 'Medium'}]->(ai),
  (bob)-[:INTERESTED_IN {level: 'High'}]->(web),
  (charlie)-[:INTERESTED_IN {level: 'High'}]->(db),
  (diana)-[:INTERESTED_IN {level: 'Medium'}]->(mobile),
  (eve)-[:INTERESTED_IN {level: 'High'}]->(ai),
  (frank)-[:INTERESTED_IN {level: 'Medium'}]->(web)

-- Path Finding
MATCH path = (alice:Person {name: 'Alice'})-[:FRIENDS_WITH*]-(frank:Person {name: 'Frank'}) RETURN path
MATCH path = shortestPath((alice:Person {name: 'Alice'})-[:FRIENDS_WITH*]-(frank:Person {name: 'Frank'})) RETURN path, length(path) as degrees
MATCH path = (alice:Person {name: 'Alice'})-[:FRIENDS_WITH*1..3]-(other:Person) WHERE other.name <> 'Alice' RETURN other.name, length(path) as distance ORDER BY distance

-- Variable Length
MATCH (me:Person {name: 'Alice'})-[:FRIENDS_WITH*2]-(friend_of_friend:Person) WHERE NOT (me)-[:FRIENDS_WITH]-(friend_of_friend) RETURN DISTINCT friend_of_friend.name as SuggestedFriend
MATCH (a:Person {name: 'Alice'})-[:FRIENDS_WITH]-(mutual)-[:FRIENDS_WITH]-(b:Person {name: 'Frank'}) RETURN mutual.name as MutualFriend
MATCH (p1:Person {name: 'Alice'})-[:INTERESTED_IN]->(i:Interest)<-[:INTERESTED_IN]-(p2:Person) WHERE p1 <> p2 RETURN p2.name as Person, collect(i.name) as CommonInterests

-- Algorithms
MATCH (p:Person) RETURN p.name, size((p)-[:FRIENDS_WITH]-()) as degree, size((p)-[:FRIENDS_WITH]->()) as out_degree, size((p)<-[:FRIENDS_WITH]-()) as in_degree ORDER BY degree DESC

MATCH (p:Person) WITH p MATCH path = allShortestPaths((start:Person)-[:FRIENDS_WITH*]-(end:Person)) WHERE start <> end AND p IN nodes(path) RETURN p.name, count(*) as betweenness ORDER BY betweenness DESC

MATCH (p:Person) WITH p MATCH component = (p)-[:FRIENDS_WITH*]-(other:Person) RETURN p.name as Person, count(DISTINCT other) as ComponentSize ORDER BY ComponentSize DESC

MATCH (a:Person)-[:FRIENDS_WITH]-(b:Person), (b:Person)-[:FRIENDS_WITH]-(c:Person), (c:Person)-[:FRIENDS_WITH]-(a:Person) WHERE id(a) < id(b) AND id(b) < id(c) RETURN a.name, b.name, c.name

-- Recommendation
MATCH (me:Person {name: 'Alice'})-[:FRIENDS_WITH]-(friend)-[:FRIENDS_WITH]-(potential) WHERE NOT (me)-[:FRIENDS_WITH]-(potential) AND me <> potential RETURN potential.name as RecommendedFriend, count(friend) as MutualFriends ORDER BY MutualFriends DESC

MATCH (me:Person {name: 'Alice'})-[:INTERESTED_IN]->(myInterest:Interest) MATCH (other:Person)-[:INTERESTED_IN]->(myInterest) WHERE me <> other WITH other, count(myInterest) as CommonInterests MATCH (other)-[:INTERESTED_IN]->(otherInterest:Interest) WHERE NOT EXISTS { MATCH (me)-[:INTERESTED_IN]->(otherInterest) } RETURN other.name as Person, collect(otherInterest.name) as SuggestedInterests, CommonInterests ORDER BY CommonInterests DESC

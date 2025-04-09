// Just node statistics
MATCH (n)
RETURN labels(n)[0] AS label, count(*) AS total
ORDER BY total DESC;

// Just relationship statistics
MATCH ()-[r]->()
RETURN type(r) AS relationship, count(*) AS total
ORDER BY total DESC;

// Top diseases by number of symptoms
MATCH (d:Disease)-[:HAS_SYMPTOM]->(s:Symptom)
RETURN d.label AS disease, count(s) AS symptom_count
ORDER BY symptom_count DESC
LIMIT 10;

// Most connected symptoms
MATCH (d:Disease)-[:HAS_SYMPTOM]->(s:Symptom)
RETURN s.label AS symptom, count(DISTINCT d) AS disease_count
ORDER BY disease_count DESC
LIMIT 10;

// Symptoms with frequency for a specific disease
MATCH (d:Disease {label: "Dyskeratosis congenita"})-[r:HAS_SYMPTOM]->(s:Symptom)
RETURN s.label AS symptom, r.frequency
ORDER BY r.frequency;

// Diseases linked to a symptom
MATCH (s:Symptom {label: "Microlissencephaly"})<-[:HAS_SYMPTOM]-(d:Disease)
RETURN d.label AS disease;

// Inheritance tree for random disease
MATCH (d:Disease)
WITH d SKIP toInteger(rand() * 100) LIMIT 1
MATCH path = (d)-[:IS_A*1..5]->(ancestor)
RETURN path;

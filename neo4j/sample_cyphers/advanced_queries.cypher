// Diseases that share more than 3 symptoms with a given disease
MATCH (d1:Disease {label: "Ataxia-telangiectasia"})-[:HAS_SYMPTOM]->(s:Symptom)<-[:HAS_SYMPTOM]-(d2:Disease)
WHERE d1 <> d2
WITH d2, count(s) AS shared
WHERE shared > 3
RETURN d2.label AS similar_disease, shared
ORDER BY shared DESC;

// Group symptoms by frequency (how many symptoms occur with each freq)
MATCH ()-[r:HAS_SYMPTOM]->()
RETURN r.frequency AS frequency, count(*) AS count
ORDER BY count DESC;

// Demo for Reasoning: inherited symptoms via IS_A
MATCH (d:Disease)-[:IS_A*1..3]->(parent)-[r:HAS_SYMPTOM]->(s:Symptom)
RETURN d.label AS disease, collect(DISTINCT s.label) AS inherited_symptoms
LIMIT 10;
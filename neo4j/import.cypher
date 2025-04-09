// Load rows (Nodes)


LOAD CSV WITH HEADERS FROM 'file:///diseases.csv' AS row
MERGE (d:Disease {id: row.id})
SET d.label = row.label;

LOAD CSV WITH HEADERS FROM 'file:///symptoms.csv' AS row
MERGE (s:Symptom {id: row.id})
SET s.label = row.label;

// Load associations (Vertexes)
LOAD CSV WITH HEADERS FROM 'file:///disease_symptom_associations_expanded.csv' AS row
MATCH (d:Disease {id: row.disease_uri})
MATCH (s:Symptom {id: row.symptom_uri})
MERGE (d)-[r:HAS_SYMPTOM]->(s)
SET r.frequency = row.frequency;

LOAD CSV WITH HEADERS FROM 'file:///is_a.csv' AS row
MATCH (child {id: row.child_id})
MATCH (parent {id: row.parent_id})
MERGE (child)-[:IS_A]->(parent);

// Add constraints - not necessary but helpful

CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) REQUIRE d.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (s:Symptom) REQUIRE s.id IS UNIQUE;

// ===========================================================
// Assigning Numeric Frequency Scores for Symptom Occurrence
// ===========================================================
//
// For every relationship between a Disease node and a Symptom node (HAS_SYMPTOM),
// we convert qualitative frequency values into numerical scores (freq_score).
// This numerical representation serves as a weight in subsequent graph processing,
// allowing for a more refined analysis of the relationship's significance.
MATCH (:Disease)-[r:HAS_SYMPTOM]->(:Symptom)
SET r.freq_score =
  CASE r.frequency
    WHEN 'VF' THEN 1.0        // Very Frequent symptom occurrence
    WHEN 'Frequent' THEN 0.75   // Frequently observed symptom
    WHEN 'Occasional' THEN 0.25 // Occasionally observed symptom
    ELSE 0.1                   // Default low score for any other cases
  END;

// ===========================================================
// Main Graph Projection for Graph Data Science (GDS) Analysis
// ===========================================================
//
// This step creates a graph projection named 'rareGraph' that includes two node types:
// 'Disease' and 'Symptom'. The relationships of type HAS_SYMPTOM are enriched with
// the 'freq_score' property, enabling analyses that take into account the strength of
// these connections. Additionally, the projection incorporates IS_A relationships
// that can represent hierarchical or typical associations within the data.
CALL gds.graph.project(
  'rareGraph',
  ['Disease', 'Symptom'],
  {
    HAS_SYMPTOM: {
      type: 'HAS_SYMPTOM',
      properties: 'freq_score'
    },
    IS_A: {
      type: 'IS_A'
    }
  }
);

// ===========================================================
// Projection of a Disease Similarity Network Based on Shared Symptoms
// ===========================================================
//
// Here, a new graph projection named 'rareGraphS' is created. In this network, each node
// represents a disease, and an edge is drawn between any two diseases that share at least
// one common symptom. This similarity network lays the foundation for further analyses
// focusing on how diseases relate based on their symptom profiles.
CALL gds.graph.project.cypher(
  'rareGraphS',
  'MATCH (d:Disease) RETURN id(d) AS id',
  'MATCH (d:Disease)-[:HAS_SYMPTOM]->(s:Symptom)<-[:HAS_SYMPTOM]-(d2:Disease)
   RETURN id(d) AS source, id(d2) AS target'
);

// ===========================================================
// Centrality Analysis of Diseases using the PageRank Algorithm
// ===========================================================
//
// Utilizing the 'rareGraph' projection, the PageRank algorithm calculates an influence
// score for each node. We then filter the results to include only nodes labeled as Disease.
// This step helps identify the most connected diseases within the network, indicating their
// relative importance in the overall structure.
CALL gds.pageRank.stream('rareGraph')
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS node, score
WHERE "Disease" IN labels(node)
RETURN node.label AS disease, score
ORDER BY score DESC LIMIT 10;


// ===========================================================
// Community Detection using the Louvain Algorithm
// ===========================================================
//
// The Louvain algorithm is applied to identify naturally occurring clusters (communities)
// among the disease nodes. Each disease is assigned to a community, after which the diseases
// are grouped by their community identifier. This grouping provides insights into clusters of
// diseases that share common features or relationships.
CALL gds.louvain.stream('rareGraph')
YIELD nodeId, communityId
WITH communityId, gds.util.asNode(nodeId) AS node
ORDER BY node.label
WITH communityId, collect(node.label) AS diseases, count(*) AS groupSize
RETURN communityId, groupSize, diseases
ORDER BY groupSize ASC
LIMIT 3;

// ===========================================================
// Identification of Key Connector Symptoms via Betweenness Centrality
// ===========================================================
//
// Using the betweenness centrality algorithm, we calculate the extent to which each symptom node
// lies on the shortest paths between other nodes. A high betweenness score indicates that the
// symptom acts as a bridge between different regions of the disease network, suggesting its critical
// role in the overall connectivity and potential pathophysiology.
CALL gds.betweenness.stream('rareGraph')
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS node, score
WHERE "Symptom" IN labels(node)
RETURN node.label AS symptom, score
ORDER BY score DESC LIMIT 10;

// ===========================================================
// Writing Disease Similarity Relationships Based on Symptom Profiles
// ===========================================================
//
// Based on the 'rareGraphS' projection, node similarity is computed for each pair of diseases
// that share common symptoms. The resulting similarity measure is written as new relationships
// labeled SIMILAR, with the 'score' property representing the degree of similarity. Only pairs
// that meet the threshold (similarityCutoff of 0.1) are persisted, and the computation is performed
// with a concurrency factor of 4 for efficiency.
CALL gds.nodeSimilarity.write('rareGraphS', {
  writeRelationshipType: 'SIMILAR',
  writeProperty: 'score',
  similarityCutoff: 0.1,
  concurrency: 4
});

MATCH (d:Disease)-[r:SIMILAR]->(d2:Disease)
RETURN d.label AS first_disease, d2.label AS second_disease, r.score
ORDER BY r.score DESC LIMIT 10;

// Find diseases that match input symptoms or their subclasses
MATCH (s:Symptom)<-[:IS_A*0..3]-(input:Symptom)<-[:HAS_SYMPTOM]-(d:Disease)
WHERE input.label IN ["ataxia", "muscle weakness"]
RETURN d.label, COUNT(*) AS matchedSymptoms
ORDER BY matchedSymptoms DESC;


//Future Extensions
//
//Support for ordo:Gene, ordo:hasTreatment
//Integration with external ontologies (e.g. HPO, SNOMED)
//OWL inference layer using RDF stack (e.g., GraphDB, OWLAPI)
//LLM-based interface and retrieval (e.g., RAG architecture)




//
//Świetnie – Krok 7: Reasoning & Scoring 🔍
//Celem tego kroku jest:
//pokazać, że umiemy w reasoning logic (nawet bez OWL reasonera),
//stworzyć bardziej inteligentne dopasowanie niż tylko label match,
//wykorzystać Cyphera (i opcjonalnie GDS) do pokazania „inference-like” zachowań.
//🧠 Co zrobimy:
//
//Obsłużymy dziedziczenie symptomów (IS_A / subClassOf)
//Rozszerzymy zapytanie, żeby obsługiwało:
//Symptom lub jego podklasy (z grafu)
//Dodamy scoring: ile symptomów z inputu pasuje do choroby
//(Opcjonalnie później): GDS – node similarity, clustering etc.
//🧮 1. Cypher do reasoning (IS_A traversal)

UNWIND $symptoms AS s
MATCH (input:Symptom)
WHERE toLower(input.label) = toLower(s)

// Traversal do podklas – reasoning like
MATCH (matched:Symptom)-[:IS_A*0..3]->(input)
MATCH (d:Disease)-[:HAS_SYMPTOM]->(matched)

RETURN d.label AS disease, COUNT(DISTINCT matched) AS score
ORDER BY score DESC
LIMIT 10

//*0..3 oznacza: symptom, jego dzieci, wnuki (podklasy)
//DISTINCT matched = liczymy tylko unikalne trafienia
//Możesz potem pokazać:
//"We found symptoms matching directly or through subclass reasoning"





//----- NODE SIMILIARY

CALL gds.nodeSimilarity.stream({
  nodeProjection: ['Disease'],
  relationshipProjection: {
    sym: {
      type: 'HAS_SYMPTOM',
      orientation: 'UNDIRECTED'
    }
  },
  topK: 5
})
YIELD node1, node2, similarity

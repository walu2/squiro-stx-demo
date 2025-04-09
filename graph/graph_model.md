# 📘 Rare Disease Graph Model — Semantically Aligned

This document describes the semantic structure of the Neo4j-based knowledge graph, based on the ORDO ontology (Orphanet Rare Disease Ontology).

---

## 📚 Source Ontology

- **Name**: ORDO (Orphanet Rare Disease Ontology)
- **Format**: OWL2 / RDF/XML
- **URL**: https://www.ebi.ac.uk/ols4/ontologies/ordo
- **Imported into Neo4j manually** using a custom RDF parser + Cypher

---

## 🧩 Node Types (mapped OWL Classes → Graph Labels)

| Graph Label | OWL Class (IRI)                                 | Description                      |
|-------------|--------------------------------------------------|----------------------------------|
| `Disease`   | `ordo:Disease`                                  | Rare disease entity              |
| `Symptom`   | `ordo:Symptom`                                  | Symptom or phenotype             |
| `Gene`      | `ordo:Gene` (optional, for future extension)     | Gene involved in pathogenesis    |

---

## 🔗 Relationship Types (mapped OWL Properties → Graph Relationships)

| Relationship       | OWL Property                | Meaning                                               |
|--------------------|-----------------------------|--------------------------------------------------------|
| `:HAS_SYMPTOM`     | `ordo:has_symptom`          | A disease is associated with a symptom                |
| `:IS_A`            | `rdfs:subClassOf`           | Hierarchical parent class                             |
| `:CAUSED_BY_GENE`  | `ordo:caused_by_gene`       | (optional) Disease is caused by a gene                |

---

## 📐 Schema Notes

Even though Neo4j is schema-less, the data model here reflects the ontology structure of ORDO. All nodes have:

- `id`: full IRI string
- `label`: human-readable name from `rdfs:label`

Constraints are added to ensure uniqueness:
```cypher
CREATE CONSTRAINT FOR (d:Disease) REQUIRE d.id IS UNIQUE;
CREATE CONSTRAINT FOR (s:Symptom) REQUIRE s.id IS UNIQUE;
```

> ℹ️ Note: Symptom relationships are currently unavailable in ORDO OWL. They may be modeled via external modules (e.g., HOOM) in future versions.

Note: Genes are not explicitly included as class hierarchy under Orphanet_317344. They may be encoded through other properties or instances.
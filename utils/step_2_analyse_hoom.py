from rdflib import Graph, URIRef
from collections import defaultdict, Counter
import pandas as pd
from pathlib import Path

# === Path configuration ===
THIS_DIR = Path(__file__).resolve().parent
ONTOLOGY_PATH = THIS_DIR.parent / "data" / "owlapi.xrdf"
OUTPUT_PATH = THIS_DIR.parent / "neo4j" / "import"
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# === Parsing RDF/XML ===
print(f"🔄 Parsing file: {ONTOLOGY_PATH}")
graph = Graph()
graph.parse(ONTOLOGY_PATH, format="xml")
print(f"✅ Loaded {len(graph)} RDF triples")

# === Association predicates ===
subject_pred = URIRef("http://purl.org/oban/association_has_subject")
object_pred = URIRef("http://purl.org/oban/association_has_object")

subject_triples = list(graph.triples((None, subject_pred, None)))
object_triples = list(graph.triples((None, object_pred, None)))

print(f"🔎 Found {len(subject_triples)} triples with association_has_subject")
print(f"🔎 Found {len(object_triples)} triples with association_has_object")

# === Debug: print 5 examples of each ===
print("\n📌 Example association_has_subject:")
for t in subject_triples[:5]:
    print(t)

print("\n📌 Example association_has_object:")
for t in object_triples[:5]:
    print(t)

# === If no results – show the most frequently used predicates in RDF ===
if not subject_triples and not object_triples:
    print("\n❗ No expected predicates found – displaying the most frequently used ones:")
    preds = [str(p) for _, p, _ in graph]
    counts = Counter(preds)
    for pred, count in counts.most_common(20):
        print(f"{pred}: {count}")

from collections import Counter
from rdflib import OWL

preds = [str(o) for s, p, o in graph.triples((None, OWL.onProperty, None))]
counts = Counter(preds)

print("🔎 Most frequently used OWL properties (onProperty):")
for pred, count in counts.most_common(15):
    print(f"{pred}: {count}")

# From this result we understand what is happening:
# The predicates we checked earlier:
# http://purl.org/oban/association_has_object (115087 occurrences)
# http://purl.org/oban/association_has_subject (115087 occurrences)
# do indeed exist and are key in onthology dataset, but not as RDF instances — rather as elements of OWL restrictions (owl:onProperty).
# This means that the 'disease → symptom' relationships are modeled using OWL restrictions with properties from the OBAN namespace, e.g.:
#
# <Class rdf:about="Disease_XYZ">
#   <equivalentClass>
#     <Class>
#       <intersectionOf rdf:parseType="Collection">
#         <Class rdf:about="&obo;Disease"/>
#         <Restriction>
#           <onProperty rdf:resource="http://purl.org/oban/association_has_subject"/>
#           <someValuesFrom rdf:resource="&ordo;Disease_XYZ"/>
#         </Restriction>
#         <Restriction>
#           <onProperty rdf:resource="http://purl.org/oban/association_has_object"/>
#           <someValuesFrom rdf:resource="&hpo;Symptom_ABC"/>
#         </Restriction>
#       </intersectionOf>
#     </Class>
#   </equivalentClass>
# </Class>
#
# So onthology data looks like this (disease and symptom are connected via OWL restrictions using association_has_subject and association_has_object).

# === Mapping by common node (association) ===
assoc_map = defaultdict(dict)
for assoc, _, subj in subject_triples:
    assoc_map[assoc]["subject"] = str(subj)
for assoc, _, obj in object_triples:
    assoc_map[assoc]["object"] = str(obj)

clean_assocs = [
    {"association": str(a), "disease_uri": v["subject"], "symptom_uri": v["object"]}
    for a, v in assoc_map.items() if "subject" in v and "object" in v
]

df_assoc = pd.DataFrame(clean_assocs)

# === CSV Export ===
csv_output_path = OUTPUT_PATH / "disease_symptom_associations.csv"
df_assoc.to_csv(csv_output_path, index=False)

print(f"\n💾 Saved {len(df_assoc)} associations to file: {csv_output_path}")


# What does this imply?
#
# The predicates association_has_subject and association_has_object are missing.
# onthology analysis revealed that these predicates do not appear in the RDF/XML.
# This means that previous assumptions (which were based on popular patterns from the OBAN model) are not valid for this file.
# Other important predicates are present:
# The most frequent predicates (besides standard RDF/OWL ones) are:
# owl:equivalentClass
# owl:intersectionOf
# owl:someValuesFrom
# owl:hasValue
# These predicates suggest that the relationships between diseases and symptoms are modeled not by simple triples,
# but through equivalent class definitions (owl:equivalentClass) composed of property restrictions (owl:intersectionOf + owl:onProperty + owl:someValuesFrom).
# 🔍 What does this mean in practice (ontology structure)?
#
# onthology data likely looks something like this (OWL schema):
# :DiseaseXYZ owl:equivalentClass [
#     owl:intersectionOf (
#         :Disease
#         [ owl:onProperty :hasSymptom ;
#           owl:someValuesFrom :SymptomABC ]
#         [ owl:onProperty :hasSymptom ;
#           owl:someValuesFrom :SymptomDEF ]
#     )
# ].
# Instead of having a simple triple like:
# :DiseaseXYZ :hasSymptom :SymptomABC .
# you have equivalent class definitions that need to be unpacked.

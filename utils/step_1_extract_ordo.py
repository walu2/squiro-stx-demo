from rdflib import Graph, Namespace, RDFS, URIRef
import pandas as pd
from pathlib import Path

INCLUDE_MISSING = True

# === Configuration ===
THIS_DIR = Path(__file__).resolve().parent
ONTOLOGY_PATH = THIS_DIR.parent / "data_import" / "ordo.owl"
OUTPUT_PATH = THIS_DIR.parent / "neo4j" / "import"

ORDO = Namespace("http://www.orpha.net/ORDO/")
OBO = Namespace("http://purl.obolibrary.org/obo/")
g = Graph()
g.parse(ONTOLOGY_PATH)

print(f"Loaded {len(g)} triples from {ONTOLOGY_PATH}")

# === Ontology and Class Roots ===
CLASS_ROOTS = {
    "disease": URIRef("http://www.orpha.net/ORDO/Orphanet_557493"),
    "symptom": URIRef("http://www.orpha.net/ORDO/Orphanet_377791"),
  #  "gene": URIRef("http://www.orpha.net/ORDO/Orphanet_317344"),
}

# === Load utils ===
g = Graph()
g.parse(ONTOLOGY_PATH)

# === Extract entities ===
def extract_entities(root_uri, label_name):
    rows = []
    for s in g.subjects(RDFS.subClassOf, root_uri):
        label = g.value(s, RDFS.label)
        if True or label:
            rows.append({"id": str(s), "label": str(label) if label else ""})
    return pd.DataFrame(rows)

extract_entities(CLASS_ROOTS["disease"], "Disease").to_csv(OUTPUT_PATH / "diseases.csv", index=False)
extract_entities(CLASS_ROOTS["symptom"], "Symptom").to_csv(OUTPUT_PATH / "symptoms.csv", index=False)
#extract_entities(CLASS_ROOTS["gene"], "Gene").to_csv(OUTPUT_PATH / "genes.csv", index=False)


# === Extract subclass relations ===
subclasses = []
for s, p, o in g.triples((None, RDFS.subClassOf, None)):
    if INCLUDE_MISSING or isinstance(o, URIRef):
        subclasses.append({"child_id": str(s), "parent_id": str(o)})
pd.DataFrame(subclasses).to_csv(OUTPUT_PATH / "is_a.csv", index=False)

print("✅ ORDO extraction complete.")
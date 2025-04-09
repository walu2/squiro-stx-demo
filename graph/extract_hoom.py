from rdflib import Graph, URIRef, RDF, OWL
from pathlib import Path
import pandas as pd

THIS_DIR = Path(__file__).resolve().parent
ONTOLOGY_PATH = THIS_DIR.parent / "data" / "owlapi.xrdf"
OUTPUT_PATH = THIS_DIR.parent / "neo4j" / "import"
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

graph = Graph()
print(f"🔄 Parsuję {ONTOLOGY_PATH}")
graph.parse(ONTOLOGY_PATH, format="xml")
print(f"✅ Załadowano {len(graph)} trójek RDF")

# Funkcja rozpakowująca RDF listy (intersectionOf)
def unpack_list(node, graph):
    items = []
    while node and node != RDF.nil:
        first = graph.value(node, RDF.first)
        if first:
            items.append(first)
        node = graph.value(node, RDF.rest)
    return items

subject_pred = URIRef("http://purl.org/oban/association_has_subject")
object_pred = URIRef("http://purl.org/oban/association_has_object")

associations = []

# Wyciągnij klasy chorób wraz z ich restrykcjami OWL
for disease_class, _, equiv_node in graph.triples((None, OWL.equivalentClass, None)):
    for _, _, intersection_node in graph.triples((equiv_node, OWL.intersectionOf, None)):
        intersection_elements = unpack_list(intersection_node, graph)

        disease_uri = None
        symptom_uri = None

        for restriction in intersection_elements:
            if (restriction, RDF.type, OWL.Restriction) in graph:
                on_prop = graph.value(restriction, OWL.onProperty)
                some_values_from = graph.value(restriction, OWL.someValuesFrom)

                if on_prop == subject_pred:
                    disease_uri = some_values_from
                elif on_prop == object_pred:
                    symptom_uri = some_values_from

        if disease_uri and symptom_uri:
            associations.append({
                "disease_class": str(disease_class),
                "disease_uri": str(disease_uri),
                "symptom_uri": str(symptom_uri)
            })

print(f"✅ Znaleziono {len(associations)} par choroba–objaw")

df = pd.DataFrame(associations)
csv_output_path = OUTPUT_PATH / "disease_symptom_associations.csv"
df.to_csv(csv_output_path, index=False)

print(f"💾 Wyniki zapisane do {csv_output_path}")

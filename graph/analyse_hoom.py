import re
from rdflib import Graph, URIRef
from collections import defaultdict, Counter
import pandas as pd
from pathlib import Path

# === Konfiguracja ścieżek ===
THIS_DIR = Path(__file__).resolve().parent
ONTOLOGY_PATH = THIS_DIR.parent / "data" / "owlapi.xrdf"
OUTPUT_PATH = THIS_DIR.parent / "neo4j" / "import"
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# === Parsowanie RDF/XML ===
print(f"🔄 Parsuję plik: {ONTOLOGY_PATH}")
graph = Graph()
graph.parse(ONTOLOGY_PATH, format="xml")
print(f"✅ Załadowano {len(graph)} trójek RDF")

# === Predykaty asocjacji ===
subject_pred = URIRef("http://purl.org/oban/association_has_subject")
object_pred = URIRef("http://purl.org/oban/association_has_object")

subject_triples = list(graph.triples((None, subject_pred, None)))
object_triples = list(graph.triples((None, object_pred, None)))

print(f"🔎 Znaleziono {len(subject_triples)} trójek z association_has_subject")
print(f"🔎 Znaleziono {len(object_triples)} trójek z association_has_object")

# === Debug: wypisz 5 przykładów z każdej ===
print("\n📌 Przykładowe association_has_subject:")
for t in subject_triples[:5]:
    print(t)

print("\n📌 Przykładowe association_has_object:")
for t in object_triples[:5]:
    print(t)

# === Jeśli brak wyników – pokaż najczęstsze predykaty w RDF ===
if not subject_triples and not object_triples:
    print("\n❗ Brak expected predykatów – pokazuję najczęstsze użyte:")
    preds = [str(p) for _, p, _ in graph]
    counts = Counter(preds)
    for pred, count in counts.most_common(20):
        print(f"{pred}: {count}")


from collections import Counter
from rdflib import OWL

preds = [str(o) for s, p, o in graph.triples((None, OWL.onProperty, None))]
counts = Counter(preds)

print("🔎 Najczęściej używane właściwości OWL (onProperty):")
for pred, count in counts.most_common(15):
    print(f"{pred}: {count}")


# Dzięki temu wynikowi wiemy już, co się dzieje:
# Predykaty, które wcześniej sprawdzaliśmy:
# http://purl.org/oban/association_has_object (115087 wystąpień)
# http://purl.org/oban/association_has_subject (115087 wystąpień)
# faktycznie istnieją i są kluczowe w Twoim zbiorze, ale nie w formie instancji RDF, tylko jako elementy OWL restrictions (owl:onProperty).
# To oznacza, że relacje „choroba → objaw” są modelowane za pomocą OWL restrictions z właściwościami z przestrzeni OBAN, np.:
# <Class rdf:about="Choroba_XYZ">
#   <equivalentClass>
#     <Class>
#       <intersectionOf rdf:parseType="Collection">
#         <Class rdf:about="&obo;Disease"/>
#         <Restriction>
#           <onProperty rdf:resource="http://purl.org/oban/association_has_subject"/>
#           <someValuesFrom rdf:resource="&ordo;Choroba_XYZ"/>
#         </Restriction>
#         <Restriction>
#           <onProperty rdf:resource="http://purl.org/oban/association_has_object"/>
#           <someValuesFrom rdf:resource="&hpo;Symptom_ABC"/>
#         </Restriction>
#       </intersectionOf>
#     </Class>
#   </equivalentClass>
# </Class>
# Czyli twoje dane wyglądają właśnie tak (choroba i objaw są połączone przez OWL restrictions z wykorzystaniem association_has_subject i association_has_object).

# === Mapowanie po wspólnym węźle (association) ===
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

# === Zapis CSV ===
csv_output_path = OUTPUT_PATH / "disease_symptom_associations.csv"
df_assoc.to_csv(csv_output_path, index=False)

print(f"\n💾 Zapisano {len(df_assoc)} asocjacji do pliku: {csv_output_path}")

#
# 🔄 Parsuję plik: /Users/piotrwalkowski/python/rare-disease-assistant/graph/owlapi.xrdf
# ✅ Załadowano 3524182 trójek RDF
# 🔎 Znaleziono 0 trójek z association_has_subject
# 🔎 Znaleziono 0 trójek z association_has_object
#
# 📌 Przykładowe association_has_subject:
#
# 📌 Przykładowe association_has_object:
#
# ❗ Brak expected predykatów – pokazuję najczęstsze użyte:
# http://www.w3.org/1999/02/22-rdf-syntax-ns#type: 804619
# http://www.w3.org/2002/07/owl#onProperty: 553013
# http://www.w3.org/1999/02/22-rdf-syntax-ns#first: 553012
# http://www.w3.org/1999/02/22-rdf-syntax-ns#rest: 553012
# http://www.w3.org/2002/07/owl#someValuesFrom: 435167
# http://www.w3.org/2000/01/rdf-schema#label: 133640
# http://www.w3.org/2000/01/rdf-schema#subClassOf: 133625
# http://www.w3.org/2002/07/owl#equivalentClass: 117938
# http://www.w3.org/2002/07/owl#intersectionOf: 117931
# http://www.w3.org/2002/07/owl#hasValue: 117839
# http://www.w3.org/2000/01/rdf-schema#comment: 4304
# http://www.w3.org/2000/01/rdf-schema#range: 14
# http://www.w3.org/2000/01/rdf-schema#domain: 14
# http://www.w3.org/2000/01/rdf-schema#isDefinedBy: 12
# http://purl.org/dc/elements/1.1/creator: 7
# http://www.w3.org/2002/07/owl#onClass: 6
# http://www.w3.org/2002/07/owl#inverseOf: 6
# https://creativecommons.org/licenses/permits: 3
# http://www.w3.org/2002/07/owl#qualifiedCardinality: 3
# http://www.w3.org/2002/07/owl#minQualifiedCardinality: 2
# 🔎 Najczęściej używane właściwości OWL (onProperty):
# http://purl.org/oban/association_has_object: 115087
# http://purl.org/oban/association_has_subject: 115087
# http://www.semanticweb.org/ontology/HOOM#validation_association_date: 114994
# http://www.semanticweb.org/ontology/HOOM#has_frequency: 114376
# http://purl.org/oban/has_provenance: 86208
# http://purl.obolibrary.org/obo/RO_0002558: 5682
# http://www.semanticweb.org/ontology/HOOM#has_DC_attribute: 1568
# http://www.semanticweb.org/ontology/HOOM#with_frequency: 6
# http://www.semanticweb.org/ontology/HOOM#is_DC_attribute: 1
# http://purl.obolibrary.org/obo/RO_0002472: 1
# http://www.semanticweb.org/ontology/HOOM#is_frequency: 1
# http://purl.org/oban/object_has_association: 1
# http://purl.org/oban/subject_has_association: 1
#
# 💾 Zapisano 0 asocjacji do pliku: /Users/piotrwalkowski/python/rare-disease-assistant/neo4j/import/disease_symptom_associations.csv

# Co z tego wynika?
#
# Brak predykatów association_has_subject i association_has_object
# Twoja analiza pokazała, że w RDF/XML nie występują te predykaty. To oznacza, że wcześniejsze przypuszczenia (które opierały się na popularnych wzorcach z modelu OBAN) nie są prawdziwe dla tego pliku.
# Występują inne istotne predykaty:
# Najczęstsze predykaty (oprócz standardowych RDF/OWL) to:
# owl:equivalentClass
# owl:intersectionOf
# owl:someValuesFrom
# owl:hasValue
# Te predykaty sugerują, że relacje między chorobami i symptomami są modelowane nie za pomocą prostych trójek, ale za pomocą klas równoważnych (owl:equivalentClass) złożonych z ograniczeń na właściwościach (owl:intersectionOf + owl:onProperty + owl:someValuesFrom).
# 🔍 Co to oznacza w praktyce (struktura ontologii)?
#
# Twoje dane najprawdopodobniej wyglądają mniej więcej tak (schemat OWL):
# :ChorobaXYZ owl:equivalentClass [
#     owl:intersectionOf (
#         :Disease
#         [ owl:onProperty :hasSymptom ;
#           owl:someValuesFrom :SymptomABC ]
#         [ owl:onProperty :hasSymptom ;
#           owl:someValuesFrom :SymptomDEF ]
#     )
# ].
# Zamiast mieć prostą trójkę typu:
# :ChorobaXYZ :hasSymptom :SymptomABC .
# masz definicje klas równoważnych, które trzeba rozpakować.
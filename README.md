# 🧠 Rare Disease Assistant – Graph-AI Demo

This is a 1-day showcase project that demonstrates how structured semantic knowledge (from ORDO ontology) can be used for rare disease reasoning using graphs, lightweight NLP and optional LLM support.

---

## 🎯 Goal

> “Given a free-text input with patient symptoms, identify likely rare diseases using a knowledge graph derived from ORDO, and explain the reasoning behind the match.”

---

## 🧱 Tech Stack

| Layer       | Tool / Tech           | Purpose                         |
|-------------|------------------------|----------------------------------|
| Graph DB    | Neo4j                  | Stores semantically structured disease/symptom graph |
| Ontology    | ORDO (OWL)             | Medical reference ontology       |
| NLP         | spaCy + keyword mapping| Simple symptom extraction        |
| Reasoning   | Cypher + `IS_A`        | Inference via subclass traversals |
| LLM (opt)   | GPT via OpenAI         | Explanation of results           |
| API         | FastAPI                | Backend interface                |
| Infra       | Docker Compose         | Full local environment           |

---

## 🚀 How to Run

### 1. Clone repo and if needed download newest ordo.owl file

### USAGE
```bash
cd rare-disease-assistant
python -m venv .venv
source .venv/bin/
pip3 install -r requirements.txt
```

For windows:
```
.\.venv\Scripts\activate
```


ORDER
```bash
python3 python3 graph/extract_ordo.py

```

DISCLAIMER!

> ⚠️ Although Neo4j supports RDF/OWL via the `n10s` plugin, this demo performs manual RDF parsing using `rdflib`, to allow greater control over which elements of the ontology are mapped and exported.


### 2. Start Neo4j + API
```bash
docker-compose up
```

* Neo4j: http://localhost:7474 
* FastAPI docs: http://localhost:8000/docs

### 3. Load data into Neo4j
Open Neo4j browser and run:
```cypher
:play cypher_import.cypher
```

✅ Szybki start

docker-compose up --build
Potem:
FastAPI docs: http://localhost:8000/docs
Neo4j browser: http://localhost:7474


### RUN NEO
```
cd neo4j/
docker-compose up -d
```
neo4j:password <- creds

```bash
docker exec -i rare-neo4j bin/cypher-shell -u neo4j -p password < import.cypher
```

This might take up to few minutes.


Play in browser
```
CALL dbms.procedures() YIELD name WHERE name CONTAINS 'apoc' RETURN name;
```

Then call
```
:play /guides/intro.adoc

```
### 4. API ENDPOINTS AND REQUESTS

## Short overview:
*API Endpoints*

`/match` – find diseases by symptoms
```
POST /match
{ "text": "ataxia and muscle weakness" }
```


```
POST /summary
{
  "symptoms": ["ataxia", "muscle weakness"],
  "diseases": [
    {"name": "Friedreich ataxia", "matches": 2}
  ]
}
```

```bash
curl -X POST http://localhost:8000/match \
-H "Content-Type: application/json" \
-d '{"text": "The patient has ataxia and muscle weakness."}'
```


```
curl -X POST http://localhost:8000/summary \
-H "Content-Type: application/json" \
-d '{
  "symptoms": ["ataxia", "muscle weakness"],
  "diseases": [
    {"name": "Friedreich ataxia", "matches": 2},
    {"name": "Spinocerebellar ataxia", "matches": 1}
  ]
}'
```


_Based on the symptoms of ataxia and muscle weakness, the most likely candidate is Friedreich ataxia. This condition is known to cause progressive ataxia and muscular degeneration. Spinocerebellar ataxia is also possible due to partial symptom overlap."_


### DEPLOYMENT

🐳 Krok 4: Przygotuj deployment na Fly.io

4.1 Zainstaluj Fly CLI
brew install flyctl  # Mac
lub:
curl -L https://fly.io/install.sh | sh
4.2 Zaloguj się i zainicjuj projekt
fly auth login
cd rare-disease-assistant
fly launch --name rare-disease-api --no-deploy
Wybierz np. Frankfurt jako region


fly deploy

---
### 🧠 Design Philosophy

This demo was designed to balance:
* Semantic awareness (OWL → Neo4j + documented mapping)
* Graph reasoning (multi-hop traversal, IS_A inference)
* Engineering practice (API, Docker, FastAPI)
* Scalability (LLM layer, RAG-ready architecture)
* See `graph/graph_model.md` for full ontology mapping details.

### 📈 Future Directions
* RDF-native reasoning layer (GraphDB, Jena)
* Biomedical NER (UMLS / BioPortal)
* Retrieval-Augmented Generation with LLMs
* UI for clinicians (Streamlit prototype)


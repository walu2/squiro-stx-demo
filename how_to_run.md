## 🚀 How to Run
### Clone repo and if needed download newest ordo.owl file

* Make sure you have Docker on your machine.
* Open .env and update `OPENAI_API_KEY` other doesnt need to be changed
You'll need two onthologies which repo is based on:

Download from here -> https://bioportal.bioontology.org/ontologies/ORDO Newest onthology and copy to `data_import/ordo.owl`
Additionally -> https://bioportal.bioontology.org/ontologies/HOOM and choose RDF/XML (because  )
copy those under `data_import` respectively as `ordo.owl` and `owlapi.xrdf` files


* From now theoretically all needd is to run:
`docker-compose up -d   (to remove `docker-compose -r -f; docker-compose down -v`)
`

You should see sth like: ![working doker](static/docker_working.png)


---
* Neo4j: http://localhost:7474 
* FastAPI: http://localhost:8000

> ⚠️ Due limited time I get rid of any frontend part so that we have only API available, but this might be easily improved in later stages...

For testing purpouses all data-engineering work is already commited but you can do it step by step


> ⚠️ Although Neo4j supports RDF/OWL via the `n10s` plugin, this demo performs manual RDF parsing using `rdflib`, to allow greater control over which elements of the ontology are mapped and exported.

```bash
python3 utils/step_1_extract_ordo.py
python3 utils/step_2_analyse_hoom.py
python3 utils/step_3_extract_hoom.py
python3 utils/step_4_extract_hoom_improver.py
python3 utils/step_5_symptoms_maker.py
``` 

So that we should have ready csv files to import property graph in neo -> `neo4j/import/*.csv` files. Same for `app/nlp/mapping_dict.json` used to NER checkings.

---
Now you can import data to neo4j (this gonna take ~ approx 5 minutes) in a both ways:
- you can call neo4j docker

```docker exec -i rare-neo4j bin/cypher-shell -u neo4j -p password < neo4j/import.cypher```

- alternatively open brower in http://localhost:7474/browser/
and copy/paste content from `/rare-disease-assistant/neo4j/import.cyper`


Now having few data
[IMGS]

---

see [Graph Model](graph/graph_model.md) for details

### Playing with graph queries
We can now experiment by calling [procedures](neo4j/sample_cyphers) stored in project folder.

#### The project includes three main files:
* `basic_queries.cypher` – contains simple Cypher queries and examples of basic expressions  
* `advanced_queries.cypher` – features more complex query structures  
* `gds_queries.cypher` – demonstrates reasoning and graph algorithms (refer to this [description](neo4j/GDS_interpret.md) for details)

You can either copy and run each query step-by-step for full control, or execute them directly from the browser console.

To launch guides from the Neo4j browser, you can use:
```
:play /guides/intro-guide.adoc
:play /guides/advanced-guide.adoc
:play /guides/gds-guide.adoc
```

### (EXTRA) MANUAL USAGE
If you insist not to use `docker-compose` you can also play by your own
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

And call e.g
```bash
python3 python3 utils/step_1_extract_ordo.py
```

### Endpoints

## 4. 📡 API Endpoints (FastAPI)

| Endpoint       | Method | Description                                |
|----------------|--------|--------------------------------------------|
| `/status`      | GET    | Healthcheck – confirms service is running  |
| `/match`       | POST   | Matches input symptoms to diseases          |
| `/summary`     | POST   | Generates LLM-based summary from matches    |

---

### ✅ `GET /status`


Check if the API is alive.


```bash
curl http://localhost:8000/status
```
Response
```json
{
  "status": "ok"
}
```
### `POST /match`

Find diseases matching user-provided symptoms.
```bash
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This patient had weird cyst, sometimes StErNaL cleft & muscle weakness"
  }'

```
Response
```json
{
  "symptoms_matched": [
    "Sternal cleft"
  ],
  "diseases": [
    {
      "name": "Relapsing polychondritis",
      "matches": 1
    },
    {
      "name": "Vitamin B12-unresponsive methylmalonic acidemia",
      "matches": 1
    },
    {
      "name": "Palmoplantar keratoderma-esophageal carcinoma syndrome",
      "matches": 1
    },
    {
      "name": "Fabry disease",
      "matches": 1
    },
    {
      "name": "TSH-secreting pituitary adenoma",
      "matches": 1
    },
    {
      "name": "Gitelman syndrome",
      "matches": 1
    }
  ]
}

```

### `POST /summary`

Generate a natural language summary based on graph-derived disease matches (with some LLMs and NLP integrtion... just to show off 😎)

```bash
curl -X POST http://localhost:8000/summary \
  -H "Content-Type: application/json" \
  -d '{
    "diseases": [
      { "label": "Friedreich ataxia", "score": 3 },
      { "label": "Ataxia-telangiectasia", "score": 2 }
    ],
    "symptoms": ["ataxia", "muscle weakness", "coordination issues"]
  }'

```
Response
```json
{
  "summary": "Based on the provided symptoms, Friedreich's ataxia and Ataxia-telangiectasia are the most likely rare diseases. Both share neurological features such as coordination issues and muscular weakness. Further clinical validation is advised."
}
```
---
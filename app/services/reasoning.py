from neo4j import Driver
from app.nlp.symptoms_extractor import extract_symptoms

def match_diseases(text: str, driver: Driver):
    # Uproszczona ekstrakcja symptomów z tekstu
    symptoms = extract_symptoms(text)

    if not symptoms:
        return {
            "symptoms_matched": [],
            "diseases": []
        }

    cypher = """
    UNWIND $symptoms AS s
    MATCH (sym:Symptom)
    WHERE toLower(sym.label) = toLower(s)
    MATCH (d:Disease)-[:HAS_SYMPTOM]->(sym)
    RETURN d.label AS disease, count(*) AS matchCount
    ORDER BY matchCount DESC
    LIMIT 10
    """

    with driver.session() as session:
        result = session.run(cypher, symptoms=symptoms)
        diseases = [{"name": r["disease"], "matches": r["matchCount"]} for r in result]

    return {
        "symptoms_matched": symptoms,
        "diseases": diseases
    }
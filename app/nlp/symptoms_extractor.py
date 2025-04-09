import spacy
from pathlib import Path
import json

# Load the lightweight spaCy model (you may use a larger model in production)
nlp = spacy.load("en_core_web_sm")

# Define the path to the mapping_dict.json file located in the same folder
MAPPING_PATH = Path(__file__).parent / "mapping_dict.json"

# Try to load known symptoms from the JSON file; if not available, use the fallback list
try:
    with open(MAPPING_PATH, 'r', encoding='utf-8') as file:
        mapping_dict = json.load(file)
    # Use the values from the JSON mapping as known symptoms
    KNOWN_SYMPTOMS = list(mapping_dict.values())
except FileNotFoundError:
    print(f"Mapping file {MAPPING_PATH} not found. Using default known symptoms.")
    KNOWN_SYMPTOMS = [
        "Situs inversus totalis",
        "Microlissencephaly",
        "Esophageal duplication cyst",
        "Cleft hard palate",
        "Familial isolated congenital asplenia"
    ]

def normalize(text: str):
    """Normalizes a string: strips whitespace and converts to lowercase."""
    return text.strip().lower()

def extract_symptoms(text: str) -> list:
    """
    Uses spaCy NER and matching to extract known symptoms from the input text.
    1. Performs an exact known phrase match.
    2. Optionally uses spaCy's NER to detect additional symptom entities.
    """
    doc = nlp(text)
    text_lower = text.lower()

    # 1. Exact known phrase match
    matches = [
        symptom for symptom in KNOWN_SYMPTOMS
        if normalize(symptom) in text_lower
    ]

    # 2. Optionally: NER-based symptom detection
    for ent in doc.ents:
        ent_text = normalize(ent.text)
        if ent_text in map(normalize, KNOWN_SYMPTOMS) and ent_text not in matches:
            matches.append(ent_text)

    return list(set(matches))

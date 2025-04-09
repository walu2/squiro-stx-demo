import csv
import json
from pathlib import Path

# Define the base directory and file paths relative to it
BASE_DIR = Path(__file__).resolve().parent.parent
SYMPTOMS_CSV = BASE_DIR / "neo4j" / "import" / "symptoms.csv"
OUTPUT_JSON = BASE_DIR / "app" / "nlp" / "mapping_dict.json"

mapping_dict = {}

with open(SYMPTOMS_CSV, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip header row
    next(csv_reader, None)

    for row in csv_reader:
        if len(row) >= 2:  # Ensure the row has at least two columns
            key = row[0].strip()
            value = row[1].strip()
            mapping_dict[key] = value

with open(OUTPUT_JSON, mode='w', encoding='utf-8') as json_file:
    json.dump(mapping_dict, json_file, ensure_ascii=False, indent=4)

print(f"Mapping dictionary successfully saved to {OUTPUT_JSON}")

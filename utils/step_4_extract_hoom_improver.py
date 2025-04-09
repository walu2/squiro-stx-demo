import pandas as pd
import re
from pathlib import Path

# Define file paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_CSV = BASE_DIR / "../neo4j/import/disease_symptom_associations.csv"
OUTPUT_CSV = BASE_DIR / "../neo4j/import/disease_symptom_associations_expanded.csv"

# Frequency mapping dictionary
FREQ_MAP = {
    "F": "Frequent",
    "O": "Occasional",
    "OB": "Obligate",
    "OC": "Occasional",
    "R": "Rare",
    "V": "Very Frequent",
    "Ex": "Excluded",
}

# Read the input CSV into a DataFrame. We assume the CSV has three columns:
#   hoom_uri, disease_uri, original_symptom_uri
df = pd.read_csv(INPUT_CSV, header=None, names=["hoom_uri", "disease_uri", "original_symptom_uri"])

# Remove duplicate header rows if present (i.e., rows where the first column equals "hoom_uri")
df = df[df["hoom_uri"] != "hoom_uri"].copy()

def decode_hoom_uri(hoom_uri):
    """
    Parse a HOOM URI of the form:
      http://www.semanticweb.org/ontology/HOOM#Orpha:891_HP:0007917_Freq:F
    and return a tuple:
      - the ORPHA-style symptom URI, constructed as:
          http://www.orpha.net/ORDO/Orphanet_{hp_id}
        where hp_id is converted to integer to remove leading zeros (e.g., "0007917" → "7917")
      - the frequency description from FREQ_MAP (e.g., "F" → "Frequent")
    If the input doesn't match the expected pattern, return (None, None).
    """
    pattern = r"Orpha:(\d+)_HP:(\d+)_Freq:([A-Z]+)"
    match = re.search(pattern, hoom_uri)
    if match:
        # We don't use the first group (disease id) because disease_uri is already provided.
        hp_id_str = match.group(2)
        # Remove leading zeros by converting to int
        hp_id = str(int(hp_id_str))
        freq_code = match.group(3)
        # Construct the symptom URI using the ORPHA pattern (without leading zeros)
        orpha_symptom_uri = f"http://www.orpha.net/ORDO/Orphanet_{hp_id}"
        frequency = FREQ_MAP.get(freq_code, freq_code)
        return orpha_symptom_uri, frequency
    else:
        return None, None

# Apply the decoding function to the 'hoom_uri' column
decoded = df["hoom_uri"].apply(lambda x: pd.Series(decode_hoom_uri(x), index=["decoded_symptom_uri", "frequency"]))

# Merge the decoded results with the original DataFrame
df = pd.concat([df, decoded], axis=1)

# Filter out rows where decoding failed (i.e., decoded_symptom_uri is null)
df = df[df["decoded_symptom_uri"].notnull()].copy()

# Override the original symptom URI with the decoded symptom URI
df["symptom_uri"] = df["decoded_symptom_uri"]

# Keep only the necessary columns: disease_uri, symptom_uri, and frequency
final_df = df[["disease_uri", "symptom_uri", "frequency"]].copy()

# Save the expanded associations to a CSV file
final_df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved {len(final_df)} records to {OUTPUT_CSV}")

import sys
from pathlib import Path

# TODO: Fix that shit
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))
from nlp.symptoms_extractor import extract_symptoms

example_texts = [
    "The patient has situs inversus totalis and frequent nosebleeds.",
    "Microlissencephaly is suspected due to abnormal brain structure.",
    "Family history of congenital asplenia and cleft hard palate.",
    "No visible symptoms yet, but duplicated esophagus might appear.",
    "Unrelated sentence about vitamin D deficiency."
]

for i, text in enumerate(example_texts, 1):
    matches = extract_symptoms(text)
    print(f"Test case {i}:")
    print(f"Input: {text}")
    print(f"Matched symptoms: {matches}\n")

#
# Test case 1:
# Input: The patient has situs inversus totalis and frequent nosebleeds.
# Matched symptoms: ['Situs inversus totalis']
#
# Test case 2:
# Input: Microlissencephaly is suspected due to abnormal brain structure.
# Matched symptoms: ['Microlissencephaly', 'microlissencephaly']
#
# Test case 3:
# Input: Family history of congenital asplenia and cleft hard palate.
# Matched symptoms: ['Cleft hard palate']
#
# Test case 4:
# Input: No visible symptoms yet, but duplicated esophagus might appear.
# Matched symptoms: []
#
# Test case 5:
# Input: Unrelated sentence about vitamin D deficiency.
# Matched symptoms: []
#

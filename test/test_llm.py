import sys
from pathlib import Path

# TODO: Fix that shit
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))
from llm.summary_generator import generate_summary

symptoms = [
    "Situs inversus totalis",
    "Microlissencephaly"
]

diseases = [
    {"name": "Ciliary dyskinesia", "matches": 2},
    {"name": "Microcephaly with brainstem abnormalities", "matches": 1},
]

print("Prompt test:")
print(generate_summary(symptoms, diseases))

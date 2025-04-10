import os
import openai


def offline_generate_summary(symptoms: list, diseases: list) -> str:
    """
    Generate an offline summary based on the provided symptoms and diseases.
    """
    disease_lines = "\n".join(
        f"- {d['label']} (score: {d.get('score') or d.get('matches')})" for d in diseases
    )

    summary = (
        "Offline Summary:\n"
        f"Provided symptoms: {', '.join(symptoms)}.\n\n"
        "Matched diseases:\n"
        f"{disease_lines}\n\n"
        "Based on this information, the most likely diagnoses are those diseases that best match the given symptoms. "
        "Further diagnostic tests and consultation with a specialist are recommended."
    )

    return summary


def generate_summary(data: dict) -> str:
    """
    Generate a natural language summary using OpenAI API (or offline fallback),
    based on symptoms and diseases already matched.
    """
    symptoms = data.get("symptoms", [])
    diseases = data.get("diseases", [])

    if not diseases or not symptoms:
        return "Insufficient data provided to generate a meaningful summary."

    # Set up the API key from environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY", "sk-...")  # Replace with fallback only for local dev/testing

    disease_lines = "\n".join(
        f"- {d['label']} (score: {d.get('score') or d.get('matches')})" for d in diseases
    )

    prompt = (
        f"Given the symptoms: {', '.join(symptoms)}\n"
        f"and the matched rare diseases:\n{disease_lines}\n\n"
        "Write a medical-style explanation suggesting which diseases are most likely and why."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as error:
        print("Error communicating with OpenAI API. Switching to offline mode.")
        print("Error details:", error)
        return offline_generate_summary(symptoms, diseases)

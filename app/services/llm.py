import os
import openai


def offline_generate_summary(symptoms: list, diseases: list) -> str:
    """
    Generate an offline summary based on the provided symptoms and diseases.
    """
    disease_lines = "\n".join(
        f"- {d['name']} (matched symptoms: {d['matches']})" for d in diseases
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


def generate_summary(symptoms: list, diseases: list) -> str:
    """
    Try to generate a summary using the OpenAI API.
    If API communication fails, return an offline result.
    """
    # Set up the API key. Prefer the environment variable, or use a fallback key if not provided.
    openai.api_key = os.getenv("OPENAI_API_KEY", "sk-...")  # Replace "sk-..." with your fallback API key if needed

    disease_lines = "\n".join(
        f"- {d['name']} (matched symptoms: {d['matches']})" for d in diseases
    )

    prompt = (
        f"Given the following symptoms: {', '.join(symptoms)},\n"
        f"and the following matched rare diseases:\n"
        f"{disease_lines}\n\n"
        "Generate a medical-style explanation that suggests which diseases are most likely, and why.\n"
        "Explain the symptom-disease relationship in simple but accurate language."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return response['choices'][0]['message']['content']
    except Exception as error:
        # If communication with OpenAI fails, fall back to the offline mode.
        print("Error communicating with OpenAI API. Switching to offline mode.")
        print("Error details:", error)
        return offline_generate_summary(symptoms, diseases)
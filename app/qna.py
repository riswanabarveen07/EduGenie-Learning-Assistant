from app.gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a friendly AI learning assistant.

Answer this academic or general-knowledge question accurately and clearly.

Question:
{question}

Requirements:
- Give a direct answer first.
- Explain the reasoning or context in simple language.
- Use headings or bullets when useful.
- Give a small example when useful.
- Avoid unnecessary jargon.
- If the question is ambiguous, state the assumption clearly.
"""
    result = generate_text(prompt)
    if result:
        return result

    return (
        "## EduGenie could not generate an answer\n\n"
        "The Gemini service is unavailable or the API key is not configured. "
        "Please check your `.env` file and try again."
    )

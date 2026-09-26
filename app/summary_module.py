from app.gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational passage.

Passage:
{text}

Requirements:
- Preserve the main facts and key ideas.
- Remove repetition and unnecessary details.
- Use simple, clear language.
- Keep the summary concise but complete.
- Use bullet points when helpful.
- Do not invent facts that are not present in the passage.
"""
    result = generate_text(prompt)
    if result:
        return result

    words = text.split()
    if len(words) <= 90:
        return "## Summary\n\n" + text.strip()

    compact = " ".join(words[:90])
    return (
        "## Summary\n\n"
        + compact
        + "...\n\n"
        "AI summarization is unavailable right now, so this fallback "
        "preserves the opening content rather than inventing a summary."
    )

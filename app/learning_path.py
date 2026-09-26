from app.gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
You are EduGenie, a personalized learning-path assistant.

Create a structured learning path for:
{topic}

Requirements:
- Cover beginner, intermediate, and advanced stages.
- Organize the path in a logical order.
- Include suggested timelines.
- Include step-by-step learning activities.
- Include practice ideas.
- Recommend useful resource types such as official documentation,
  videos, articles, and books. Do not invent exact URLs.
- Mention prerequisites when relevant.
- End with a practical mini-project or assessment idea.
- Keep the plan realistic for a self-learner.
- Use clear Markdown headings and bullet points.
"""
    result = generate_text(prompt)
    if result:
        return result

    return f"""# Learning Path: {topic}

## Beginner
1. Learn the basic terminology and purpose of {topic}.
2. Study the core concepts with simple examples.
3. Practice with small exercises.

## Intermediate
1. Study major components and common patterns.
2. Solve practical problems.
3. Review mistakes and strengthen weak areas.

## Advanced
1. Explore advanced concepts and real-world use cases.
2. Build a small project using {topic}.
3. Review the project and identify improvements.

## Suggested Timeline
- Beginner: 1–2 weeks
- Intermediate: 2–3 weeks
- Advanced: 2–4 weeks

## Practice
- Take notes in your own words.
- Use active recall.
- Complete practical exercises.
- Finish with a mini-project.
"""

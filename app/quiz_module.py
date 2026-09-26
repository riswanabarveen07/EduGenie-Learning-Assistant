
import json
import re

from app.gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def fallback_quiz(topic_or_text: str) -> list:
    topic = topic_or_text.strip()[:80] or "the topic"

    return [
        {
            "question": f"What is the main purpose of studying {topic}?",
            "options": [
                "To understand the key ideas",
                "To avoid learning anything",
                "To remove all examples",
                "To make the topic unrelated",
            ],
            "correct_answer": "To understand the key ideas",
        },
        {
            "question": f"Which approach is most useful when learning {topic}?",
            "options": [
                "Understand, practice, and review",
                "Memorize without understanding",
                "Skip difficult parts",
                "Never test yourself",
            ],
            "correct_answer": "Understand, practice, and review",
        },
        {
            "question": f"What should a learner do after making a mistake about {topic}?",
            "options": [
                "Review the mistake and learn from it",
                "Ignore it",
                "Stop studying",
                "Delete the notes",
            ],
            "correct_answer": "Review the mistake and learn from it",
        },
        {
            "question": f"Why is practice important when learning {topic}?",
            "options": [
                "It helps reinforce understanding",
                "It makes learning impossible",
                "It removes the need for knowledge",
                "It prevents improvement",
            ],
            "correct_answer": "It helps reinforce understanding",
        },
        {
            "question": f"What is a good way to remember important concepts in {topic}?",
            "options": [
                "Review and apply them regularly",
                "Read them only once",
                "Ignore examples",
                "Avoid practicing",
            ],
            "correct_answer": "Review and apply them regularly",
        },
        {
            "question": f"What should you do if a concept in {topic} is difficult?",
            "options": [
                "Break it into smaller parts and practice",
                "Give up immediately",
                "Ignore the concept",
                "Avoid asking questions",
            ],
            "correct_answer": "Break it into smaller parts and practice",
        },
        {
            "question": f"Which activity can help test your understanding of {topic}?",
            "options": [
                "Answering practice questions",
                "Avoiding all questions",
                "Skipping revision",
                "Only reading the title",
            ],
            "correct_answer": "Answering practice questions",
        },
        {
            "question": f"What is an effective learning habit for {topic}?",
            "options": [
                "Consistent learning and revision",
                "Studying only once",
                "Never reviewing mistakes",
                "Avoiding practice",
            ],
            "correct_answer": "Consistent learning and revision",
        },
        {
            "question": f"How can examples help when learning {topic}?",
            "options": [
                "They connect concepts with practical situations",
                "They make concepts impossible to understand",
                "They remove the need for practice",
                "They have no learning value",
            ],
            "correct_answer": "They connect concepts with practical situations",
        },
        {
            "question": f"What is the best way to improve your knowledge of {topic}?",
            "options": [
                "Learn, practice, review, and correct mistakes",
                "Only memorize the topic name",
                "Avoid difficult questions",
                "Never review what you learned",
            ],
            "correct_answer": "Learn, practice, review, and correct mistakes",
        },
    ]


def generate_quiz(passage: str) -> list:
    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 10 multiple-choice questions from the following topic or passage.

Content:
{passage}

Return ONLY valid JSON in this exact shape:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Exactly one option from the options list"
  }}
]

Rules:
- Exactly 10 questions.
- Exactly 4 options per question.
- Every question must be relevant to the supplied topic or passage.
- Questions should test understanding, not only simple memorization.
- Include plausible but incorrect distractors.
- Do not repeat the same question.
- The correct answer must exactly match one of the four options.
- Do not add Markdown fences.
- Do not add explanations outside the JSON.
"""

    result = generate_text(prompt)

    if not result:
        return []

    try:
        data = json.loads(clean_json_block(result))

        if isinstance(data, list):
            return data

    except json.JSONDecodeError:
        pass

    return []
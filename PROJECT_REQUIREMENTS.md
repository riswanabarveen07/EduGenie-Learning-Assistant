# PROJECT REQUIREMENTS

## EduGenie: Google Gemini Powered Learning Assistant

This document translates the supplied EduGenie specification into the current working project.

## Project Description

EduGenie is a lightweight AI-powered educational assistant that simplifies learning through generative AI. It supports:

- Ask questions and receive smart, concise answers
- Understand complex concepts through simplified explanations
- Generate quizzes from topics or text
- Receive personalized learning recommendations
- Summarize large educational passages

The backend uses FastAPI. The frontend uses HTML/CSS with Jinja2 templates.

## Scenarios

### Scenario 1
A student asks: “Which is the largest ocean?” The QnA module returns an educational answer.

### Scenario 2
A student enters “The Pythagoras Theorem” and generates a quiz containing three MCQs with four options each. Selecting a wrong option reveals the correct answer.

### Scenario 3
A learner exploring SQL requests a structured path from beginner to advanced, with timelines, stepwise guidance, practice, and resource types.

## Prerequisites

- Python 3.10+
- FastAPI
- HTML and CSS
- Google Gemini API key
- Uvicorn
- Jinja2

Install:

```bash
python -m pip install -r requirements.txt
```

## Gemini API Key

Keep the key in `.env`:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

The model is configurable through the environment rather than hard-coded so the implementation can be updated when model availability changes.

## Milestone 1 — Model Selection and Architecture

The supplied specification names:

- Gemini 1.5 Pro via API for Q&A, summarization, quiz generation, and learning paths.
- LaMini-Flan-T5-783M locally for concept explanation.

In this implementation:

- Gemini model selection is controlled by `GEMINI_MODEL`.
- `explanation_module.py` contains an optional LaMini-Flan-T5-783M local backend.
- When the optional local-model dependencies are not available, the explanation feature uses Gemini as the working fallback.

## Folder Architecture

```text
EduGenie/
├── app/
│   ├── main.py
│   ├── gemini_client.py
│   ├── explanation_module.py
│   ├── qna.py
│   ├── quiz_module.py
│   ├── summary_module.py
│   └── learning_path.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── result.html
├── static/
│   └── style.css
├── .env.example
├── .gitignore
├── README.md
├── PROJECT_REQUIREMENTS.md
└── requirements.txt
```

## Milestone 2 — Core Functionalities

### Explanation Module

The explanation feature breaks complex concepts into:

- A simple definition
- Key points
- Important terms
- Practical examples where useful

### QnA Module

The QnA feature:

- Accepts an academic or general-knowledge question
- Uses a structured Gemini prompt
- Returns a direct educational answer
- Keeps language simple and readable

### Quiz Module

The quiz feature:

- Generates exactly three questions
- Provides four options per question
- Provides the correct answer
- Requests valid JSON
- Cleans Markdown code fences before JSON parsing
- Uses a fallback quiz if AI generation is unavailable
- Provides browser-based correction after an option is selected

### Summary Module

The summary feature:

- Keeps important facts and ideas
- Removes repetition
- Uses concise, clear language
- Supports long educational passages

### Learning Path Module

The recommendation feature:

- Covers beginner, intermediate, and advanced stages
- Provides suggested timelines
- Gives stepwise learning activities
- Includes practice ideas
- Mentions prerequisites when relevant
- Suggests documentation, videos, articles, and books without inventing URLs
- Ends with a practical mini-project or assessment

## Milestone 2.2 — Backend API with FastAPI

Required feature endpoints:

```text
POST /qa
POST /explain
POST /quiz
POST /summarize
POST /learn/recommendations
```

Additional:

```text
GET /health
POST /api/qa
POST /api/explain
POST /api/quiz
POST /api/summarize
POST /api/learn/recommendations
```

## Milestone 3 — Frontend Development

The web interface contains:

- Task dropdown: Explain, QnA, Quiz, Summary, Recommend Path
- Text area for user input
- Submit button
- Responsive design
- Result container

## Milestone 3.2 — Live Integration

The selected task maps to a FastAPI endpoint. The response is rendered on the result page.

## Milestone 4 — Local Deployment

Run:

```bash
python -m uvicorn app.main:app --reload
```

Navigate to:

```text
http://127.0.0.1:8000
```

## Functional Testing

Test:

- Ask a question
- Get an explanation
- Generate a quiz
- Select quiz answers and verify correction
- Summarize content
- Get personalized learning recommendations

## Future Enhancements

The supplied specification also identifies these future directions:

- Voice-based interaction
- Multilingual support
- Mobile application
- Progress tracking dashboards
- Gamification
- Adaptive learning paths
- Group study sessions
- Teacher/parent dashboards
- LMS integration such as Moodle or Google Classroom
- Image and PDF input
- Smart notifications

These are kept as future enhancements rather than being presented as completed features.

## Conclusion

The current project implements the requested five learning workflows in a modular FastAPI application: QnA, simplified explanation, quiz generation, summarization, and learning recommendations.

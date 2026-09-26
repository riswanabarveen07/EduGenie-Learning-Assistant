# EduGenie: Google Gemini Powered Learning Assistant

## Project Description

EduGenie is a lightweight AI-powered educational assistant that simplifies learning through generative AI. Designed for students of different academic levels, it provides:

- Question answering with concise responses
- Simplified concept explanations
- Quiz generation from topics or text
- Personalized learning recommendations
- Summarization of educational passages

Built with FastAPI for the backend and HTML/CSS with Jinja2 templates for the frontend.

## Scenarios

**Scenario 1 — QnA:** A student asks, “Which is the largest ocean?”

**Scenario 2 — Quiz:** A student enters “The Pythagoras Theorem” and generates a three-question MCQ quiz with four options per question.

**Scenario 3 — Learning Path:** A learner exploring SQL requests a beginner-to-advanced learning path with timelines, practice steps, and resource types.

## Architecture

```text
Browser
  |
  v
FastAPI (app/main.py)
  |
  +--> /qa ----------------------> qna.py
  +--> /explain -----------------> explanation_module.py
  +--> /quiz --------------------> quiz_module.py
  +--> /summarize ---------------> summary_module.py
  +--> /learn/recommendations ---> learning_path.py
  |
  +--> gemini_client.py ----------> Google Gemini API
```

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
├── PROJECT_REQUIREMENTS.md
├── README.md
└── requirements.txt
```

## Prerequisites

- Python 3.10+
- FastAPI
- Uvicorn
- Jinja2
- Google Gemini API key

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create `.env` from `.env.example` and add your API key:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Never commit `.env`.

## Run Locally

```bash
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Backend Endpoints

| Endpoint | Purpose |
|---|---|
| `POST /qa` | Question answering |
| `POST /explain` | Simplified concept explanation |
| `POST /quiz` | Three MCQs with four options each |
| `POST /summarize` | Educational passage summarization |
| `POST /learn/recommendations` | Structured beginner-to-advanced learning path |
| `GET /health` | Health check |

## Core Modules

### Explanation Module
Provides beginner-friendly concept explanations. The code also contains an optional local integration path for **LaMini-Flan-T5-783M**, enabled with `USE_LOCAL_LAMINI=true` when its optional dependencies are installed.

### QnA Module
Sends a structured learning prompt to Gemini and returns a clear answer with simple context and examples where useful.

### Quiz Module
Requests exactly three MCQs in JSON. Each question has four options and a correct answer. The parser removes Markdown code fences before loading JSON. The web page also corrects the user's choice immediately.

### Summary Module
Produces concise revision material while preserving the important facts and ideas from the supplied educational text.

### Learning Path Module
Generates beginner, intermediate, and advanced learning stages with suggested timelines, practice activities, prerequisites, resource types, and a final project/assessment.

## Frontend

The main page contains the requested task dropdown:

- Explain
- QnA
- Quiz
- Summary
- Recommend Path

A text area accepts the topic or source passage. The selected task is mapped to the corresponding FastAPI endpoint and the generated output is shown on a result page.

## Security

The real Gemini key belongs in `.env`. `.gitignore` prevents `.env` from being tracked.

Use `.env.example` only as a safe template. Never put a real API key into Python source code, README files, or screenshots.

## Testing Checklist

- Ask a question
- Explain a topic
- Generate 3 MCQs with 4 options each
- Select an answer and verify correction
- Summarize a long passage
- Generate a beginner-to-advanced learning path
- Open `/health`
- Verify `.env` is not tracked

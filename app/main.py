import logging
from pathlib import Path

import markdown
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.explanation_module import generate_explanation
from app.gemini_client import GeminiServiceError
from app.learning_path import get_learning_recommendations
from app.qna import answer_question
from app.quiz_module import fallback_quiz, generate_quiz
from app.summary_module import summarize_text


# =========================================
# LOGGING
# =========================================

logger = logging.getLogger("edugenie")


# =========================================
# BASE DIRECTORY & ENVIRONMENT
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# =========================================
# FASTAPI APP
# =========================================

app = FastAPI(
    title="EduGenie: Google Gemini Powered Learning Assistant",
    description=(
        "A lightweight AI-powered educational assistant "
        "built with FastAPI and Google Gemini."
    ),
    version="1.0.0",
)


# =========================================
# STATIC FILES & TEMPLATES
# =========================================

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# =========================================
# MARKDOWN → HTML
# =========================================

def to_html(text: str) -> str:
    """
    Convert Markdown text into HTML for normal
    AI responses such as QnA, explanation, summary,
    and learning path.
    """

    if not text:
        return ""

    return markdown.markdown(
        str(text),
        extensions=[
            "fenced_code",
            "tables",
            "nl2br",
        ],
    )


# =========================================
# COMMON RESULT RENDERER
# =========================================

def render_result(
    request: Request,
    task: str,
    title: str,
    source: str,
    content,
    is_quiz: bool = False,
    source_type: str = "ai",
):
    """
    Render the common result page.

    Quiz content is passed as structured Python data.
    Other content is converted from Markdown to HTML.
    """

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "task": task,
            "title": title,
            "source": source,
            "prompt": source,
            "content": (
                content
                if is_quiz
                else to_html(content)
            ),
            "is_quiz": is_quiz,
            "has_error": False,
            "source_type": source_type,
        },
    )


# =========================================
# QUIZ DATA PREPARATION
# =========================================

def prepare_quiz_data(quiz_data: list) -> list:
    """
    Convert quiz data into one consistent structure
    expected by result.html.

    Supported input formats:

    New format:
        {
            "question": "...",
            "options": [
                {
                    "value": "A",
                    "label": "...",
                    "feedback": ""
                }
            ],
            "correctValues": ["A"]
        }

    Old format:
        {
            "question": "...",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option A"
        }
    """

    cleaned = []

    if not isinstance(quiz_data, list):
        return cleaned

    # -----------------------------------------
    # MAXIMUM 10 QUESTIONS
    # -----------------------------------------

    quiz_data = quiz_data[:10]

    for index, item in enumerate(quiz_data):

        if not isinstance(item, dict):
            continue

        # -----------------------------------------
        # QUESTION
        # -----------------------------------------

        question = str(
            item.get(
                "question",
                f"Question {index + 1}",
            )
        ).strip()

        if not question:
            question = f"Question {index + 1}"

        # -----------------------------------------
        # OPTIONS
        # -----------------------------------------

        options = item.get(
            "options",
            [],
        )

        if not isinstance(options, list):
            options = []

        cleaned_options = []

        for option_index, option in enumerate(
            options[:4]
        ):

            # -----------------------------
            # NEW OPTION FORMAT
            # -----------------------------

            if isinstance(option, dict):

                value = str(
                    option.get(
                        "value",
                        chr(65 + option_index),
                    )
                ).strip()

                label = str(
                    option.get(
                        "label",
                        option.get(
                            "text",
                            option.get(
                                "value",
                                "Not provided",
                            ),
                        ),
                    )
                ).strip()

                feedback = str(
                    option.get(
                        "feedback",
                        "",
                    )
                ).strip()

            # -----------------------------
            # OLD OPTION FORMAT
            # -----------------------------

            else:

                value = chr(
                    65 + option_index
                )

                label = str(option).strip()

                feedback = ""

            # ---------------------------------
            # NORMALIZE EMPTY LABEL
            # ---------------------------------

            if not label:
                label = "Not provided"

            cleaned_options.append(
                {
                    "value": value,
                    "label": label,
                    "feedback": feedback,
                }
            )

        # -----------------------------------------
        # ENSURE EXACTLY 4 OPTIONS
        # -----------------------------------------

        while len(cleaned_options) < 4:

            next_letter = chr(
                65 + len(cleaned_options)
            )

            cleaned_options.append(
                {
                    "value": next_letter,
                    "label": "Not provided",
                    "feedback": "",
                }
            )

        # -----------------------------------------
        # CORRECT VALUES
        # -----------------------------------------

        correct_values = item.get(
            "correctValues",
            [],
        )

        if not isinstance(
            correct_values,
            list,
        ):
            correct_values = [
                correct_values
            ]

        correct_values = [
            str(value).strip()
            for value in correct_values
            if str(value).strip()
        ]

        # -----------------------------------------
        # OLD FORMAT COMPATIBILITY
        # -----------------------------------------

        if not correct_values:

            old_correct = item.get(
                "correct_answer",
                "",
            )

            if old_correct:

                old_correct = str(
                    old_correct
                ).strip()

                for option in cleaned_options:

                    option_value = (
                        option["value"]
                        .strip()
                        .lower()
                    )

                    option_label = (
                        option["label"]
                        .strip()
                        .lower()
                    )

                    old_correct_normalized = (
                        old_correct.lower()
                    )

                    if (
                        option_value
                        == old_correct_normalized
                        or
                        option_label
                        == old_correct_normalized
                    ):

                        correct_values = [
                            option["value"]
                        ]

                        break

        # -----------------------------------------
        # IF CORRECT ANSWER IS A LETTER
        # -----------------------------------------

        if not correct_values:

            old_correct = item.get(
                "correct_answer",
                "",
            )

            if old_correct:

                old_correct = (
                    str(old_correct)
                    .strip()
                    .upper()
                )

                if old_correct in ["A", "B", "C", "D"]:

                    correct_values = [
                        old_correct
                    ]

        # -----------------------------------------
        # FINAL QUESTION OBJECT
        # -----------------------------------------

        cleaned.append(
            {
                "id": str(
                    item.get(
                        "id",
                        f"q{index + 1}",
                    )
                ),

                "question": question,

                "type": str(
                    item.get(
                        "type",
                        "single_select",
                    )
                ),

                "options": cleaned_options,

                "correctValues": correct_values,

                "hint": str(
                    item.get(
                        "hint",
                        "",
                    )
                ),
            }
        )

    return cleaned


# =========================================
# HOME
# =========================================

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
        },
    )


# =========================================
# EXPLAIN - GET
# =========================================

@app.get(
    "/explain",
    response_class=HTMLResponse,
)
async def explain_get(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
        },
    )


# =========================================
# QnA
# =========================================

@app.post(
    "/qa",
    response_class=HTMLResponse,
)
async def qa(
    request: Request,
    text: str = Form(...),
):

    text = text.strip()

    answer = answer_question(text)

    return render_result(
        request,
        "QnA",
        "Your question is answered",
        text,
        answer,
        is_quiz=False,
        source_type="ai",
    )


# =========================================
# CONCEPT EXPLANATION
# =========================================

@app.post(
    "/explain",
    response_class=HTMLResponse,
)
async def explain(
    request: Request,
    topic: str = Form(default=""),
):

    topic = topic.strip()

    # -----------------------------------------
    # NO TOPIC ENTERED
    # -----------------------------------------

    if not topic:

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "title": "Concept Explained Simply",
                "task": "CONCEPT EXPLANATION",
                "source": "",
                "prompt": "",
                "content": None,
                "is_quiz": False,
                "has_error": True,
                "error_title": "No concept entered",
                "error_message": (
                    "Please enter a concept to explain."
                ),
            },
        )

    try:

        # -----------------------------------------
        # GENERATE EXPLANATION
        # -----------------------------------------

        result = generate_explanation(topic)

        # -----------------------------------------
        # NEW DICTIONARY FORMAT
        # -----------------------------------------

        if isinstance(result, dict):

            content = result.get(
                "content",
                "",
            )

            source_type = result.get(
                "source",
                "ai",
            )

        # -----------------------------------------
        # OLD STRING FORMAT
        # -----------------------------------------

        else:

            content = result
            source_type = "ai"

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "title": "Concept Explained Simply",
                "task": "CONCEPT EXPLANATION",
                "source": topic,
                "prompt": topic,
                "content": to_html(content),
                "is_quiz": False,
                "has_error": False,
                "source_type": source_type,
            },
        )

    # -----------------------------------------
    # GEMINI SERVICE ERROR
    # -----------------------------------------

    except GeminiServiceError as exc:

        logger.warning(
            "Gemini explanation error: %s",
            exc,
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "title": "Concept Explained Simply",
                "task": "CONCEPT EXPLANATION",
                "source": topic,
                "prompt": topic,
                "content": None,
                "is_quiz": False,
                "has_error": True,
                "error_title": (
                    "AI service temporarily unavailable"
                ),
                "error_message": getattr(
                    exc,
                    "message",
                    str(exc),
                ),
            },
            status_code=503,
        )

    # -----------------------------------------
    # UNEXPECTED ERROR
    # -----------------------------------------

    except Exception as exc:

        logger.exception(
            "Unexpected explanation route error: %s",
            exc,
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "title": "Concept Explained Simply",
                "task": "CONCEPT EXPLANATION",
                "source": topic,
                "prompt": topic,
                "content": None,
                "is_quiz": False,
                "has_error": True,
                "error_title": "Something went wrong",
                "error_message": (
                    "EduGenie could not generate this "
                    "explanation. Please try again."
                ),
            },
            status_code=500,
        )


# =========================================
# QUIZ
# =========================================

@app.post(
    "/quiz",
    response_class=HTMLResponse,
)
async def quiz(
    request: Request,
    text: str = Form(...),
):

    text = text.strip()

    # -----------------------------------------
    # EMPTY INPUT
    # -----------------------------------------

    if not text:

        quiz_data = fallback_quiz(
            "the topic"
        )

        cleaned = prepare_quiz_data(
            quiz_data
        )

        return render_result(
            request,
            "Quiz",
            "Test your understanding",
            text,
            cleaned,
            is_quiz=True,
            source_type="local",
        )

    # -----------------------------------------
    # TRY GEMINI
    # -----------------------------------------

    try:

        quiz_data = generate_quiz(text)

    except GeminiServiceError as exc:

        # Gemini quota/service problem.
        # Fall back to local quiz data.

        logger.warning(
            "Gemini quiz unavailable. "
            "Using fallback quiz. Reason: %s",
            exc,
        )

        quiz_data = []

    except Exception as exc:

        logger.exception(
            "Unexpected quiz generation error: %s",
            exc,
        )

        quiz_data = []

    # -----------------------------------------
    # REQUIRE 10 QUESTIONS
    # -----------------------------------------

    if (
        not isinstance(quiz_data, list)
        or len(quiz_data) < 10
    ):

        logger.warning(
            "Quiz returned fewer than 10 questions. "
            "Using fallback quiz."
        )

        quiz_data = fallback_quiz(text)

        source_type = "local"

    else:

        source_type = "ai"

    # -----------------------------------------
    # PREPARE QUIZ DATA
    # -----------------------------------------

    cleaned = prepare_quiz_data(
        quiz_data
    )

    # -----------------------------------------
    # FINAL SAFETY CHECK
    # -----------------------------------------

    if len(cleaned) < 10:

        logger.warning(
            "Prepared quiz contains fewer than 10 "
            "valid questions. Using fallback quiz."
        )

        cleaned = prepare_quiz_data(
            fallback_quiz(text)
        )

        source_type = "local"

    # -----------------------------------------
    # MAXIMUM 10
    # -----------------------------------------

    cleaned = cleaned[:10]

    return render_result(
        request,
        "Quiz",
        "Test your understanding",
        text,
        cleaned,
        is_quiz=True,
        source_type=source_type,
    )


# =========================================
# SUMMARY
# =========================================

@app.post(
    "/summarize",
    response_class=HTMLResponse,
)
async def summarize(
    request: Request,
    text: str = Form(...),
):

    text = text.strip()

    summary = summarize_text(text)

    return render_result(
        request,
        "Summary",
        "A concise version of your passage",
        text,
        summary,
        is_quiz=False,
        source_type="ai",
    )


# =========================================
# LEARNING PATH
# =========================================

@app.post(
    "/learn/recommendations",
    response_class=HTMLResponse,
)
async def learn_recommendations(
    request: Request,
    text: str = Form(...),
):

    text = text.strip()

    try:

        recommendations = get_learning_recommendations(
            text
        )

        return render_result(
            request,
            "Recommend Path",
            "Your learning path",
            text,
            recommendations,
            is_quiz=False,
            source_type="ai",
        )

    except GeminiServiceError as exc:

        logger.warning(
            "Gemini learning path error: %s",
            exc,
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "title": "Your learning path",
                "task": "Recommend Path",
                "source": text,
                "prompt": text,
                "content": None,
                "is_quiz": False,
                "has_error": True,
                "error_title": (
                    "Gemini request limit reached"
                ),
                "error_message": (
                    "The Gemini API request limit has "
                    "been reached temporarily. Please "
                    "try this feature again after the "
                    "quota becomes available."
                ),
                "source_type": "ai",
            },
            status_code=503,
        )

    except Exception as exc:

        logger.exception(
            "Unexpected learning path error: %s",
            exc,
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "title": "Your learning path",
                "task": "Recommend Path",
                "source": text,
                "prompt": text,
                "content": None,
                "is_quiz": False,
                "has_error": True,
                "error_title": "Something went wrong",
                "error_message": (
                    "EduGenie could not generate your "
                    "learning path right now."
                ),
                "source_type": "ai",
            },
            status_code=500,
        )

# =========================================
# HEALTH CHECK
# =========================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "app": "EduGenie",
    }


# =========================================
# API - QnA
# =========================================

@app.post("/api/qa")
async def api_qa(
    text: str = Form(...),
):

    return {
        "answer": answer_question(text)
    }


# =========================================
# API - EXPLANATION
# =========================================

@app.post("/api/explain")
async def api_explain(
    text: str = Form(...),
):

    return {
        "explanation": generate_explanation(text)
    }


# =========================================
# API - QUIZ
# =========================================

@app.post("/api/quiz")
async def api_quiz(
    text: str = Form(...),
):

    try:

        quiz_data = generate_quiz(text)

    except GeminiServiceError as exc:

        logger.warning(
            "Gemini API quiz error. "
            "Using fallback quiz: %s",
            exc,
        )

        quiz_data = []

    except Exception as exc:

        logger.exception(
            "Unexpected API quiz error: %s",
            exc,
        )

        quiz_data = []

    # -----------------------------------------
    # FALLBACK IF LESS THAN 10
    # -----------------------------------------

    if (
        not isinstance(quiz_data, list)
        or len(quiz_data) < 10
    ):

        quiz_data = fallback_quiz(text)

    return {
        "quiz": quiz_data[:10]
    }


# =========================================
# API - SUMMARY
# =========================================

@app.post("/api/summarize")
async def api_summarize(
    text: str = Form(...),
):

    return {
        "summary": summarize_text(text)
    }


# =========================================
# API - LEARNING PATH
# =========================================

@app.post(
    "/api/learn/recommendations"
)
async def api_learning_path(
    text: str = Form(...),
):

    return {
        "recommendations": (
            get_learning_recommendations(text)
        )
    }

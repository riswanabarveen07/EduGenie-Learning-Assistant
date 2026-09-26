import logging

from .gemini_client import generate_text, GeminiServiceError


logger = logging.getLogger("edugenie.explanation")


# =========================================================
# OPTIONAL LOCAL LAMINI DEPENDENCIES
# =========================================================

try:
    from transformers import pipeline
    LAMINI_AVAILABLE = True

except ImportError:
    pipeline = None
    LAMINI_AVAILABLE = False


# =========================================================
# CONFIGURATION
# =========================================================

USE_LOCAL_LAMINI = True

_lamini_pipeline = None


# =========================================================
# LOCAL LAMINI
# =========================================================

def _get_lamini_pipeline():

    global _lamini_pipeline

    if not LAMINI_AVAILABLE:
        return None

    if _lamini_pipeline is not None:
        return _lamini_pipeline

    try:

        logger.info("Loading local LaMini model...")

        _lamini_pipeline = pipeline(
            "text2text-generation",
            model="MBZUAI/LaMini-Flan-T5-783M"
        )

        logger.info("Local LaMini model loaded successfully.")

        return _lamini_pipeline

    except Exception as exc:

        logger.warning(
            "Local LaMini model could not be loaded: %s",
            exc,
        )

        _lamini_pipeline = None

        return None


def _local_lamini_explanation(topic):

    if not LAMINI_AVAILABLE:
        return None

    model = _get_lamini_pipeline()

    if model is None:
        return None

    try:

        prompt = (
            "Explain the following concept in simple language for a student. "
            "Use short paragraphs and examples where useful. "
            f"Concept: {topic}"
        )

        result = model(
            prompt,
            max_new_tokens=300,
            do_sample=False,
        )

        if not result:
            return None

        generated_text = result[0].get("generated_text")

        if not generated_text:
            return None

        return generated_text.strip()

    except Exception as exc:

        logger.warning(
            "Local LaMini generation failed: %s",
            exc,
        )

        return None


# =========================================================
# PUBLIC EXPLANATION FUNCTION
# =========================================================

def generate_explanation(topic):

    topic = (topic or "").strip()

    if not topic:
        raise ValueError("Please enter a concept to explain.")

    # -----------------------------------------------------
    # 1. Try local LaMini first
    # -----------------------------------------------------

    if USE_LOCAL_LAMINI:

        local_result = _local_lamini_explanation(topic)

        if local_result:
            logger.info(
                "Explanation generated using local LaMini."
            )

            return {
                "content": local_result,
                "source": "local",
                "error": False,
            }

    # -----------------------------------------------------
    # 2. Gemini fallback
    # -----------------------------------------------------

    prompt = f"""
You are EduGenie, an AI learning assistant.

Explain the following concept to a student in very simple,
clear and easy-to-understand language.

Concept:
{topic}

Requirements:
- Start with a simple definition.
- Explain how it works.
- Give a simple real-world example.
- Mention important points.
- Avoid unnecessary technical jargon.
- Use headings and bullet points where helpful.
"""

    try:

        result = generate_text(prompt)

        return {
            "content": result,
            "source": "gemini",
            "error": False,
        }

    except GeminiServiceError:
        raise

    except Exception as exc:

        logger.error(
            "Unexpected explanation error: %s",
            exc,
        )

        raise GeminiServiceError(
            "EduGenie could not generate the explanation. "
            "Please try again."
        ) from exc
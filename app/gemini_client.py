import os
import time
import logging

from dotenv import load_dotenv
from google import genai


load_dotenv()

logger = logging.getLogger("edugenie.gemini")


class GeminiServiceError(Exception):
    """User-friendly Gemini API error."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

MAX_RETRIES = 3
INITIAL_DELAY = 1.5


_client = None


def get_client():
    """
    Create the Gemini client only when needed.
    """

    global _client

    if _client is not None:
        return _client

    if not API_KEY:
        raise GeminiServiceError(
            "Gemini API key is not configured. "
            "Please check your .env file."
        )

    try:
        _client = genai.Client(api_key=API_KEY)
        return _client

    except Exception as exc:
        logger.error("Gemini client initialization failed: %s", exc)

        raise GeminiServiceError(
            "EduGenie could not connect to the Gemini service."
        ) from exc


def _is_retryable_error(exc):
    """
    Determine whether an exception is likely temporary.
    """

    error_text = str(exc).lower()

    retry_keywords = [
        "503",
        "unavailable",
        "high demand",
        "timeout",
        "timed out",
        "deadline exceeded",
        "temporarily unavailable",
        "internal server error",
        "500",
        "502",
        "504",
        "resource exhausted",
        "429",
        "rate limit",
    ]

    return any(keyword in error_text for keyword in retry_keywords)


def _user_friendly_error(exc):
    """
    Convert technical Gemini errors into clean UI messages.
    """

    error_text = str(exc).lower()

    if "503" in error_text or "unavailable" in error_text:
        return (
            "Gemini is temporarily busy right now. "
            "Please try again in a few seconds."
        )

    if (
        "429" in error_text
        or "rate limit" in error_text
        or "resource exhausted" in error_text
    ):
        return (
            "EduGenie has reached the Gemini request limit temporarily. "
            "Please wait a moment and try again."
        )

    if (
        "timeout" in error_text
        or "timed out" in error_text
        or "deadline exceeded" in error_text
    ):
        return (
            "The Gemini request took too long to complete. "
            "Please try again."
        )

    if "401" in error_text or "403" in error_text:
        return (
            "EduGenie could not authenticate with Gemini. "
            "Please check the Gemini API configuration."
        )

    return (
        "EduGenie could not generate a response from Gemini. "
        "Please try again."
    )


def generate_text(prompt):
    """
    Generate text using Gemini Chat API.

    Includes:
    - Chat.send_message()
    - Exponential backoff
    - Retry handling
    - Clean user-facing errors
    """

    client = get_client()

    last_exception = None

    for attempt in range(MAX_RETRIES):

        try:

            logger.info(
                "Gemini request started. attempt=%s/%s model=%s",
                attempt + 1,
                MAX_RETRIES,
                MODEL_NAME,
            )

            # Use Chat API instead of directly calling
            # client.models.generate_content().
            chat = client.chats.create(
                model=MODEL_NAME
            )

            response = chat.send_message(
                message=prompt
            )

            text = getattr(response, "text", None)

            if text and text.strip():
                logger.info("Gemini request completed successfully.")
                return text.strip()

            raise GeminiServiceError(
                "Gemini returned an empty response."
            )

        except GeminiServiceError as exc:
            last_exception = exc

            if attempt < MAX_RETRIES - 1:
                delay = INITIAL_DELAY * (2 ** attempt)

                logger.warning(
                    "Gemini temporary failure. Retrying in %.1f seconds.",
                    delay,
                )

                time.sleep(delay)
                continue

            raise

        except Exception as exc:

            last_exception = exc

            if _is_retryable_error(exc) and attempt < MAX_RETRIES - 1:

                delay = INITIAL_DELAY * (2 ** attempt)

                logger.warning(
                    "Gemini temporary error on attempt %s/%s. "
                    "Retrying in %.1f seconds.",
                    attempt + 1,
                    MAX_RETRIES,
                    delay,
                )

                time.sleep(delay)
                continue

            friendly_message = _user_friendly_error(exc)

            logger.error(
                "Gemini request failed after %s attempt(s): %s",
                attempt + 1,
                exc,
            )

            raise GeminiServiceError(
                friendly_message
            ) from exc

    raise GeminiServiceError(
        "Gemini is temporarily unavailable. Please try again."
    ) from last_exception
import json
from typing import Type

from pydantic import BaseModel

from config import settings


try:

    from google import genai
    from google.genai import types

except ImportError:

    genai = None
    types = None


_client = None


# =========================================================
# Gemini Client
# =========================================================

def get_client():

    global _client

    if _client is not None:
        return _client

    if genai is None:

        raise RuntimeError(
            "google-genai is not installed. "
            "Run: python -m pip install -r requirements.txt"
        )

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add your Gemini API key to .env"
        )

    _client = genai.Client(
        api_key=settings.gemini_api_key
    )

    return _client


# =========================================================
# Normal text generation
# =========================================================

def generate_text(
    prompt: str,
    system_instruction: str | None = None
) -> str:

    client = get_client()

    config = types.GenerateContentConfig(
        temperature=0.4,
        max_output_tokens=4096,
        system_instruction=system_instruction
        if system_instruction
        else None,
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


# =========================================================
# Structured generation
# =========================================================

def generate_structured(
    prompt: str,
    schema: Type[BaseModel],
    system_instruction: str | None = None
) -> BaseModel:

    client = get_client()

    config = types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=4096,
        response_mime_type="application/json",
        response_schema=schema,
        system_instruction=system_instruction
        if system_instruction
        else None,
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config
    )

    parsed = getattr(
        response,
        "parsed",
        None
    )

    if parsed is not None:

        if isinstance(parsed, schema):
            return parsed

        return schema.model_validate(
            parsed
        )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned no structured response."
        )

    cleaned = text.strip()

    if cleaned.startswith("```"):

        cleaned = (
            cleaned
            .replace("```json", "", 1)
            .replace("```", "", 1)
            .strip()
        )

    try:

        data = json.loads(cleaned)

        return schema.model_validate(
            data
        )

    except Exception as exc:

        raise RuntimeError(
            "Unable to parse Gemini response: "
            + str(exc)
        ) from exc
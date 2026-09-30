from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request  # type: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse  # type: ignore[reportMissingImports]
from fastapi.staticfiles import StaticFiles  # type: ignore[reportMissingImports]
from fastapi.templating import Jinja2Templates  # type: ignore[reportMissingImports]
from pydantic import BaseModel, Field

from config import settings
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import create_quiz
from summary_module import summarize_text
from learning_path import create_learning_path


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# =========================================================
# Request Models
# =========================================================

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=settings.max_input_chars
    )


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=settings.max_input_chars
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=settings.max_input_chars
    )

    count: int = Field(
        default=5,
        ge=1,
        le=10
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    level: str = Field(
        default="beginner",
        min_length=1,
        max_length=50
    )

    weeks: int = Field(
        default=4,
        ge=1,
        le=24
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "app_name": settings.app_name,
        "gemini_model": settings.gemini_model,
    }
)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health() -> dict[str, Any]:

    return {
        "status": "ok",
        "application": settings.app_name,
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
        "gemini_model": settings.gemini_model,
        "local_explanation_enabled":
            settings.use_local_explanation,
    }


# =========================================================
# QUESTION & ANSWER
# =========================================================

@app.post("/qa")
async def qa(request: QuestionRequest):

    try:

        answer = answer_question(
            request.question
        )

        return {
            "success": True,
            "result": answer
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# =========================================================
# EXPLANATION
# =========================================================

@app.post("/explain")
async def explain(request: TextRequest):

    try:

        result = explain_concept(
            request.text
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# =========================================================
# QUIZ
# =========================================================

@app.post("/quiz")
async def quiz(request: QuizRequest):

    try:

        result = create_quiz(
            request.text,
            request.count
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# =========================================================
# SUMMARY
# =========================================================

@app.post("/summarize")
async def summary(request: TextRequest):

    try:

        result = summarize_text(
            request.text
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# =========================================================
# LEARNING PATH
# =========================================================

@app.post("/learn/recommendations")
async def learning_path(
    request: LearningPathRequest
):

    try:

        result = create_learning_path(
            topic=request.topic,
            level=request.level,
            weeks=request.weeks
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# =========================================================
# RUN DIRECTLY
# =========================================================

if __name__ == "__main__":

    import importlib

    try:
        uvicorn = importlib.import_module("uvicorn")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "uvicorn is required to run the app. Install it with: pip install uvicorn"
        ) from exc

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
from typing import List

from pydantic import BaseModel, Field

from gemini_service import generate_structured


class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4
    )

    answer: str

    explanation: str


class QuizResponse(BaseModel):

    title: str

    questions: List[QuizQuestion]


def create_quiz(
    text: str,
    count: int = 5
) -> dict:

    prompt = f"""
Create exactly {count} multiple-choice
questions from the study material below.

Rules:

- Create exactly {count} questions.
- Each question must have exactly 4 options.
- Only one option is correct.
- The correct answer must exactly match
  one of the four options.
- Questions must be based on the supplied
  study material.
- Do not introduce unrelated facts.
- Provide an explanation for every answer.

STUDY MATERIAL:

{text}
"""

    response = generate_structured(
        prompt,
        QuizResponse,
        system_instruction="""
You are EduGenie's professional quiz generator.

Create useful educational MCQs for students.

Return only the requested structured data.
"""
    )

    questions = response.questions[:count]

    if len(questions) < count:

        raise RuntimeError(
            "The AI returned fewer questions "
            "than requested."
        )

    return {
        "title": response.title,

        "questions": [
            question.model_dump()
            for question in questions
        ]
    }
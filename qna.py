from gemini_service import generate_text


SYSTEM_INSTRUCTION = """
You are EduGenie, a friendly educational AI assistant.

Your job is to help students understand academic topics.

Rules:
1. Give accurate answers.
2. Use simple English.
3. Explain difficult terminology.
4. Give examples when useful.
5. Do not invent facts.
6. Keep the answer focused.
7. Structure answers clearly.
"""


def answer_question(question: str) -> str:
    """
    Answer a student's academic question using Gemini.
    """

    prompt = f"""
Answer the following student question.

QUESTION:
{question}

Use this structure:

Direct Answer:
Give the answer directly.

Explanation:
Explain the answer in simple language.

Example:
Give one simple example if appropriate.

Key Point:
Give one short revision point.
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM_INSTRUCTION
    )
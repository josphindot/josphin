from gemini_service import generate_text


SYSTEM_INSTRUCTION = """
You are EduGenie's educational summarization assistant.

Your job is to turn long study material
into clear revision notes.

Rules:

1. Do not invent information.
2. Preserve important facts.
3. Preserve definitions.
4. Preserve important relationships.
5. Use simple language.
6. Organize the answer clearly.
"""


def summarize_text(
    text: str
) -> str:

    prompt = f"""
Summarize the following educational material.

STUDY MATERIAL:

{text}

Use this structure:

Overview:
Give a short overview.

Key Points:
List the most important ideas.

Important Terms:
Explain important terms briefly.

Quick Revision:
Give short revision notes.

Remember:
Give 3 important things the student
should remember.
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM_INSTRUCTION
    )
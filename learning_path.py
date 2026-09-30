from gemini_service import generate_text


SYSTEM_INSTRUCTION = """
You are EduGenie's learning-path planner.

Create realistic educational learning plans.

The student should progress from fundamentals
to more advanced concepts.

Make the plan practical and easy to follow.

Do not claim that external resources
have been personally verified.
"""


def create_learning_path(
    topic: str,
    level: str = "beginner",
    weeks: int = 4
) -> str:

    prompt = f"""
Create a {weeks}-week learning path.

Topic:
{topic}

Student Level:
{level}

For each week include:

Week Goal:
...

Topics:
...

Practice:
...

Checkpoint:
...

Also include:

1. Recommended Learning Order
2. Practice Strategy
3. Mini Project Ideas
4. Revision Strategy
5. Progress Checklist
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM_INSTRUCTION
    )
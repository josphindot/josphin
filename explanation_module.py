from config import settings
from gemini_service import generate_text


_local_tokenizer = None
_local_model = None


# =========================================================
# Load local model
# =========================================================

def load_local_model():

    global _local_tokenizer
    global _local_model

    if (
        _local_tokenizer is not None
        and _local_model is not None
    ):

        return (
            _local_tokenizer,
            _local_model
        )

    try:

        from transformers import (
            AutoModelForSeq2SeqLM,
            AutoTokenizer
        )

    except ImportError as exc:

        raise RuntimeError(
            "transformers is not installed."
        ) from exc

    _local_tokenizer = (
        AutoTokenizer.from_pretrained(
            settings.local_explanation_model
        )
    )

    _local_model = (
        AutoModelForSeq2SeqLM.from_pretrained(
            settings.local_explanation_model
        )
    )

    _local_model.eval()

    return (
        _local_tokenizer,
        _local_model
    )


# =========================================================
# Local explanation
# =========================================================

def local_explain(
    concept: str
) -> str:

    tokenizer, model = load_local_model()

    prompt = f"""
Explain this concept to a beginner:

{concept}

Include:

1. Definition
2. Important points
3. Simple example
4. Memory tip
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    output = model.generate(
        **inputs,
        max_new_tokens=250,
        num_beams=4,
        no_repeat_ngram_size=3
    )

    return tokenizer.decode(
        output[0],
        skip_special_tokens=True
    ).strip()


# =========================================================
# Public function
# =========================================================

def explain_concept(
    concept: str
) -> str:

    # Use local model only when explicitly enabled.
    if settings.use_local_explanation:

        try:

            result = local_explain(
                concept
            )

            if result:
                return result

        except Exception:

            # If local model fails,
            # fall back to Gemini.
            pass

    return generate_text(

        f"""
Explain the following concept
to a beginner:

{concept}

Provide:

1. Simple Definition
2. Why It Matters
3. Important Points
4. Simple Example
5. Memory Tip
""",

        system_instruction="""
You are an excellent teacher.

Explain academic concepts clearly,
accurately and in beginner-friendly language.
"""
    )
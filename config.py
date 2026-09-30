import os

from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency in some environments
    def load_dotenv(*args, **kwargs):
        return False


load_dotenv()


def get_bool(
    value: str | None,
    default: bool = False
) -> bool:

    if value is None:
        return default

    return value.strip().lower() in {
        "true",
        "1",
        "yes",
        "on"
    }


@dataclass(frozen=True)
class Settings:

    app_name: str = os.getenv(
        "APP_NAME",
        "EduGenie"
    )

    host: str = os.getenv(
        "HOST",
        "127.0.0.1"
    )

    port: int = int(
        os.getenv(
            "PORT",
            "8000"
        )
    )

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    ).strip()

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    ).strip()

    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    ).strip()

    use_local_explanation: bool = get_bool(
        os.getenv(
            "USE_LOCAL_EXPLANATION"
        ),
        False
    )

    max_input_chars: int = int(
        os.getenv(
            "MAX_INPUT_CHARS",
            "30000"
        )
    )


settings = Settings()
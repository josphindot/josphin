# EduGenie

EduGenie is a Google Gemini powered AI learning assistant.

It provides:

- Question and Answer
- Concept Explanation
- Quiz Generation
- Text Summarization
- Personalized Learning Paths

## Technology

Backend:

- Python
- FastAPI
- Pydantic

AI:

- Google Gemini API
- Optional LaMini-Flan-T5

Frontend:

- HTML
- CSS
- JavaScript
- Jinja2

---

# Project Structure

```text
EduGenie/

main.py
config.py
gemini_service.py
explanation_module.py
qna.py
quiz_module.py
summary_module.py
learning_path.py

requirements.txt
.env
.env.example
.gitignore
README.md
test_smoke.py

templates/
    index.html

static/
    style.css
    app.js
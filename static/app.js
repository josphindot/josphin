const task =
    document.getElementById("task");

const inputText =
    document.getElementById("inputText");

const runButton =
    document.getElementById("runButton");

const clearButton =
    document.getElementById("clearButton");

const copyButton =
    document.getElementById("copyButton");

const resultSection =
    document.getElementById("resultSection");

const result =
    document.getElementById("result");

const statusBox =
    document.getElementById("status");

const countField =
    document.getElementById("countField");

const levelField =
    document.getElementById("levelField");

const weeksField =
    document.getElementById("weeksField");

const count =
    document.getElementById("count");

const level =
    document.getElementById("level");

const weeks =
    document.getElementById("weeks");


let latestResult = "";


// =========================================================
// HTML escaping
// =========================================================

function escapeHtml(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );
}


// =========================================================
// Update UI based on selected task
// =========================================================

function updateControls() {

    const selected =
        task.value;


    countField.classList.toggle(
        "hidden",
        selected !== "quiz"
    );


    levelField.classList.toggle(
        "hidden",
        selected !== "learn"
    );


    weeksField.classList.toggle(
        "hidden",
        selected !== "learn"
    );


    const placeholders = {

        qa:
            "Example: What is artificial intelligence?",

        explain:
            "Example: Explain object-oriented programming.",

        quiz:
            "Paste your study material here.",

        summarize:
            "Paste the text you want to summarize.",

        learn:
            "Example: Python Programming"

    };


    inputText.placeholder =
        placeholders[selected];
}


// =========================================================
// Status
// =========================================================

function setStatus(
    message,
    type = ""
) {

    statusBox.textContent =
        message;

    statusBox.className =
        `status ${type}`;
}


// =========================================================
// Render normal text
// =========================================================

function renderText(text) {

    latestResult = text;

    result.innerHTML = `
        <div class="result-text">
            ${escapeHtml(text)}
        </div>
    `;
}


// =========================================================
// Render quiz
// =========================================================

function renderQuiz(data) {

    const questions =
        data.questions || [];


    latestResult =
        JSON.stringify(
            data,
            null,
            2
        );


    let html = "";


    html += `
        <h2>
            ${escapeHtml(
                data.title ||
                "EduGenie Quiz"
            )}
        </h2>
    `;


    questions.forEach(
        (question, index) => {

            html += `
                <div
                    class="quiz-question"
                >

                    <h3>
                        ${index + 1}.
                        ${escapeHtml(
                            question.question
                        )}
                    </h3>
            `;


            question.options.forEach(
                (option, optionIndex) => {

                    const letter =
                        String.fromCharCode(
                            65 + optionIndex
                        );


                    html += `
                        <label class="option">

                            <input
                                type="radio"
                                name="question-${index}"
                            >

                            <span>
                                <strong>
                                    ${letter}.
                                </strong>

                                ${escapeHtml(
                                    option
                                )}
                            </span>

                        </label>
                    `;

                }
            );


            html += `

                <div class="answer">

                    <strong>
                        Correct Answer:
                    </strong>

                    ${escapeHtml(
                        question.answer
                    )}

                    <br><br>

                    <strong>
                        Explanation:
                    </strong>

                    ${escapeHtml(
                        question.explanation
                    )}

                </div>

                </div>

            `;

        }
    );


    result.innerHTML =
        html;
}


// =========================================================
// Run selected task
// =========================================================

async function runTask() {

    const text =
        inputText.value.trim();


    if (!text) {

        setStatus(
            "Please enter something first.",
            "error"
        );

        return;
    }


    let endpoint;

    let body;


    switch (task.value) {


        case "qa":

            endpoint = "/qa";

            body = {
                question: text
            };

            break;


        case "explain":

            endpoint = "/explain";

            body = {
                text: text
            };

            break;


        case "quiz":

            endpoint = "/quiz";

            body = {
                text: text,

                count:
                    Number(
                        count.value
                    )
            };

            break;


        case "summarize":

            endpoint = "/summarize";

            body = {
                text: text
            };

            break;


        case "learn":

            endpoint =
                "/learn/recommendations";

            body = {

                topic: text,

                level:
                    level.value,

                weeks:
                    Number(
                        weeks.value
                    )
            };

            break;


        default:

            return;
    }


    runButton.disabled =
        true;

    runButton.textContent =
        "Generating...";


    setStatus(
        "EduGenie is generating your answer..."
    );


    resultSection.classList.remove(
        "hidden"
    );


    try {

        const response =
            await fetch(
                endpoint,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(body)
                }
            );


        let data;


        try {

            data =
                await response.json();

        } catch {

            throw new Error(
                "Server returned an invalid response."
            );
        }


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "The request failed."
            );
        }


        if (
            task.value === "quiz"
        ) {

            renderQuiz(
                data.result
            );

        } else {

            renderText(
                data.result
            );

        }


        setStatus(
            "Completed successfully.",
            "success"
        );


        resultSection.scrollIntoView({
            behavior: "smooth"
        });


    } catch (error) {

        result.innerHTML = "";

        setStatus(
            error.message ||
            "Something went wrong.",
            "error"
        );


    } finally {

        runButton.disabled =
            false;

        runButton.textContent =
            "Generate Result";
    }
}


// =========================================================
// Clear
// =========================================================

function clearAll() {

    inputText.value = "";

    result.innerHTML = "";

    latestResult = "";

    resultSection.classList.add(
        "hidden"
    );

    setStatus("");
}


// =========================================================
// Copy
// =========================================================

async function copyResult() {

    if (!latestResult) {

        setStatus(
            "There is no result to copy.",
            "error"
        );

        return;
    }


    try {

        await navigator.clipboard.writeText(
            latestResult
        );

        setStatus(
            "Result copied successfully.",
            "success"
        );

    } catch {

        setStatus(
            "Could not copy the result.",
            "error"
        );
    }
}


// =========================================================
// Event listeners
// =========================================================

task.addEventListener(
    "change",
    updateControls
);


runButton.addEventListener(
    "click",
    runTask
);


clearButton.addEventListener(
    "click",
    clearAll
);


copyButton.addEventListener(
    "click",
    copyResult
);


// =========================================================
// Initial UI
// =========================================================

updateControls();
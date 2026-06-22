const form = document.querySelector("#calculator-form");
const queryInput = document.querySelector("#query");
const submitButton = document.querySelector("#submit-button");
const result = document.querySelector("#result");
const answerCard = document.querySelector(".answer-card");

const outputs = {
  task: document.querySelector("#task-output"),
  tool: document.querySelector("#tool-output"),
  expression: document.querySelector("#expression-output"),
  answer: document.querySelector("#answer-output"),
  error: document.querySelector("#error-output"),
};

function showResult(data) {
  result.classList.remove("is-empty");
  outputs.task.textContent = data.task;
  outputs.tool.textContent = data.tool;
  outputs.expression.textContent = data.expression || "Not available";
  outputs.answer.textContent = data.error ? "Unable to calculate" : data.answer;
  outputs.error.textContent = data.error || "";
  answerCard.classList.toggle("has-error", Boolean(data.error));
}

async function calculate(query) {
  submitButton.disabled = true;
  submitButton.querySelector("span").textContent = "Thinking…";

  try {
    const response = await fetch("/api/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error("The calculator service could not process this request.");
    }

    showResult(await response.json());
  } catch (error) {
    showResult({
      task: "service error",
      tool: "calculator",
      expression: null,
      answer: null,
      error: error.message,
    });
  } finally {
    submitButton.disabled = false;
    submitButton.querySelector("span").textContent = "Calculate";
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const query = queryInput.value.trim();
  if (query) calculate(query);
});

document.querySelectorAll("[data-query]").forEach((button) => {
  button.addEventListener("click", () => {
    queryInput.value = button.dataset.query;
    queryInput.focus();
  });
});

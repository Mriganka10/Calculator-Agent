# Calculator Agent

A small Python calculator agent with a FastAPI API and responsive web UI. It:

1. accepts a mathematical request in natural language,
2. identifies the calculation type,
3. selects the calculator tool,
4. executes the calculation safely, and
5. returns the result with a short explanation.

## Run locally

Python 3.10 or newer is recommended.

```bash
git clone https://github.com/Mriganka10/Calculator-Agent.git
cd Calculator-Agent
git checkout feature/prototype_development_v1

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) for the UI or
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API
documentation.

Try requests such as:

```text
calculate 20% of 8500
add 25 and 17
what is (12 + 8) * 3?
square root of 144
2 to the power of 8
```

## Terminal mode

The original terminal agent is still available:

```bash
python -m calculator_agent "calculate 20% of 8500"
```

Example output:

```text
Task: percentage calculation
Tool: calculator
Answer: 1700
```

## Test

```bash
python -m pytest
```

## Design

- `CalculatorAgent` interprets the request and chooses a tool.
- `CalculatorTool` evaluates only an allowlist of arithmetic operations.
- `FastAPI` exposes the agent at `POST /api/calculate`.
- The browser UI visualizes the agent's task, tool choice, expression, and
  answer.
- No API key or external language model is required for this prototype.

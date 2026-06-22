# Calculator Agent

A small, dependency-free Python agent that:

1. accepts a mathematical request in natural language,
2. identifies the calculation type,
3. selects the calculator tool,
4. executes the calculation safely, and
5. returns the result with a short explanation.

## Run

Python 3.10 or newer is recommended.

```bash
python -m calculator_agent
```

Then enter requests such as:

```text
calculate 20% of 8500
add 25 and 17
what is (12 + 8) * 3?
square root of 144
2 to the power of 8
```

You can also send one request directly:

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
python -m unittest discover -s tests -v
```

## Design

- `CalculatorAgent` interprets the request and chooses a tool.
- `CalculatorTool` evaluates only an allowlist of arithmetic operations.
- No API key, external model, or third-party package is required for this
  prototype.

"""HTTP API and web entrypoint for the calculator agent."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from calculator_agent import CalculatorAgent


STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title="Calculator Agent",
    description="Understand a mathematical request, choose a calculator tool, and return the answer.",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

agent = CalculatorAgent()


class CalculationRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=500,
        examples=["calculate 20% of 8500"],
    )


class CalculationResponse(BaseModel):
    task: str
    tool: str
    answer: int | float | None
    expression: str | None
    error: str | None


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/calculate", response_model=CalculationResponse)
def calculate(request: CalculationRequest) -> CalculationResponse:
    result = agent.run(request.query)
    return CalculationResponse(
        task=result.task,
        tool=result.tool,
        answer=result.answer,
        expression=result.expression,
        error=result.error,
    )

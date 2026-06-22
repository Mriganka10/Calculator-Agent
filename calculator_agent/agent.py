"""Natural-language planning layer for the calculator tool."""

from __future__ import annotations

from dataclasses import dataclass
import re

from .tool import CalculationError, CalculatorTool


@dataclass(frozen=True)
class AgentResponse:
    task: str
    tool: str
    answer: int | float | None
    expression: str | None = None
    error: str | None = None

    def format(self) -> str:
        if self.error:
            return f"Task: {self.task}\nTool: {self.tool}\nError: {self.error}"
        return f"Task: {self.task}\nTool: {self.tool}\nAnswer: {self.answer}"


class CalculatorAgent:
    """Understand common math requests and execute them with a calculator."""

    _number = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)"

    def __init__(self, calculator: CalculatorTool | None = None) -> None:
        self.calculator = calculator or CalculatorTool()

    def run(self, user_input: str) -> AgentResponse:
        if not user_input or not user_input.strip():
            return AgentResponse(
                task="unknown mathematical task",
                tool=self.calculator.name,
                answer=None,
                error="Please enter a mathematical question.",
            )

        try:
            task, expression = self._understand(user_input)
            answer = self.calculator.calculate(expression)
            return AgentResponse(
                task=task,
                tool=self.calculator.name,
                expression=expression,
                answer=answer,
            )
        except CalculationError as error:
            return AgentResponse(
                task="unsupported mathematical task",
                tool=self.calculator.name,
                answer=None,
                error=str(error),
            )

    def _understand(self, user_input: str) -> tuple[str, str]:
        text = user_input.lower().strip()
        text = text.replace(",", "")
        text = re.sub(r"[?=]+$", "", text).strip()

        percentage = re.fullmatch(
            rf"(?:calculate\s+|what\s+is\s+)?({self._number})\s*(?:%|percent)\s+of\s+({self._number})",
            text,
        )
        if percentage:
            percent, value = percentage.groups()
            return "percentage calculation", f"({percent} / 100) * {value}"

        patterns = (
            (
                rf"(?:add|sum(?:\s+of)?)\s+({self._number})\s+(?:and|to)\s+({self._number})",
                "addition",
                lambda a, b: f"{a} + {b}",
            ),
            (
                rf"(?:subtract)\s+({self._number})\s+from\s+({self._number})",
                "subtraction",
                lambda a, b: f"{b} - {a}",
            ),
            (
                rf"(?:multiply)\s+({self._number})\s+(?:by|and)\s+({self._number})",
                "multiplication",
                lambda a, b: f"{a} * {b}",
            ),
            (
                rf"(?:divide)\s+({self._number})\s+by\s+({self._number})",
                "division",
                lambda a, b: f"{a} / {b}",
            ),
            (
                rf"(?:what\s+is\s+)?({self._number})\s+to\s+the\s+power\s+of\s+({self._number})",
                "power calculation",
                lambda a, b: f"{a} ** {b}",
            ),
        )
        for pattern, task, expression_builder in patterns:
            match = re.fullmatch(pattern, text)
            if match:
                return task, expression_builder(*match.groups())

        square_root = re.fullmatch(
            rf"(?:calculate\s+|what\s+is\s+)?(?:the\s+)?square\s+root\s+of\s+({self._number})",
            text,
        )
        if square_root:
            return "square root calculation", f"sqrt({square_root.group(1)})"

        expression = re.sub(
            r"^(?:calculate|compute|evaluate|solve|what\s+is)\s+",
            "",
            text,
        ).strip()
        expression = expression.replace("^", "**")

        if re.fullmatch(r"[\d\s.+\-*/%()]+", expression):
            return "arithmetic calculation", expression

        raise CalculationError(
            "I could not identify a supported calculation. "
            "Try '20% of 8500' or '(12 + 8) * 3'."
        )

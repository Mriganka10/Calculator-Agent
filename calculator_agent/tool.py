"""Safe arithmetic tool used by the agent."""

from __future__ import annotations

import ast
import math
import operator


class CalculationError(ValueError):
    """Raised when a calculation cannot be evaluated safely."""


class CalculatorTool:
    """Evaluate a restricted arithmetic expression."""

    name = "calculator"

    _binary_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    _unary_operators = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }
    _functions = {
        "abs": abs,
        "sqrt": math.sqrt,
    }

    def calculate(self, expression: str) -> int | float:
        if not expression.strip():
            raise CalculationError("The calculation is empty.")

        try:
            tree = ast.parse(expression, mode="eval")
            result = self._evaluate(tree.body)
        except (SyntaxError, TypeError, ValueError, ZeroDivisionError, OverflowError) as error:
            raise CalculationError(f"Could not calculate '{expression}': {error}") from error

        if isinstance(result, complex) or not math.isfinite(float(result)):
            raise CalculationError("The result must be a finite real number.")

        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result

    def _evaluate(self, node: ast.AST) -> int | float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in self._binary_operators:
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            return self._binary_operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in self._unary_operators:
            return self._unary_operators[type(node.op)](self._evaluate(node.operand))

        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in self._functions
            and len(node.args) == 1
            and not node.keywords
        ):
            return self._functions[node.func.id](self._evaluate(node.args[0]))

        raise CalculationError("Only numbers and supported arithmetic operations are allowed.")

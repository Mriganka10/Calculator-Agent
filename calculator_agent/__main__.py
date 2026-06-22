"""Command-line interface for the calculator agent."""

from __future__ import annotations

import sys

from .agent import CalculatorAgent


def main() -> None:
    agent = CalculatorAgent()

    if len(sys.argv) > 1:
        print(agent.run(" ".join(sys.argv[1:])).format())
        return

    print("Calculator Agent (type 'quit' to exit)")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user_input.lower() in {"quit", "exit"}:
            break
        print(agent.run(user_input).format())


if __name__ == "__main__":
    main()

import unittest

from calculator_agent import CalculatorAgent


class CalculatorAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = CalculatorAgent()

    def test_percentage(self) -> None:
        response = self.agent.run("calculate 20% of 8500")
        self.assertEqual(response.task, "percentage calculation")
        self.assertEqual(response.tool, "calculator")
        self.assertEqual(response.answer, 1700)

    def test_arithmetic_expression(self) -> None:
        self.assertEqual(self.agent.run("what is (12 + 8) * 3?").answer, 60)

    def test_natural_language_operations(self) -> None:
        self.assertEqual(self.agent.run("add 25 and 17").answer, 42)
        self.assertEqual(self.agent.run("subtract 8 from 20").answer, 12)
        self.assertEqual(self.agent.run("multiply 7 by 6").answer, 42)
        self.assertEqual(self.agent.run("divide 84 by 7").answer, 12)

    def test_square_root_and_power(self) -> None:
        self.assertEqual(self.agent.run("square root of 144").answer, 12)
        self.assertEqual(self.agent.run("2 to the power of 8").answer, 256)

    def test_rejects_non_math_code(self) -> None:
        response = self.agent.run("__import__('os').getcwd()")
        self.assertIsNone(response.answer)
        self.assertIsNotNone(response.error)

    def test_division_by_zero_returns_error(self) -> None:
        response = self.agent.run("10 / 0")
        self.assertIsNone(response.answer)
        self.assertIn("division by zero", response.error)


if __name__ == "__main__":
    unittest.main()

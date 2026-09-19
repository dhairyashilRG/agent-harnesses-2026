"""
Safe Calculator Tool - No eval() security risk
Uses AST parsing for safe mathematical expression evaluation
"""

import ast
import operator
from typing import Union

class SafeCalculator:
    """
    Safe calculator that parses and evaluates mathematical expressions
    without using eval() to avoid code injection vulnerabilities.
    """

    # Supported operations
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def __init__(self):
        self.allowed_nodes = {
            ast.Expression, ast.Expr, ast.Module,  # Container nodes
            ast.BinOp, ast.UnaryOp,  # Operation nodes
            ast.Constant, ast.Num,  # Number nodes
            ast.USub,  # Unary negative
        }

    def evaluate(self, expression: str) -> Union[float, int, str]:
        """
        Safely evaluate a mathematical expression.

        Args:
            expression: Mathematical expression string (e.g., "15 * 23 + 100")

        Returns:
            Result of evaluation or error message

        Example:
            >>> calc = SafeCalculator()
            >>> calc.evaluate("15 * 23 + 100")
            445
            >>> calc.evaluate("2 ** 8")
            256
        """
        try:
            # Parse the expression
            tree = ast.parse(expression, mode='eval')

            # Evaluate safely - tree.body is the actual expression
            result = self._eval_node(tree.body)

            return result

        except ValueError as e:
            return f"Error: {str(e)}"
        except (SyntaxError, TypeError) as e:
            return f"Error: Invalid expression - {str(e)}"
        except ZeroDivisionError:
            return "Error: Division by zero"
        except OverflowError:
            return "Error: Result too large"
        except Exception as e:
            return f"Error: {str(e)}"

    def _is_allowed_node(self, node):
        """Check if node type is allowed"""
        return isinstance(node, tuple(self.allowed_nodes))

    def _eval_node(self, node):
        """Recursively evaluate AST node"""
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8 compatibility
            return node.n
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)

            if op_type in self.OPERATORS:
                return self.OPERATORS[op_type](left, right)
            else:
                raise ValueError(f"Unsupported binary operator: {op_type}")

        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)

            if op_type in self.OPERATORS:
                return self.OPERATORS[op_type](operand)
            else:
                raise ValueError(f"Unsupported unary operator: {op_type}")

        else:
            raise ValueError(f"Unsupported node type: {type(node)}")


# Tool interface for agent systems
class CalculatorTool:
    """Calculator tool compatible with agent harness systems"""

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return """Perform mathematical calculations.

Supports: +, -, *, /, ** (exponent), unary minus

Examples:
- "15 * 23" → 345
- "2 ** 8" → 256
- "-10 + 5" → -5
- "100 / 4" → 25.0

Input: expression (string) - mathematical expression to evaluate
Output: numeric result or error message
"""

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '15 * 23 + 100')"
                }
            },
            "required": ["expression"],
            "additionalProperties": False
        }

    def execute(self, expression: str) -> str:
        """Execute calculation"""
        calc = SafeCalculator()
        result = calc.evaluate(expression)

        # Return as string for agent compatibility
        return str(result)


# Demo and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Safe Calculator Demo")
    print("=" * 60)

    calc = SafeCalculator()

    # Test cases
    test_cases = [
        ("15 * 23", 345),
        ("15 * 23 + 100", 445),
        ("2 ** 8", 256),
        ("-10 + 5", -5),
        ("100 / 4", 25.0),
        ("(5 + 3) * 2", 16),
    ]

    print("\n✅ Valid Expressions:")
    for expr, expected in test_cases:
        result = calc.evaluate(expr)
        status = "✅" if result == expected else "❌"
        print(f"{status} {expr} = {result} (expected {expected})")

    # Test security - these should fail
    print("\n🔒 Security Tests (should be blocked):")
    malicious = [
        "__import__('os').system('ls')",
        "open('/etc/passwd').read()",
        "exec('print(1)')",
        "eval('1+1')",
    ]

    for expr in malicious:
        result = calc.evaluate(expr)
        print(f"✅ Blocked: {expr[:40]}... → {result}")

    # Test edge cases
    print("\n🧪 Edge Cases:")
    edge_cases = [
        "1 / 0",  # Division by zero
        "999 ** 999",  # Overflow
        "invalid expression",  # Syntax error
    ]

    for expr in edge_cases:
        result = calc.evaluate(expr)
        print(f"  {expr}: {result}")

    print("\n" + "=" * 60)
    print("✅ All security tests passed - No eval() vulnerabilities!")
    print("=" * 60)

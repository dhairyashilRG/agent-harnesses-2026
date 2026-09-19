"""
Episode 8: Future Directions Demo
Code-Based Harness (Emerging Trend)

This demonstrates the emerging trend of using code as the primary
harness substrate instead of natural language prompts.
"""

import os
import sys
from typing import Optional, List
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _llm import MODEL
from _llm import text as llm_text   # aliased: a local param named `text` shadows it

load_dotenv()

class CodeBasedHarness:
    """
    A code-based harness that generates and executes code
    to solve problems.

    This represents an emerging trend where code becomes the
    primary substrate for agent harnesses.
    """

    def __init__(self):
        self.code_library = {}
        self.execution_results = {}

    def solve_task(self, task_description: str,
                   test_cases: Optional[List[dict]] = None) -> dict:
        """
        Solve a task by generating and executing code.

        Process:
        1. Generate code solution
        2. Test against test cases
        3. Refine if needed
        4. Return final solution
        """
        print(f"\n🎯 Task: {task_description}\n")

        # Step 1: Generate solution code
        print("📝 Step 1: Generating solution code...")
        solution_code = self._generate_solution_code(task_description)

        print(f"\nGenerated code:\n{solution_code}\n")

        # Step 2: Test if test cases provided
        if test_cases:
            print("🧪 Step 2: Testing solution...")

            test_results = []
            for i, test_case in enumerate(test_cases):
                result = self._test_code(solution_code, test_case)
                test_results.append(result)
                status = "✅" if result["passed"] else "❌"
                print(f"  Test {i+1}: {status} {result.get('output', '')[:50]}")

            # Step 3: Refine if tests fail
            if not all(r["passed"] for r in test_results):
                print("\n🔧 Step 3: Refining solution...")
                solution_code = self._refine_solution(
                    solution_code,
                    test_cases,
                    test_results
                )

        # Store solution
        solution_id = f"solution_{len(self.code_library)}"
        self.code_library[solution_id] = solution_code

        return {
            "solution_id": solution_id,
            "code": solution_code,
            "test_results": test_results if test_cases else None
        }

    def _generate_solution_code(self, task: str) -> str:
        """Generate code to solve the task"""
        prompt = f"""Write a Python function to solve this task:
{task}

Requirements:
- Write clean, well-commented code
- Include type hints
- Handle edge cases
- Return the result

Only output the function code, no explanations."""

        reply = llm_text([{"role": "user", "content": prompt}], max_tokens=max(1024, 2500), temperature=0)

        return self._extract_code(reply)

    def _extract_code(self, text: str) -> str:
        """Extract code from text"""
        if "```python" in text:
            # Extract code block
            start = text.find("```python") + 9
            end = text.find("```", start)
            return text[start:end].strip()
        return text.strip()

    def _test_code(self, code: str, test_case: dict) -> dict:
        """Test code against a test case"""
        try:
            # Create execution environment
            exec_globals = {}
            exec(code, exec_globals)

            # Get the function (assume it's the first function)
            func_name = None
            for name in exec_globals:
                if callable(exec_globals[name]) and not name.startswith("_"):
                    func_name = name
                    break

            if not func_name:
                return {"passed": False, "error": "No function found"}

            # Execute test
            func = exec_globals[func_name]
            result = func(*test_case.get("args", []), **test_case.get("kwargs", {}))

            # Check result
            expected = test_case.get("expected")
            passed = result == expected

            return {
                "passed": passed,
                "output": str(result),
                "expected": str(expected)
            }

        except Exception as e:
            return {
                "passed": False,
                "error": str(e)
            }

    def _refine_solution(self, code: str, test_cases: list,
                         test_results: list) -> str:
        """Refine solution based on test failures"""
        # Collect failures
        failures = [
            (tc, tr)
            for tc, tr in zip(test_cases, test_results)
            if not tr["passed"]
        ]

        # Build refinement prompt
        failures_desc = "\n".join([
            f"- Test: {tc}\n  Got: {tr.get('output')}\n  Expected: {tc.get('expected')}\n  Error: {tr.get('error', 'N/A')}"
            for tc, tr in failures
        ])

        prompt = f"""Refine this code to fix failing tests:

Current code:
{code}

Failing tests:
{failures_desc}

Return the refined code only."""

        reply = llm_text([{"role": "user", "content": prompt}], max_tokens=max(1024, 2500), temperature=0)

        return self._extract_code(reply)

def demo_code_harness():
    """Demonstrate code-based harness"""
    print("=" * 60)
    print("DEMO: Code-Based Harness")
    print("(Emerging Trend: Code as Primary Substrate)")
    print("=" * 60)

    harness = CodeBasedHarness()

    # Example 1: Simple math task
    result = harness.solve_task(
        task_description="Create a function that calculates the factorial of a number",
        test_cases=[
            {"args": [5], "expected": 120},
            {"args": [0], "expected": 1},
            {"args": [3], "expected": 6}
        ]
    )

    print(f"\n✅ Solution generated: {result['solution_id']}")
    print(f"Code length: {len(result['code'])} characters")

    # Example 2: String manipulation
    result = harness.solve_task(
        task_description="Create a function that reverses a string and counts vowels",
        test_cases=[
            {"args": ["hello"], "expected": ("olleh", 2)},
            {"args": ["world"], "expected": ("dlrow", 1)}
        ]
    )

    print(f"\n✅ Solution generated: {result['solution_id']}")

    print("\n💡 Key insight: Code-based harnesses use executable code")
    print("   as the primary representation instead of natural language.")
    print("   This enables precise execution, testing, and refinement.")

if __name__ == "__main__":
    demo_code_harness()

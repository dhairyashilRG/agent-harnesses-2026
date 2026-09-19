"""
Episode 2: Core Loop Demo
Complete ReAct Agent Implementation
"""

import os
import sys
from dotenv import load_dotenv
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _llm import MODEL, chat

load_dotenv()

@dataclass
class ToolCall:
    """Represents a tool call in the ReAct loop"""
    name: str
    input: Dict[str, Any]
    id: Optional[str] = None      # tool_call id; the tool reply must echo it back
    result: Optional[str] = None

@dataclass
class StepResult:
    """Result of a single ReAct step"""
    step_number: int
    thought: str
    action: Optional[ToolCall]
    observation: Optional[str]
    tokens_used: int
    duration_ms: float

class ReActAgent:
    """
    Complete ReAct agent implementation showing the core loop:
    Think -> Act -> Observe -> Repeat
    """

    def __init__(self, tools: Optional[List] = None):
        self.tools = {tool.name: tool for tool in (tools or [])}
        self.trace: List[StepResult] = []

    def run(self, task: str, max_steps: int = 10) -> str:
        """
        Execute the ReAct loop to solve a task.

        The core algorithm:
        1. THINK: Get LLM reasoning about next action
        2. ACT: Execute the chosen tool/action
        3. OBSERVE: Capture the result
        4. Repeat until done or max_steps reached
        """
        print(f"\n🎯 Task: {task}\n")

        # Initialize conversation
        messages = [{"role": "user", "content": task}]

        for step in range(1, max_steps + 1):
            print(f"\n{'='*60}")
            print(f"Step {step}/{max_steps}")
            print(f"{'='*60}")

            start_time = time.time()

            # THINK: Get next action from LLM
            result = chat(
                messages,
                tools=[self._format_tool(tool) for tool in self.tools.values()],
                max_tokens=2500,
                temperature=0,
            )
            response = result["message"]

            duration_ms = (time.time() - start_time) * 1000
            tokens_used = (result["usage"].get("prompt_tokens", 0)
                           + result["usage"].get("completion_tokens", 0))

            # Extract the thinking/reasoning
            thought = self._extract_thought(response)
            print(f"💭 Thought: {thought}")

            # Check if done
            if self._is_final_answer(response):
                answer = self._extract_answer(response)
                print(f"\n✅ Final Answer: {answer}")

                self.trace.append(StepResult(
                    step_number=step,
                    thought=thought,
                    action=None,
                    observation=None,
                    tokens_used=tokens_used,
                    duration_ms=duration_ms
                ))

                return answer

            # ACT: Extract and execute tool call
            tool_call = self._extract_tool_call(response)

            if tool_call:
                print(f"🔧 Tool: {tool_call.name}")
                print(f"📝 Input: {tool_call.input}")

                # Execute tool
                tool_result = self._execute_tool(tool_call)
                tool_call.result = tool_result

                print(f"📊 Result: {self._format_result(tool_result)}")

                # OBSERVE: echo the assistant's turn back verbatim, then answer it with a
                # role="tool" message carrying the SAME tool_call_id. Every provider
                # requires that pairing — a plain "Tool result: ..." user string is
                # rejected on the next call.
                messages.append(response)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.name,
                    "content": str(tool_result),
                })

                self.trace.append(StepResult(
                    step_number=step,
                    thought=thought,
                    action=tool_call,
                    observation=tool_result,
                    tokens_used=tokens_used,
                    duration_ms=duration_ms
                ))

        return "Task incomplete - reached maximum steps"

    def _format_tool(self, tool) -> Dict:
        """Our Tool objects -> the provider's function schema."""
        return {"type": "function", "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.input_schema,
        }}

    def _extract_thought(self, response) -> str:
        """Whatever the model said alongside its tool call, if anything."""
        return (response.get("content") or "").strip()[:200] or "No explicit thought"

    def _is_final_answer(self, response) -> bool:
        """Done means: it asked for no tools and it said something."""
        return not response.get("tool_calls") and bool(response.get("content"))

    def _extract_answer(self, response) -> str:
        return (response.get("content") or "").strip()

    def _extract_tool_call(self, response) -> Optional[ToolCall]:
        """First tool call, if the model asked for one. Arguments arrive as a JSON string."""
        for call in (response.get("tool_calls") or []):
            return ToolCall(
                name=call["function"]["name"],
                input=json.loads(call["function"]["arguments"] or "{}"),
                id=call["id"],
            )
        return None

    def _execute_tool(self, tool_call: ToolCall) -> str:
        """Execute a tool call"""
        tool = self.tools.get(tool_call.name)
        if tool:
            try:
                result = tool.execute(**tool_call.input)
                return str(result)
            except Exception as e:
                return f"Error: {str(e)}"
        return f"Tool {tool_call.name} not found"

    def _format_result(self, result: str) -> str:
        """Format result for display"""
        if len(result) > 150:
            return result[:150] + "..."
        return result

    def get_trace(self) -> List[StepResult]:
        """Get the complete execution trace"""
        return self.trace

    def print_summary(self):
        """Print execution summary"""
        if not self.trace:
            print("No trace available")
            return

        total_tokens = sum(step.tokens_used for step in self.trace)
        total_duration = sum(step.duration_ms for step in self.trace)
        tool_calls = [step.action for step in self.trace if step.action]

        print(f"\n{'='*60}")
        print("Execution Summary")
        print(f"{'='*60}")
        print(f"Total Steps: {len(self.trace)}")
        print(f"Total Tokens: {total_tokens}")
        print(f"Total Duration: {total_duration:.0f}ms")
        print(f"Tool Calls: {len(tool_calls)}")

        if tool_calls:
            print("\nTools Used:")
            for call in tool_calls:
                print(f"  - {call.name}")

# Example Tools
class Tool:
    """Base tool class"""
    @property
    def name(self): pass
    @property
    def description(self): pass
    @property
    def input_schema(self): pass
    def execute(self, **kwargs): pass

class Calculator(Tool):
    """Basic calculator tool"""

    @property
    def name(self):
        return "calculator"

    @property
    def description(self):
        return "Perform mathematical calculations. Input should be an expression like '15 * 23'."

    @property
    def input_schema(self):
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }

    def execute(self, expression: str) -> str:
        """Safely evaluate mathematical expression"""
        try:
            # Only allow safe characters
            allowed = set("0123456789+-*/.() ")
            if not all(c in allowed for c in expression):
                return "Error: Invalid characters in expression"

            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"

def demo_react_agent():
    """Demonstrate the ReAct agent"""
    print("=" * 60)
    print("DEMO: Complete ReAct Agent")
    print("=" * 60)

    # Create agent with tools
    agent = ReActAgent(tools=[Calculator()])

    # Run a complex task
    result = agent.run(
        task="Calculate 15 times 23, then add 100 to that result.",
        max_steps=5
    )

    # Print summary
    agent.print_summary()

if __name__ == "__main__":
    demo_react_agent()

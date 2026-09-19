"""
Episode 2: Core Loop Demo
Trace Visualization Tool
"""

from typing import List
from dataclasses import dataclass
import json

@dataclass
class TraceStep:
    """A single step in an agent trace"""
    step_number: int
    thought: str
    action: str
    observation: str
    tokens: int
    duration_ms: float

class TraceVisualizer:
    """
    Visualizes agent execution traces for debugging and understanding.
    This is essential for production systems.
    """

    def __init__(self):
        self.steps: List[TraceStep] = []

    def add_step(self, step: TraceStep):
        """Add a step to the trace"""
        self.steps.append(step)

    def visualize(self) -> str:
        """Generate a human-readable trace visualization"""
        if not self.steps:
            return "No trace data available"

        output = []
        output.append("\n" + "=" * 70)
        output.append("AGENT EXECUTION TRACE")
        output.append("=" * 70)

        for step in self.steps:
            output.append(f"\n{'─' * 70}")
            output.append(f"STEP {step.step_number}")
            output.append(f"{'─' * 70}")

            # Thought (in blue conceptually)
            output.append(f"\n💭 THOUGHT:")
            output.append(f"   {step.thought}")

            # Action (in green conceptually)
            output.append(f"\n🔧 ACTION:")
            output.append(f"   {step.action}")

            # Observation (in orange conceptually)
            output.append(f"\n📊 OBSERVATION:")
            output.append(f"   {self._format_observation(step.observation)}")

            # Metrics
            output.append(f"\n📈 METRICS:")
            output.append(f"   Tokens: {step.tokens} | Duration: {step.duration_ms:.0f}ms")

        output.append(f"\n{'=' * 70}")
        output.append("TRACE SUMMARY")
        output.append(f"{'=' * 70}")

        total_tokens = sum(s.tokens for s in self.steps)
        total_duration = sum(s.duration_ms for s in self.steps)
        action_steps = sum(1 for s in self.steps if s.action != "No action")

        output.append(f"Total Steps: {len(self.steps)}")
        output.append(f"Total Tokens: {total_tokens}")
        output.append(f"Total Duration: {total_duration:.0f}ms ({total_duration/1000:.1f}s)")
        output.append(f"Action Steps: {action_steps}")
        output.append(f"Avg Tokens/Step: {total_tokens // len(self.steps)}")
        output.append(f"Avg Duration/Step: {total_duration/len(self.steps):.0f}ms")

        return "\n".join(output)

    def _format_observation(self, observation: str) -> str:
        """Format observation for display"""
        if len(observation) > 100:
            return observation[:100] + "..."
        return observation

    def to_json(self) -> str:
        """Export trace as JSON for analysis"""
        data = [
            {
                "step": s.step_number,
                "thought": s.thought,
                "action": s.action,
                "observation": s.observation,
                "tokens": s.tokens,
                "duration_ms": s.duration_ms
            }
            for s in self.steps
        ]
        return json.dumps(data, indent=2)

    def save_trace(self, filepath: str):
        """Save trace to file"""
        with open(filepath, 'w') as f:
            f.write(self.visualize())
            f.write("\n\n" + "=" * 70)
            f.write("JSON EXPORT")
            f.write("=" * 70 + "\n")
            f.write(self.to_json())

def demo_trace_visualizer():
    """Demonstrate trace visualization"""
    print("=" * 70)
    print("DEMO: Trace Visualization")
    print("=" * 70)

    viz = TraceVisualizer()

    # Simulate an agent execution
    viz.add_step(TraceStep(
        step_number=1,
        thought="I need to calculate 15 * 23 first",
        action="Use calculator with '15 * 23'",
        observation="345",
        tokens=150,
        duration_ms=850
    ))

    viz.add_step(TraceStep(
        step_number=2,
        thought="Now I need to add 100 to the result (345)",
        action="Use calculator with '345 + 100'",
        observation="445",
        tokens=180,
        duration_ms=920
    ))

    viz.add_step(TraceStep(
        step_number=3,
        thought="I have the final answer: 445",
        action="No action - providing final answer",
        observation="Task complete",
        tokens=120,
        duration_ms=650
    ))

    # Display trace
    print(viz.visualize())

    # Save trace
    viz.save_trace("demo_trace.txt")
    print("\n💾 Trace saved to demo_trace.txt")

if __name__ == "__main__":
    demo_trace_visualizer()

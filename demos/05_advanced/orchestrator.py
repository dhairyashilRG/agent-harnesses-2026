"""
Episode 5: Advanced Patterns Demo
Multi-Agent Orchestrator-Worker System
"""

import os
import sys
from typing import List, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _llm import MODEL, chat, text

load_dotenv()

@dataclass
class Subtask:
    """A subtask to be delegated to a worker agent"""
    id: str
    description: str
    worker_type: str
    dependencies: List[str]

@dataclass
class SubtaskResult:
    """Result from a worker agent"""
    subtask_id: str
    result: str
    success: bool

class WorkerAgent:
    """Specialized worker agent that executes specific types of tasks"""

    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty

    def execute(self, subtask: Subtask) -> SubtaskResult:
        """Execute a subtask"""
        print(f"🔧 {self.name} working on: {subtask.description}")

        # Simulate work with LLM
        reply = text([{
                "role": "user",
                "content": f"As a {self.specialty} specialist, complete this task: {subtask.description}"
            }], max_tokens=2000)

        return SubtaskResult(
            subtask_id=subtask.id,
            result=reply,
            success=True
        )

class OrchestratorAgent:
    """
    Orchestrator agent that coordinates worker agents.
    Demonstrates the orchestrator-worker pattern for multi-agent systems.
    """

    def __init__(self):
        self.workers = {
            "coder": WorkerAgent("CodeBot", "programming"),
            "researcher": WorkerAgent("ResearchBot", "research"),
            "writer": WorkerAgent("WriteBot", "writing")
        }

    def solve_task(self, task: str) -> str:
        """
        Solve a complex task by:
        1. Decomposing into subtasks
        2. Assigning to appropriate workers
        3. Synthesizing results
        """
        print(f"\n🎯 Orchestrator received task: {task}\n")

        # Step 1: Decompose task
        print("📋 Step 1: Decomposing task...")
        subtasks = self._decompose_task(task)

        # Step 2: Execute subtasks (simplified - would handle dependencies)
        print("\n👥 Step 2: Assigning to workers...")
        results = {}
        for subtask in subtasks:
            worker = self.workers[subtask.worker_type]
            result = worker.execute(subtask)
            results[subtask.id] = result

        # Step 3: Synthesize results
        print("\n🔗 Step 3: Synthesizing results...")
        final_answer = self._synthesize(task, results)

        return final_answer

    def _decompose_task(self, task: str) -> List[Subtask]:
        """Break task into subtasks"""
        # In production, this would use the LLM to analyze and decompose
        # For demo, return predefined subtasks

        if "blog post" in task.lower():
            return [
                Subtask("1", "Research the main topic", "researcher", []),
                Subtask("2", "Outline the blog structure", "writer", ["1"]),
                Subtask("3", "Write the content", "writer", ["2"]),
                Subtask("4", "Add code examples", "coder", ["2"])
            ]
        else:
            return [
                Subtask("1", f"Analyze requirements for: {task}", "researcher", []),
                Subtask("2", "Propose solution approach", "coder", ["1"])
            ]

    def _synthesize(self, task: str, results: Dict[str, SubtaskResult]) -> str:
        """Synthesize worker results into final answer"""
        synthesis_input = f"Original task: {task}\n\nWorker results:\n"

        for subtask_id, result in results.items():
            synthesis_input += f"\nSubtask {subtask_id}: {result.result}\n"

        reply = text([{
                "role": "user",
                "content": f"Synthesize these worker results into a coherent final answer:\n{synthesis_input}"
            }], max_tokens=2500)

        return reply

def demo_orchestrator():
    """Demonstrate multi-agent orchestrator"""
    print("=" * 60)
    print("DEMO: Multi-Agent Orchestrator-Worker System")
    print("=" * 60)

    orchestrator = OrchestratorAgent()

    result = orchestrator.solve_task(
        task="Create a blog post about quantum computing with code examples"
    )

    print(f"\n✅ Final Result:\n{result}")

if __name__ == "__main__":
    demo_orchestrator()

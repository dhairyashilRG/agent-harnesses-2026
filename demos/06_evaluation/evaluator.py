"""
Episode 6: Evaluation Demo
Agent Evaluation Framework
"""

import time
from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum

class TaskType(Enum):
    CODING = "coding"
    MATH = "math"
    WRITING = "writing"
    REASONING = "reasoning"

@dataclass
class Task:
    """A task for evaluation"""
    id: str
    description: str
    task_type: TaskType
    expected_output: str
    verify_fn: Callable[[str], bool]

@dataclass
class TaskResult:
    """Result of running a task"""
    task_id: str
    success: bool
    correct: bool
    duration_seconds: float
    tokens_used: int
    cost_usd: float
    answer: str

@dataclass
class EvaluationReport:
    """Complete evaluation report"""
    total_tasks: int
    success_rate: float
    correctness_rate: float
    avg_duration: float
    avg_cost: float
    results_by_type: Dict[str, Dict]
    detailed_results: List[TaskResult]

class AgentEvaluator:
    """
    Comprehensive agent evaluation system.

    Measures:
    - Success rate (did it complete?)
    - Correctness (was the answer right?)
    - Efficiency (time and cost)
    - Generalization (performance across types)
    """

    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a task to the evaluation suite"""
        self.tasks.append(task)

    def evaluate(self, agent: Any, agent_name: str = "Agent") -> EvaluationReport:
        """
        Evaluate an agent on the task suite.

        This runs the agent on each task and collects metrics.
        """
        print(f"\n{'='*60}")
        print(f"Evaluating {agent_name}")
        print(f"{'='*60}\n")

        results = []

        for task in self.tasks:
            print(f"Task {task.id}: {task.description[:50]}...")

            start_time = time.time()

            try:
                # Run the agent (simplified - would use actual agent.run())
                answer = self._run_agent(agent, task)

                duration = time.time() - start_time

                # Check correctness
                correct = task.verify_fn(answer)

                result = TaskResult(
                    task_id=task.id,
                    success=True,
                    correct=correct,
                    duration_seconds=duration,
                    tokens_used=self._estimate_tokens(answer),
                    cost_usd=self._calculate_cost(duration),
                    answer=answer[:100]  # Truncated for storage
                )

                status = "✅" if correct else "❌"
                print(f"  {status} Correct: {correct} | Time: {duration:.1f}s")

            except Exception as e:
                duration = time.time() - start_time

                result = TaskResult(
                    task_id=task.id,
                    success=False,
                    correct=False,
                    duration_seconds=duration,
                    tokens_used=0,
                    cost_usd=self._calculate_cost(duration),
                    answer=str(e)
                )

                print(f"  💥 Failed: {str(e)[:50]}")

            results.append(result)

        # Generate report
        return self._generate_report(results, agent_name)

    def _run_agent(self, agent: Any, task: Task) -> str:
        """Run agent on task (simplified)"""
        # In production, this would call agent.run(task.description)
        # For demo, return a mock response
        return f"Mock answer for {task.id}"

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)"""
        return len(text.split()) * 1.3  # Rough estimate

    def _calculate_cost(self, duration: float) -> float:
        """Calculate cost based on duration (simplified)"""
        # Assume $0.001 per second
        return duration * 0.001

    def _generate_report(self, results: List[TaskResult], agent_name: str) -> EvaluationReport:
        """Generate evaluation report"""

        if not results:
            return EvaluationReport(0, 0, 0, 0, 0, {}, [])

        # Calculate aggregate metrics
        success_count = sum(1 for r in results if r.success)
        correct_count = sum(1 for r in results if r.correct)
        total_duration = sum(r.duration_seconds for r in results)
        total_cost = sum(r.cost_usd for r in results)

        # Results by task type
        results_by_type = {}
        for result in results:
            task = next(t for t in self.tasks if t.id == result.task_id)
            task_type = task.task_type.value

            if task_type not in results_by_type:
                results_by_type[task_type] = {
                    "total": 0,
                    "correct": 0,
                    "success": 0
                }

            results_by_type[task_type]["total"] += 1
            if result.correct:
                results_by_type[task_type]["correct"] += 1
            if result.success:
                results_by_type[task_type]["success"] += 1

        return EvaluationReport(
            total_tasks=len(results),
            success_rate=success_count / len(results),
            correctness_rate=correct_count / len(results),
            avg_duration=total_duration / len(results),
            avg_cost=total_cost / len(results),
            results_by_type=results_by_type,
            detailed_results=results
        )

    def print_report(self, report: EvaluationReport):
        """Print evaluation report"""
        print(f"\n{'='*60}")
        print("EVALUATION REPORT")
        print(f"{'='*60}\n")

        print(f"Total Tasks: {report.total_tasks}")
        print(f"Success Rate: {report.success_rate:.1%}")
        print(f"Correctness Rate: {report.correctness_rate:.1%}")
        print(f"Average Duration: {report.avg_duration:.1f}s")
        print(f"Average Cost: ${report.avg_cost:.4f}")

        print(f"\nResults by Task Type:")
        for task_type, stats in report.results_by_type.items():
            print(f"\n  {task_type}:")
            print(f"    Total: {stats['total']}")
            print(f"    Correct: {stats['correct']}/{stats['total']} ({stats['correct']/stats['total']:.1%})")
            print(f"    Success: {stats['success']}/{stats['total']} ({stats['success']/stats['total']:.1%})")

def demo_evaluator():
    """Demonstrate agent evaluation"""
    print("=" * 60)
    print("DEMO: Agent Evaluation Framework")
    print("=" * 60)

    evaluator = AgentEvaluator()

    # Add sample tasks
    evaluator.add_task(Task(
        id="math1",
        description="Calculate 15 * 23",
        task_type=TaskType.MATH,
        expected_output="345",
        verify_fn=lambda x: "345" in x
    ))

    evaluator.add_task(Task(
        id="code1",
        description="Write a function to reverse a string",
        task_type=TaskType.CODING,
        expected_output="def reverse",
        verify_fn=lambda x: "def" in x and "reverse" in x
    ))

    evaluator.add_task(Task(
        id="reason1",
        description="If all bloops are bleeps and some bleeps are blops, are all bloops blops?",
        task_type=TaskType.REASONING,
        expected_output="Cannot be determined",
        verify_fn=lambda x: "cannot" in x.lower() or "not necessarily" in x.lower()
    ))

    # Evaluate a mock agent
    class MockAgent:
        pass

    agent = MockAgent()
    report = evaluator.evaluate(agent, "MockAgent")

    # Print report
    evaluator.print_report(report)

if __name__ == "__main__":
    demo_evaluator()

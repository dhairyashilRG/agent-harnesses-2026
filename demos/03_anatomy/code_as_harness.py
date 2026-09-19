"""
Code as Agent Harness - Educational Implementation
Major 2026 theme: Code serving as executable substrate for reasoning

This demonstrates how code itself becomes the harness:
- Code maintains state across reasoning steps
- Code implements verification and self-checking
- Code provides the world model and knowledge representation
- Code IS the harness, not just a tool the harness uses

Key insight: In 2026, we increasingly treat code as the primary
harness substrate, with LLMs as reasoning engines that write and
execute code to solve problems.
"""

import time
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ExecutionPhase(Enum):
    """Phases of code-based harness execution"""
    INITIALIZATION = "initialization"
    REASONING = "reasoning"
    VERIFICATION = "verification"
    WORLD_MODEL_UPDATE = "world_model_update"
    ACTION = "action"
    REFLECTION = "reflection"


@dataclass
class WorldState:
    """The world model maintained by code"""
    facts: Dict[str, Any] = field(default_factory=dict)
    relationships: List[tuple] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)

    def add_fact(self, key: str, value: Any, confidence: float = 1.0):
        """Add a fact to the world model"""
        self.facts[key] = value
        self.confidence_scores[key] = confidence

    def add_relationship(self, entity1: str, relation: str, entity2: str):
        """Add a relationship between entities"""
        self.relationships.append((entity1, relation, entity2))

    def query(self, query: str) -> Any:
        """Query the world model"""
        # Simple query implementation
        if query in self.facts:
            return self.facts[query]
        return None


@dataclass
class CodeHarnessStep:
    """A single step in code-based harness execution"""
    phase: ExecutionPhase
    code_executed: str
    result: Any
    world_state_before: Dict
    world_state_after: Dict
    timestamp: str
    success: bool


class CodeAsHarness:
    """
    Code as Harness implementation

    The code IS the harness - it maintains state, implements reasoning,
    provides verification, and represents the world model.
    """

    def __init__(self, name: str = "CodeHarness"):
        self.name = name
        self.world_state = WorldState()
        self.execution_history: List[CodeHarnessStep] = []
        self.code_blocks: Dict[str, Callable] = {}
        self.verification_rules: List[Callable] = []

        # Initialize with basic capabilities
        self._initialize_base_capabilities()

    def _initialize_base_capabilities(self):
        """Initialize basic harness capabilities as code"""

        # Reasoning capability
        def reason_about(task: str, context: Dict) -> Dict:
            """Reason about a task using world state"""
            return {
                "task": task,
                "relevant_facts": [k for k in context.world_state.facts.keys()],
                "confidence": 0.7
            }

        # Verification capability
        def verify_result(result: Any, expected_criteria: Dict) -> Dict:
            """Verify a result meets criteria"""
            return {
                "verified": True,
                "confidence": 0.8,
                "issues": []
            }

        # World model update capability
        def update_world_model(new_info: Dict, world_state: WorldState):
            """Update world model with new information"""
            for key, value in new_info.items():
                world_state.add_fact(key, value, confidence=0.9)
            return world_state

        # Register code blocks
        self.code_blocks["reason"] = reason_about
        self.code_blocks["verify"] = verify_result
        self.code_blocks["update_world"] = update_world_model

    def execute_task(self, task: str, max_steps: int = 5) -> Dict[str, Any]:
        """
        Execute a task using code as the harness

        The LLM (not shown here) would write code that:
        1. Reasons about the task
        2. Updates the world model
        3. Takes actions
        4. Verifies results
        5. Reflects and iterates

        This code IS the harness.
        """
        print(f"\n{'='*70}")
        print(f"📝 CODE AS HARNESS: Executing Task")
        print(f"{'='*70}")
        print(f"Task: {task}")
        print()

        steps_executed = 0
        result = None

        for step in range(max_steps):
            steps_executed += 1
            print(f"\n{'─'*70}")
            print(f"📍 STEP {step + 1}/{max_steps}")
            print(f"{'─'*70}")

            # Phase 1: Reasoning (code-based)
            print("💭 Phase: REASONING")
            reasoning_result = self.code_blocks["reason"](
                task,
                type('Context', (), {'world_state': self.world_state})()
            )
            print(f"   Reasoned about task: {reasoning_result['task']}")
            print(f"   Relevant facts: {reasoning_result['relevant_facts']}")

            # Phase 2: World Model Update (code-based)
            print("🌍 Phase: WORLD MODEL UPDATE")
            self.world_state.add_relationship("task", "requires", task.split()[0])
            print(f"   Updated world model with task info")

            # Phase 3: Action (code-based)
            print("⚡ Phase: ACTION")
            if "calculate" in task.lower():
                result = self._code_action_calculate(task)
            elif "analyze" in task.lower():
                result = self._code_action_analyze(task)
            else:
                result = f"Result for: {task}"
            print(f"   Action result: {result[:50]}...")

            # Phase 4: Verification (code-based)
            print("✓ Phase: VERIFICATION")
            verification = self.code_blocks["verify"](result, {"criteria": "basic"})
            print(f"   Verified: {verification['verified']} (confidence: {verification['confidence']})")

            # Phase 5: Reflection (code-based)
            print("🔄 Phase: REFLECTION")
            if verification['verified'] and verification['confidence'] > 0.7:
                print("   ✓ Satisfied with result, completing")
                break
            else:
                print("   ○ Need to iterate, updating world model")

            # Record step
            self.execution_history.append(CodeHarnessStep(
                phase=ExecutionPhase.REASONING,
                code_executed=f"reason_about('{task}')",
                result=result,
                world_state_before={},
                world_state_after={k: v for k, v in self.world_state.facts.items()},
                timestamp=datetime.now().isoformat(),
                success=verification['verified']
            ))

        return {
            "result": result,
            "steps": steps_executed,
            "world_state": {k: v for k, v in self.world_state.facts.items()},
            "success": verification['verified']
        }

    def _code_action_calculate(self, task: str) -> str:
        """Code-based calculation action"""
        # In real implementation, LLM would write this code
        numbers = [int(n) for n in task.split() if n.isdigit()]
        if numbers:
            return f"Calculation result: sum = {sum(numbers)}"
        return "No numbers found in task"

    def _code_action_analyze(self, task: str) -> str:
        """Code-based analysis action"""
        # In real implementation, LLM would write this code
        words = task.split()
        return f"Analysis result: {len(words)} words, {len(set(words))} unique"


def demo_code_as_harness():
    """Demonstrate code-as-harness concept"""
    print("\n" + "="*70)
    print("💻 CODE AS HARNESS DEMO")
    print("="*70)
    print()
    print("2026 Major Theme: Code as the Primary Harness Substrate")
    print()
    print("Traditional view:")
    print("  • LLM is the brain")
    print("  • Harness is external scaffolding")
    print("  • Tools are separate from reasoning")
    print()
    print("2026 view (Code as Harness):")
    print("  • Code IS the harness")
    print("  • State maintenance happens in code")
    print("  • Verification is code-based")
    print("  • World model is code structures")
    print("  • LLM writes code to solve problems")
    print()
    print("Key benefits:")
    print("  • Maximum expressiveness")
    print("  • Precise state management")
    print("  • Composability and reusability")
    print("  • Debuggable and inspectable")
    print("  • Can be improved automatically")
    print()

    harness = CodeAsHarness()

    # Run demo tasks
    tasks = [
        "Calculate the sum of 15, 23, and 100",
        "Analyze this text for patterns",
    ]

    for task in tasks:
        result = harness.execute_task(task, max_steps=3)
        print(f"\n✓ Task completed: {result['result']}")
        print(f"  Steps: {result['steps']}, Success: {result['success']}")


def demo_executable_world_model():
    """Demonstrate executable world model concept"""
    print("\n" + "="*70)
    print("🌍 EXECUTABLE WORLD MODEL")
    print("="*70)
    print()
    print("The world model is CODE that can be EXECUTED to:")
    print("  • Query state and relationships")
    print("  • Simulate actions and consequences")
    print("  • Verify consistency")
    print("  • Make predictions")
    print()
    print("Example: Physics world model (simplified)")
    print()

    world_model_code = '''
class PhysicsWorld:
    """Executable world model for physics reasoning"""

    def __init__(self):
        self.objects = {}
        self.laws = {
            "gravity": 9.8,
            "friction": 0.1
        }

    def add_object(self, name, mass, position):
        """Add an object to the world"""
        self.objects[name] = {
            "mass": mass,
            "position": position,
            "velocity": 0
        }

    def simulate(self, action):
        """Execute action and update world state"""
        # Physics simulation code here
        return f"Simulated: {action}"

    def query(self, question):
        """Query the world model"""
        if "position" in question.lower():
            for obj, data in self.objects.items():
                return f"{obj} at {data['position']}"
'''

    print(world_model_code)

    print("This code IS the world model - it's executable and queryable!")
    print()
    print("The LLM can:")
    print("  1. Write such world model code")
    print("  2. Execute it to simulate scenarios")
    print("  3. Query it to answer questions")
    print("  4. Update it based on new observations")
    print()


def demo_harness_learns_code():
    """Demonstrate how harness learns code patterns"""
    print("\n" + "="*70)
    print("🧠 HARNESS LEARNS CODE PATTERNS")
    print("="*70)
    print()
    print("Self-improving harnesses don't just learn prompts -")
    print("they learn CODE patterns that work!")
    print()
    print("Example learning process:")
    print()
    print("1. Execute many tasks with different code approaches")
    print("2. Mine traces for successful code patterns")
    print("3. Extract reusable code snippets")
    print("4. Add to skill library as executable code")
    print()
    print("This means:")
    print("  ✓ Skills are CODE, not text prompts")
    print("  ✓ Can be composed and reused")
    print("  ✓ Can be debugged and optimized")
    print("  ✓ Can be automatically improved")
    print()


if __name__ == "__main__":
    demo_code_as_harness()
    demo_executable_world_model()
    demo_harness_learns_code()

    print("\n" + "="*70)
    print("WHERE THIS IS A THESIS, NOT A CITATION")
    print("="*70)
    print()
    print("The argument for code as the harness substrate:")
    print("  1. Code is more expressive than JSON actions")
    print("  2. Code maintains precise state")
    print("  3. Code implements verification logic")
    print("  4. Code can represent the world model")
    print()
    print("This thesis has real, citable support:")
    print()
    print("  Executable World Models for ARC-AGI-3 in the Era of Coding Agents")
    print("  Sergey Rodionov, arxiv.org/abs/2605.05138 (v1 2026-05-06)")
    print("  github.com/astroseger/arc-3-agents-baseline1")
    print()
    print("  The agent 'maintains an executable Python world model, verifies it")
    print("  against previous observations, refactors it toward simpler")
    print("  abstractions ... and plans through the model before acting.'")
    print("  No hand-coded game-specific logic. One playthrough per game.")
    print("  Result: 58.12% mean RHAE with GPT-5.5 high, 15/25 public games")
    print("  solved (41.29%, 8/25 with GPT-5.4). The world model IS the code.")
    print()
    print("Also verified (tufalabs.ai/research/duck-harness/, 2026-07-17):")
    print("  - Tufa Labs' Duck won ARC-AGI-3 Milestone 1")
    print("    (arcprize.org/blog/arc-prize-2026-milestone-1)")
    print("  - It is the only winner using the agent-writes-code approach")
    print("  - Minimal harness, Python REPL, Qwen 3.6 27B FP8, image perception")
    print("  - An order of magnitude cheaper per game than the EWM agent on GPT-5.4")
    print()
    print("Where to stay honest:")
    print("  - NOBODY RAN THE EXPERIMENT. No source compares code-as-action against")
    print("    JSON-as-action with everything else held fixed. Code-as-harness is a")
    print("    well-supported thesis, not a measured finding.")
    print("  - Duck's 58.12%-vs-1.21% neighbours are on DIFFERENT SETS. EWM's number")
    print("    is the hill-climbable public set; Duck's 1.21% is the leaderboard.")
    print("    EWM's own paper: performance on the private set 'remains to be tested'.")
    print("  - Milestone 1 published no judging criteria. Do not claim Duck won")
    print("    BECAUSE of the code approach.")
    print("  - Tufa's own framing cuts the other way and deserves airtime:")
    print("    'solvability of a game being dependent on model capability, while")
    print("     the cost is mostly dictated by the harness.'")
    print()

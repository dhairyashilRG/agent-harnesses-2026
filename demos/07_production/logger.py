"""
Episode 7: Production Realities Demo
Production-Grade Logging System
"""

import time
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

@dataclass
class AgentEvent:
    """A single agent event for logging"""
    timestamp: float
    level: LogLevel
    agent_id: str
    session_id: str
    event_type: str
    data: Dict[str, Any]

@dataclass
class PerformanceMetrics:
    """Performance metrics for an action"""
    duration_ms: float
    tokens_used: int
    cost_usd: float
    llm_latency_ms: float

class ProductionLogger:
    """
    Production-grade logging for agent systems.

    Provides:
    - Structured logging with all relevant context
    - Performance tracking
    - Error tracking
    - Export for analysis
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.session_id = f"session_{int(time.time())}"
        self.events: list = []
        self.metrics: Dict[str, list] = {
            "durations": [],
            "tokens": [],
            "costs": []
        }

    def log_action(self,
                   action_type: str,
                   tool_name: Optional[str] = None,
                   inputs: Optional[Dict] = None,
                   outputs: Optional[Dict] = None,
                   performance: Optional[PerformanceMetrics] = None,
                   error: Optional[str] = None):
        """
        Log an agent action with full context.

        This captures everything needed for debugging and analysis.
        """
        level = LogLevel.ERROR if error else LogLevel.INFO

        event = AgentEvent(
            timestamp=time.time(),
            level=level,
            agent_id=self.agent_id,
            session_id=self.session_id,
            event_type=action_type,
            data={
                "tool": tool_name,
                "inputs": self._sanitize(inputs) if inputs else None,
                "outputs": self._sanitize(outputs) if outputs else None,
                "performance": asdict(performance) if performance else None,
                "error": error
            }
        )

        self.events.append(event)

        # Track metrics
        if performance:
            self.metrics["durations"].append(performance.duration_ms)
            self.metrics["tokens"].append(performance.tokens_used)
            self.metrics["costs"].append(performance.cost_usd)

        # Print for demo
        self._print_event(event)

    def _sanitize(self, data: Dict) -> Dict:
        """Sanitize sensitive data from logs"""
        sanitized = data.copy()
        sensitive_keys = ["api_key", "password", "token", "secret", "key"]

        for key in list(sanitized.keys()):
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                sanitized[key] = "***REDACTED***"

        return sanitized

    def _print_event(self, event: AgentEvent):
        """Print event for demo purposes"""
        timestamp = datetime.fromtimestamp(event.timestamp).strftime("%H:%M:%S")

        level_icon = {
            LogLevel.DEBUG: "🔍",
            LogLevel.INFO: "ℹ️",
            LogLevel.WARNING: "⚠️",
            LogLevel.ERROR: "❌"
        }[event.level]

        print(f"{level_icon} [{timestamp}] {event.event_type}")

        if event.data.get("tool"):
            print(f"   Tool: {event.data['tool']}")

        if event.data.get("performance"):
            perf = event.data["performance"]
            print(f"   Duration: {perf['duration_ms']:.0f}ms | "
                  f"Tokens: {perf['tokens_used']} | "
                  f"Cost: ${perf['cost_usd']:.4f}")

        if event.data.get("error"):
            print(f"   Error: {event.data['error']}")

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of logged events"""
        return {
            "session_id": self.session_id,
            "total_events": len(self.events),
            "errors": sum(1 for e in self.events if e.level == LogLevel.ERROR),
            "avg_duration_ms": sum(self.metrics["durations"]) / len(self.metrics["durations"]) if self.metrics["durations"] else 0,
            "total_tokens": sum(self.metrics["tokens"]),
            "total_cost_usd": sum(self.metrics["costs"])
        }

    def export_logs(self, filepath: str):
        """Export logs to JSON file"""
        export_data = {
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "summary": self.get_summary(),
            "events": [
                {
                    "timestamp": e.timestamp,
                    "level": e.level.value,
                    "event_type": e.event_type,
                    "data": e.data
                }
                for e in self.events
            ]
        }

        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"\n💾 Logs exported to {filepath}")

def demo_production_logger():
    """Demonstrate production logging"""
    print("=" * 60)
    print("DEMO: Production-Grade Logging")
    print("=" * 60)

    logger = ProductionLogger("demo_agent")

    # Simulate various agent actions

    # Successful tool use
    logger.log_action(
        action_type="tool_use",
        tool_name="calculator",
        inputs={"expression": "15 * 23"},
        outputs={"result": 345},
        performance=PerformanceMetrics(
            duration_ms=850,
            tokens_used=150,
            cost_usd=0.0015,
            llm_latency_ms=650
        )
    )

    # Another successful action
    logger.log_action(
        action_type="tool_use",
        tool_name="file_write",
        inputs={"path": "result.txt", "content": "345"},
        outputs={"status": "success"},
        performance=PerformanceMetrics(
            duration_ms=1200,
            tokens_used=200,
            cost_usd=0.0020,
            llm_latency_ms=950
        )
    )

    # Error case
    logger.log_action(
        action_type="tool_use",
        tool_name="api_call",
        inputs={"endpoint": "/data"},
        error="Rate limit exceeded",
        performance=PerformanceMetrics(
            duration_ms=500,
            tokens_used=50,
            cost_usd=0.0005,
            llm_latency_ms=500
        )
    )

    # Print summary
    print(f"\n{'='*60}")
    print("SESSION SUMMARY")
    print(f"{'='*60}")

    summary = logger.get_summary()
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")

    # Export logs
    logger.export_logs("demo_agent_logs.json")

if __name__ == "__main__":
    demo_production_logger()

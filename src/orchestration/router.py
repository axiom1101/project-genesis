from src.orchestration.state_machine import StateMachine
from src.agents.analyst import AnalystAgent
from src.evaluation.critic import CriticAgent


class TaskRouter:
    """
    Deterministic Orchestrator (Layer 5).
    Controls the flow, limits, and order of agent execution.
    """

    def __init__(self):
        self.state_machine = StateMachine()
        self.analyst = AnalystAgent()
        self.critic = CriticAgent()

    async def route_task(self, scenario: str, payload: dict):
        state = self.state_machine.initialize(payload)

        # Hardcoded deterministic flow (No LLM routing)
        for attempt in range(3):  # max_retries
            # 1. Agent does the work
            draft_result = await self.analyst.execute(state)

            # 2. Critic evaluates
            evaluation = await self.critic.evaluate(draft_result)

            if evaluation.get("approved"):
                return draft_result
            else:
                state["feedback"] = evaluation.get("feedback")

        return {"error": "Task failed after max retries due to critic rejection."}
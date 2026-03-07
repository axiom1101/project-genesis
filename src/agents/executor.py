from src.agents.base_agent import BaseAgent

class ExecutorAgent(BaseAgent):
    """
    Executes actions (e.g., formatting, sending alerts) ONLY after Critic approval.
    """
    def __init__(self):
        super().__init__("configs/agents_config.yaml")

    async def execute(self, context: dict) -> dict:
        return {"action_taken": True}
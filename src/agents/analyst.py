from src.agents.base_agent import BaseAgent

class AnalystAgent(BaseAgent):
    """
    Analyzes data based on the provided context.
    Stateless: forgets everything after returning the result.
    """
    def __init__(self):
        super().__init__("configs/agents_config.yaml")

    async def execute(self, context: dict) -> dict:
        # TODO: Call LLM API with context and system prompt
        return {"analysis": "Mocked analysis result based on data."}
class ContextManager:
    """
    Builds the final prompt context by combining:
    1. Operational State
    2. Semantic Memory (RAG)
    3. Persistent Facts
    """
    def build_context(self, task_payload: dict) -> str:
        return "Compiled context for LLM."
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract Base Class for all Intelligence Units.
    Enforces strict input/output contracts.
    """
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)

    def _load_config(self, path):
        # Load YAML config for prompts and limits
        return {}

    @abstractmethod
    async def execute(self, context: dict) -> dict:
        pass
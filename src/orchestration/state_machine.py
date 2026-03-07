class StateMachine:
    """
    Tracks the operational state of the current task.
    """
    def initialize(self, payload: dict) -> dict:
        return {
            "status": "initialized",
            "original_payload": payload,
            "history":[],
            "feedback": None
        }
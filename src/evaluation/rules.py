"""
Hardcoded deterministic rules for the Evaluation Layer.
E.g., Regex checks, JSON schema validation, threshold checks.
"""
def validate_json_schema(payload: dict) -> bool:
    return True
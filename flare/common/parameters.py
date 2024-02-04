def boolean_parameter(value: str) -> bool:
    if isinstance(value, str):
        return value.lower() == "true"
    else:
        return False

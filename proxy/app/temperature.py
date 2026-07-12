def temperature_from_raw(raw: int) -> float:
    """Convert raw int16 temperature to degrees (divide by 10)."""
    return raw / 10.0

def pressure_from_raw(raw: int) -> float:
    """Convert raw int16 pressure to bar (divide by 100)."""
    return raw / 100.0

from datetime import datetime, timezone


class Temperature():
    def __init__(self, value: float, timestamp: datetime = datetime.now(timezone.utc)):
        self.value = self._check_valid_temperature(value)
        self.timestamp = timestamp

    def _check_valid_temperature(self, value: float) -> float:
        if value > 45:
            raise ValueError("Temperature cannot be higher than 45")
        if value < -10:
            raise ValueError("Temperature cannot be lower than -10")
        return value

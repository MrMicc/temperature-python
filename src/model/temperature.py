from datetime import datetime, timezone
from typing import Optional


class Temperature():
    def __init__(self, value: float, timestamp: Optional[datetime] = None):
        self.value = self._check_valid_temperature(value)
        self.timestamp = timestamp or datetime.now(timezone.utc)
        self.id = self._generate_id_maks(self.timestamp)

    def _generate_id_maks(self, timestamp):
        time = self._convert_to_timestamp(timestamp)
        return time.strftime("%Y%m%d%H%M%S")

    def _convert_to_timestamp(self, timestamp):
        if isinstance(timestamp, str):
            return datetime.fromisoformat(timestamp)
        return timestamp

    def _check_valid_temperature(self, value: float) -> float:
        if value > 45:
            raise ValueError("Temperature cannot be higher than 45")
        if value < -10:
            raise ValueError("Temperature cannot be lower than -10")
        return value

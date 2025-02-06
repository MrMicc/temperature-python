from model.enum_alerts import EnumAlerts
from model.temperature import Temperature


class TemperatureAlert():

    def __init__(self, high_threshold: float = 24, low_threshold: float = 21):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

    def check(self, temperature: Temperature) -> str:
        if temperature.value > self.high_threshold:
            return EnumAlerts.HIGH.value
        if temperature.value < self.low_threshold:
            return EnumAlerts.LOW.value

        return EnumAlerts.NORMAL.value

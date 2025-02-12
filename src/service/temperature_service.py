from model.sensor import SensorInterface
from model.alerts import TemperatureAlert
from model.temperature import Temperature


class TemperatureService():

    def __init__(self, low_threshold: float, high_threshold: float, sensor: SensorInterface):
        self.alert = TemperatureAlert(
            low_threshold=low_threshold, high_threshold=high_threshold)
        self.sensor = sensor

    def process_temperature(self) -> dict:

        temperature_value = self.sensor.get_temperature()
        temperature = Temperature(temperature_value)
        result = self.alert.check(temperature)

        return {"temperature": temperature, "alert": result}

from model.sensor import SensorInterface
from model.alerts import TemperatureAlert
from model.temperature import Temperature
from persistence.temperature_repository import TemperatureRepository


class TemperatureService():

    def __init__(self, low_threshold: float, high_threshold: float, sensor: SensorInterface, repository: TemperatureRepository):
        self.alert = TemperatureAlert(
            low_threshold=low_threshold, high_threshold=high_threshold, repository=repository)
        self.sensor = sensor
        self.repository = repository

    def process_temperature(self) -> dict:

        temperature_value = self.sensor.get_temperature()
        temperature = Temperature(temperature_value)
        self.repository.save(temperature)

        result = self.alert.check(temperature)

        return {"temperature": temperature, "alert": result}

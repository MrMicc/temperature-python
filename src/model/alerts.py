from statistics import mean
from model.enum_alerts import EnumAlerts
from model.temperature import Temperature
from persistence.temperature_repository import SqliteTemperatureRepository, TemperatureRepository
from errors.custom_errors import NoDataFoundError


class TemperatureAlert():

    def __init__(self, high_threshold: float = 24, low_threshold: float = 21, reading_count: int = 10, repository: TemperatureRepository =
                 SqliteTemperatureRepository("temperature.db")):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.temperature_repository = repository
        self.reading_count = reading_count

    def check(self, temperature: Temperature) -> str:
        if temperature.value > self.high_threshold:
            return EnumAlerts.HIGH.value
        if temperature.value < self.low_threshold:
            return EnumAlerts.LOW.value

        return EnumAlerts.NORMAL.value

    def check_mean_temperature(self) -> dict:
        temperature_list = self.temperature_repository.get_temperature_list(
            self.reading_count)

        mean_temperature = self._get_mean(temperature_list)
        alert = self.check(mean_temperature)
        return {"temperature": mean_temperature, "alert": alert}

    def _get_mean(self, temperature_list: list[Temperature]) -> Temperature:
        if temperature_list:
            mean_temperature = mean(temp.value for temp in temperature_list)
            return Temperature(mean_temperature)
        raise NoDataFoundError(
            f"No data found on temperature_list: {temperature_list}")

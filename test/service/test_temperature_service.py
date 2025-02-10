
import pytest
from service.temperature_service import TemperatureService
from model.sensor import SensorInterface
from datetime import datetime, timezone


class SensorMock(SensorInterface):
    def __init__(self, value: float):
        self.temperature_value = value

    def get_temperature(self) -> float:
        return self.temperature_value


class TestTemperatureService():

    @pytest.mark.parametrize("low_threshold, high_threshold, value", [(20, 30, SensorMock(30.1)), (10, 20, SensorMock(22))])
    def test_temperature_service_with_high_alert(self, low_threshold, high_threshold, value):
        service = TemperatureService(
            low_threshold=low_threshold, high_threshold=high_threshold, sensor=value)
        result = service.process_temperature()

        expected = {"temperature": value.get_temperature(),
                    "alert": "High temperature", "timestamp": datetime.now(timezone.utc)}
        assert result["temperature"] == expected["temperature"]
        assert result["alert"] == expected["alert"]
        assert result["timestamp"].strftime(
            "%Y-%m-%d %H:%M") == expected["timestamp"].strftime("%Y-%m-%d %H:%M")

    @pytest.mark.parametrize("low_threshold, high_threshold, value", [(20, 30, SensorMock(19)), (10, 20, SensorMock(9.9))])
    def test_temperature_service_with_low_alert(self, low_threshold, high_threshold, value):
        service = TemperatureService(
            low_threshold=low_threshold, high_threshold=high_threshold, sensor=value)
        result = service.process_temperature()
        expected = {"temperature": value.get_temperature(),
                    "alert": "Low temperature", "timestamp": datetime.now(timezone.utc)}
        assert result["temperature"] == expected["temperature"]
        assert result["alert"] == expected["alert"]
        assert result["timestamp"].strftime(
            "%Y-%m-%d %H:%M") == expected["timestamp"].strftime("%Y-%m-%d %H:%M")

    @pytest.mark.parametrize("low_threshold, high_threshold, value", [(20, 30, SensorMock(25)), (10, 20, SensorMock(15))])
    def test_temperature_service_with_normal_alert(self, low_threshold, high_threshold, value):
        service = TemperatureService(
            low_threshold=low_threshold, high_threshold=high_threshold, sensor=value)
        result = service.process_temperature()
        expected = {"temperature": value.get_temperature(),
                    "alert": "Normal temperature", "timestamp": datetime.now(timezone.utc)}
        assert result["temperature"] == expected["temperature"]
        assert result["alert"] == expected["alert"]
        assert result["timestamp"].strftime(
            "%Y-%m-%d %H:%M") == expected["timestamp"].strftime("%Y-%m-%d %H:%M")

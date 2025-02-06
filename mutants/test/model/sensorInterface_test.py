import pytest
from src.model.sensorInterface import Sensor


class SensorMock(Sensor):

    def ler_temperatura(self) -> float:
        return 25.5


class TestSensor():
    def test_ler_temperatura_retorna_valor(self):
        sensor = SensorMock()
        result = sensor.ler_temperatura()
        assert isinstance(result, float)

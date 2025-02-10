from unittest.mock import MagicMock
import pytest
from pyfirmata import Arduino
from model.sensor import Sensor


@pytest.fixture
def mock_board():
    mock = MagicMock(spec=Arduino)
    mock_pin = MagicMock()
    mock.analog = [mock_pin]

    mock_pin.read.return_value = 0.4897  # 21.0
    return mock


@pytest.fixture
def mock_board_with_no_pin():
    mock = MagicMock(spec=Arduino)
    mock_pin = MagicMock()
    mock.analog = [mock_pin]
    mock_pin.read.return_value = None
    return mock


def test_get_temperature(mock_board):
    sensor = Sensor(mock_board)

    result = sensor.get_temperature()

    assert result == 21.0


def test_none_analog_value(mock_board_with_no_pin):
    sensor = Sensor(mock_board_with_no_pin)

    result = sensor.get_temperature()

    assert result == 0


def test_get_value_from_sensor_pin_invalid_value(mock_board_with_no_pin):
    sensor = Sensor(mock_board_with_no_pin)
    result = sensor._Sensor__get_value_from_sensor_pin()
    assert result == 0


def test_get_value_from_sensor_pin_valid_value(mock_board):
    sensor = Sensor(mock_board)
    result = sensor._Sensor__get_value_from_sensor_pin()
    assert result == 0.4897


@pytest.mark.parametrize("kelvin_temp, expected_celsius", [
    (300, 26.85),
    (0, -273.15),
    (373.15, 100),
    (310.15, 37),
    (500, 226.85)
])
def test_kelvin_to_celsius(mock_board, kelvin_temp, expected_celsius):
    sensor = Sensor(mock_board)
    kelvin_temp = 300
    expected_celsius = round(kelvin_temp - 273.15, 2)
    result = sensor._Sensor__transform_kelvin_to_celsius(kelvin_temp)
    assert result == expected_celsius

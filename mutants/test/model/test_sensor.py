from unittest.mock import MagicMock
from pyfirmata import Arduino
from model.sensor import Sensor
import pytest


@pytest.fixture
def mock_board():
    mock_board = MagicMock(spec=Arduino)
    mock_pin = MagicMock()
    mock_board.analog = [mock_pin]

    mock_pin.read.return_value = 0.4897  # 21.0
    return mock_board


@pytest.fixture
def mock_board_with_no_pin():
    mock_board = MagicMock(spec=Arduino)
    mock_pin = MagicMock()
    mock_board.analog = [mock_pin]
    mock_pin.read.return_value = None
    return mock_board


def test_get_temperature(mock_board):
    sensor = Sensor(mock_board)

    result = sensor.get_temperature()

    assert result == 21.0


def test_none_analog_value(mock_board_with_no_pin):
    sensor = Sensor(mock_board_with_no_pin)

    result = sensor.get_temperature()

    assert result == 0

from unittest.mock import MagicMock
from pyfirmata import Arduino
from src.model.sensor import Sensor
import pytest


@pytest.fixture
def mock_board():
    mock_board = MagicMock(spec=Arduino)
    mock_pin = MagicMock()
    mock_board.analog = [mock_pin]

    mock_pin.read.return_value = 0.5106  # 0.5171
    return mock_board


def test_get_temperature(mock_board):
    sensor = Sensor(mock_board)

    # 0.3402  # 0.4976  # 0.5191
 # 0.3314  # 0.5191
    # 0.5191
    result = sensor.get_temperature()

    assert result == 21.0

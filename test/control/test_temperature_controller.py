

from unittest.mock import MagicMock
import pytest
from pyfirmata import Arduino
from control.temperature_controller import TemperatureController


@pytest.fixture
def mock_board(mock_leds):
    mock = MagicMock(spec=Arduino)
    mock.get_pin = MagicMock(
        side_effect=lambda pin: mock_leds.get(pin, MagicMock()))
    return mock


@pytest.fixture
def mock_leds():
    led = {"d:8:o": MagicMock(), "d:9:o": MagicMock(),
           "d:10:o": MagicMock()}  # red, green,yello
    return led


def test_leds_with_high_temperature(mock_board, mock_leds):
    controller = TemperatureController(mock_board)
    controller.control_leds("High temperature")

    mock_leds["d:8:o"].write.assert_called_once_with(1)
    mock_leds["d:9:o"].write.assert_called_once_with(0)
    mock_leds["d:10:o"].write.assert_called_once_with(0)


def test_leds_with_low_temperature(mock_board, mock_leds):
    controller = TemperatureController(mock_board)
    controller.control_leds("Low temperature")

    mock_leds["d:8:o"].write.assert_called_once_with(0)
    mock_leds["d:9:o"].write.assert_called_once_with(0)
    mock_leds["d:10:o"].write.assert_called_once_with(1)


def test_leds_with_normal_temperature(mock_board, mock_leds):
    controller = TemperatureController(mock_board)
    controller.control_leds("Normal temperature")

    mock_leds["d:8:o"].write.assert_called_once_with(0)
    mock_leds["d:9:o"].write.assert_called_once_with(1)
    mock_leds["d:10:o"].write.assert_called_once_with(0)

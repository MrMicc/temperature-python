import time
import random
from pyfirmata import Arduino, util
from control.temperature_led_controller import TemperatureLedController
from model.sensor import Sensor, SensorInterface
from persistence.temperature_repository import SqliteTemperatureRepository, TemperatureRepository
from service.temperature_service import TemperatureService
from zoneinfo import ZoneInfo


class SensorMock(SensorInterface):
    def get_temperature(self) -> float:
        return random.randint(18, 28)


def run_temperature_monitor():
    board = Arduino('/dev/tty.usbmodem1101')
    repository = SqliteTemperatureRepository("temperature.db")
    it = util.Iterator(board)
    it.start()

    time_zone = ZoneInfo('America/Sao_Paulo')
    time_format = '%Y-%m-%d %H:%M:%S'
    temp_controller = TemperatureLedController(board)

    time.sleep(2)
    temperature_sensor = Sensor(board)
    process = TemperatureService(21, 24, temperature_sensor)

    while True:

        result = process.process_temperature()
        repository.save(result['temperature'])
        print(
            f"{result['temperature'].timestamp.astimezone(time_zone).strftime(time_format)} ## Temperature: {result['temperature'].value}C, Alert: {result['alert']}")
        temp_controller.control_leds(result['alert'])
        time.sleep(3)


if __name__ == "__main__":
    run_temperature_monitor()

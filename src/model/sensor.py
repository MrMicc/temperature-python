

from abc import abstractmethod, ABC
from pyfirmata import Arduino
import math


class SensorInterface(ABC):
    @abstractmethod
    def get_temperature(self) -> float:
        pass


class Sensor(SensorInterface):

    def __init__(self,  board: Arduino):
        self.board = board
        self.__setup_sensor_pin()
        self.sensor_value = self.__get_value_from_sensor_pin()

    def __get_value_from_sensor_pin(self):
        voltage = self.sensor_pin.read()
        if voltage is None:
            return 0
        return voltage

    def __setup_sensor_pin(self):
        self.sensor_pin = self.board.analog[0]
        self.sensor_pin.enable_reporting()

    def get_temperature(self) -> float:
        analog_value = self.__get_value_from_sensor_pin()  # Retorna um valor entre 0 e 1
        temperature = self.__transform_anlog_value_to_temperature(analog_value)
        return temperature

    def __transform_anlog_value_to_temperature(self, analog_value):
        if analog_value:
            voltage = self.__convert_analog_value_to_voltage(analog_value)
            pullup_resistor = self.__calculate_pullup(voltage)
            resistance = self.__calculate_circuit_resistance(voltage,
                                                             resistor=pullup_resistor)

            kelvin_temperature = self.__calculate_steinhart_hart_formula(
                resistance)
            celsius_temperature = self.__transform_kelvin_to_celsius(
                kelvin_temperature)
            return celsius_temperature
        return 0

    def __convert_analog_value_to_voltage(self, analog_value, vcc=5):
        voltage = analog_value * vcc
        return voltage

    def __calculate_pullup(self, voltage):
        pullup = self.__calculate_circuit_resistance(voltage)
        return pullup

    def __calculate_circuit_resistance(self, voltage, resistor=13000, vcc=5):
        resistance = resistor * ((vcc / voltage) - 1)
        return resistance

    def __calculate_steinhart_hart_formula(self, resistance, A=0.001129148,
                                           B=0.000234125, C=0.0000000876741):
        kelvin_temperature = 1 / \
            (A + (B * math.log(resistance)) + (C * math.log(resistance) ** 3))
        return kelvin_temperature

    def __transform_kelvin_to_celsius(self, kelvin_temperature):
        celsius_temperature = kelvin_temperature - 273.15
        return round(celsius_temperature, 2)

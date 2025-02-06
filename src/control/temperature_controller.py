from pyfirmata import Arduino


class TemperatureController():

    def __init__(self, board: Arduino):
        self.board = board
        self.red_led = self.board.get_pin('d:8:o')
        self.green_led = self.board.get_pin('d:9:o')
        self.yellow_led = self.board.get_pin('d:10:o')

    def control_leds(self, alert_type):
        if alert_type == "High temperature":
            self.__turn_red_on()
        if alert_type == "Low temperature":
            self.__turn_yellow_on()
        if alert_type == "Normal temperature":
            self.__turn_green_on()

    def __turn_red_on(self):
        self.red_led.write(1)
        self.yellow_led.write(0)
        self.green_led.write(0)

    def __turn_yellow_on(self):
        self.red_led.write(0)
        self.yellow_led.write(1)
        self.green_led.write(0)

    def __turn_green_on(self):
        self.red_led.write(0)
        self.yellow_led.write(0)
        self.green_led.write(1)

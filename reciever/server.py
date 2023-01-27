import os.path

from flask import Flask, json

# api = Flask(__name__)
# light_switch = None


def create_app():
    app = Flask(__name__)
    light_switch = LightSwitch()


    @app.route("/on", methods=['GET'])
    def turn_on():
        light_switch.turn_on()
        return "success"

    @app.route("/off", methods=['GET'])
    def turn_off():
        light_switch.turn_off()
        return "success"
    return app

class LightSwitch:
    def __init__(self):
        ""
        self.GPIO_CONTROLLER = GPIOController(203, GPIOController.GPIO_OUT)

    def turn_on(self):
        self.GPIO_CONTROLLER.set_high()

    def turn_off(self):
        self.GPIO_CONTROLLER.set_low()


class GPIOController:
    GPIO_OUT = "out"
    GPIO_IN = "in"
    GPIO_VAL_HI = "1";
    GPIO_VAL_LO = "0";

    def __init__(self, GPIO_PIN, GPIO_DIRECTION):
        self.GPIO_BASE_PATH = "/sys/class/gpio";
        self.GPIO_DIR = GPIO_DIRECTION;
        self.GPIO_PIN = GPIO_PIN
        self.GPIO_PATH = self.GPIO_BASE_PATH + "/gpio" + str(self.GPIO_PIN)
        self.value_file = None

        if not os.path.isdir(self.GPIO_PATH):
            export_file = open(self.GPIO_BASE_PATH + "/export", 'w')
            export_file.write(str(self.GPIO_PIN))
            export_file.flush()

        direction_file = open(self.GPIO_PATH + "/direction", 'w')
        direction_file.write(self.GPIO_DIR)
        direction_file.flush()


    def set_low(self):
        self.set_value_file(self.GPIO_VAL_LO)

    def set_high(self):
        self.set_value_file(self.GPIO_VAL_HI)

    def set_value_file(self, value):
        if not self.value_file:
            self.value_file = open(self.GPIO_PATH + '/value', 'w')
        self.value_file.write(value)
        self.value_file.flush()

if __name__ == '__main__':
        api.run()
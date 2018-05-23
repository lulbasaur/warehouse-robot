

class TCPFeedback(object):
    def __init__(self):
        self.last_action = None
        self.temperature = None
        self.humidity = None
        self.gyro = None
        self.proximity = None
        self.mode = None

    @property
    def last_action(self):
        return self._last_action

    @last_action.setter
    def last_action(self, value):
        self._last_action = value
        if self._last_action is None:
            self._last_action = 0

    @last_action.deleter
    def last_action(self):
        del self._last_action

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        if self._temperature is None:
            self._temperature = 1

    @temperature.deleter
    def temperature(self):
        del self._temperature

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self, value):
        self._humidity = value
        if self._humidity is None:
            self._humidity = 1

    @humidity.deleter
    def humidity(self):
        del self._humidity

    @property
    def gyro(self):
        return self._gyro

    @gyro.setter
    def gyro(self, value):
        self._gyro = value
        if self._gyro is None:
            self._gyro = 1

    @gyro.deleter
    def gyro(self):
        del self._gyro

    @property
    def proximity(self):
        return self._proximity

    @proximity.setter
    def proximity(self, value):
        self._proximity = value
        if self._proximity is None:
            self._proximity = 1

    @proximity.deleter
    def proximity(self):op
        del self._proximity

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        # auto/manual 0/1
        self._mode = value
        if self._mode is None:
            self._mode = 0

    @mode.deleter
    def mode(self):
        del self._mode

    def mode_to_string(self):
        if self._mode is 0:
            return "Automatic"
        elif self._mode is 2:
            return "Stopped"
        else:
            return "Manual"

    def action_to_string(self):
        move_string = ""
        if self._mode is 1:
            if self._last_action is 0:
                move_string = "LEFT"
            elif self._last_action is 1:
                move_string = "FORWARD"
            elif self._last_action is 2:
                move_string = "RIGHT"
            elif self._last_action is 3:
                move_string = "BACKWARD"
            elif self._last_action is 4:
                move_string = "LIFTING"
            else:
                move_string = "No move"
        else:
            if self._last_action is 0:
                move_string = "Prioritized region 0"
            elif self._last_action is 1:
                move_string = "Prioritized region 1"
            elif self._last_action is 2:
                move_string = "Prioritized region 2"
            elif self._last_action is 3:
                move_string = "Prioritized region 3"
            else:
                move_string = "No move"
        return move_string

    def print_feedback(self):
        print("")
        print("--------- Feedback ---------")
        print("Mode: ", self.mode_to_string())
        print("Action: ", self.action_to_string())
        print("Temperature: ", self._temperature, "degrees")
        print("Humidity: ", self._humidity, "%")
        print("Gyroscope: ", self._gyro, "degrees")
        print("Proximity: ", self._proximity, "cm")
        print("----------------------------")
        print("")

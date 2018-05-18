
class TCPFeedback(object):
    def __init__(self):
        self.last_action = None
        self.temperature = None
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


    def data_print(self):
        print("Data: {}, {}").format(self._last_action, self._temperature)

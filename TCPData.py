from types import *


class TCPData(object):
    def __init__(self):
        self.mode = None
        self.option = None

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        # auto/manual/stop 0/1/2
        self._mode = value
        if self._mode is None:
            self._mode = 0

    @mode.deleter
    def mode(self):
        del self._mode

    @property
    def option(self):
        return self._option

    @option.setter
    def option(self, value):
        self._option = value
        if self._option is 0:
            self._option = 4
        if self._option is 2:
            self._option = 3
        if self._option is 3:
            self._option = 2

        if self._option is None:
            self._option = 1

    @option.deleter
    def option(self):
        del self._option

    def data_print(self):
        print("Data: {}, {}").format(self._mode, self._option)

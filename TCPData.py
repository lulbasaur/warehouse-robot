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
        # auto/manual 0/1
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
        if self._option is None:
            self._option = 1

    @option.deleter
    def option(self):
        del self._option

    def data_print(self):
        print("Data: {}, {}").format(self.mode, self.option)

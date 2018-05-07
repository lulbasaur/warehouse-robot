from types import *


class TCPData(object):
    def __init__(self):
        # init with auto/manual 0/1
        self.mode = -1
        self.option = -1

    def set_mode(self, mode):
        assert type(mode) is IntType, "mode is not an integer: %r" % mode
        self.mode = mode
        if self.option == -1:
            self.option = 0

    def set_option(self, option):
        assert type(option) is IntType, "option is not an integer: %r" % option
        self.option = option
        if self.mode == -1:
            self.option = 1

    def data_print(self):
        print("Data: {}, {}").format(self.mode, self.option)

    def data_get(self):
        return {self.mode, self.option}

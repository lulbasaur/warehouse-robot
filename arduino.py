import bluetooth_connection


class arduino(object):
    def __init__(self, arduino_address, ardiuno_port):
        self.arduino = bluetooth_connection.bluetooth_connection(robot_address, robot_port)
        self.arduino.listen()


    def __del__(self):
        self.arduino.close()


    def send(self, message):
        self.arduino.send(message);


    def receive(self):
        return self.arduino.receive()

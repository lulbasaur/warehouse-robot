import socket

class bluetooth_connection(object):
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.backlog = 1
        self.packet_size = 1024
        self.incomming_connection = False

    #Connect to a bluetooth server. For us this is the robot.
    def connect(self):
        self.connection = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.connection.connect((self.address, self.port))
        print("[Bluetooth] Connectection to server established")


    #Send message. Assumes byte stream i provided
    def send(self, message):
        self.connection.sendall(message)


    #Sets up listening interface.
    def listen(self):
        self.connection = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind((self.address, self.port))
        self.connection.listen(self.backlog)


    #Get data from robot
    def receive(self):
        if not self.incomming_connection:
            self.incomming_connection, self.incomming_address = self.connection.accept()
            print("Client accepted")
        data = self.incomming_connection.recv(self.packet_size)
        print("Data received")
        return data


    def close(self):
        try:
            self.connection.close()
        except:
            print("[Bluetooth] Server connection did not want to close")

        try:
            self.incomming_connection.close()
        except:
            print("[Bluetooth] Client connection didnt want to close")



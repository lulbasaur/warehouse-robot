

import socket

class bluetooth_connection(object):
    def __init__(self, adress, port):
        self.address = adress
        self.port = port
        self.backlog = 1
        self.packet_size = 1024

    def connect():
        self.connection = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.connection.connect((self.address, self.port))

    def send(message):
        self.connection.send(bytes(message, 'UTF-8'))

    def listen():
        self.connection = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.connection.bind((self.address, self.port))
        self.connection.listen(self.backlog)

    def receive():
        incomming_connection, incomming_address = self.connection.accept()
        data = incomming_connection.recv(self.packet_size)
        return data

    def close():
        self.connection.close()




class robot(object):
    def __init__(self, address, port):
        self.bluetooth_client = bluetooth_connection(address, port)
        self.bluetooth_server = bluetooth_connection("SERVER_ADDRESS pls fix", "SERVER PORT fix")


    def __del__(self):
        self.bluetooth_client.close()
        self.bluetooth_server.close()

    
    """ TODO """
    # Send Navigation
    # Receive and forward Status to client
    # 


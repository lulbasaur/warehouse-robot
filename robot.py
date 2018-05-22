import socket

class bluetooth_connection(object):
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.backlog = 1
        self.packet_size = 1024


    #Connect to a bluetooth server. For us this is the robot. 
    def connect(self):
        self.connection = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.connection.connect((self.address, self.port))

    
    #Send message. Assumes byte stream i provided
    def send(self, message):
        self.connection.sendall(message)


    #Sets up listening interface. 
    def listen(self):
        self.connection = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind((self.address, self.port))
        self.connection.listen(self.backlog)
        self.incomming_connection, self.incomming_address = self.connection.accept()


    #Get data from robot
    def receive(self):
        data = self.incomming_connection.recv(self.packet_size)
        return data


    def close(self):
        try:
            self.connection.close()
        except:
            print "Server connection didn̈́t want to close"

        try:
            self.incomming_connection.close()
        except:
            print "Robot connection didnt want to close"




class robot(object):
    def __init__(self, robot_address, robot_port, server_address, server_port):
        self.bluetooth_client = bluetooth_connection(robot_address, robot_port)
        self.bluetooth_server = bluetooth_connection(server_address, server_port)

        self.bluetooth_client.connect()
        self.bluetooth_server.listen()


    def __del__(self):
        self.bluetooth_client.close()
        self.bluetooth_server.close()
   

    def send(self, message):
        self.bluetooth_client.send(message);
   

    def receive(self):
        return self.bluetooth_server.receive()











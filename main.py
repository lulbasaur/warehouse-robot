import socket
import threading

class ThreadedServer(object):
    def __init__(self, host, port):
        #host address and port
        self.host = host
        self.port = port
        #set socket variables
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen_for_incoming_connections(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            #time out if client is inactive
            client.settimeout(60)
            #spawn thread for each client
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listen_to_client(self, client, address):
        rx_data_size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    response = data
                    client.send(response)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    while True:
        print("Initiating Warehouse Server...")
        port_num = input("Enter port nr: ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedServer('',port_num).listen_for_incoming_connections()

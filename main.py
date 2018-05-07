import socket
import threading
import TCPData
import sys
import json
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)


class ThreadedServer(object):
    def __init__(self, host, port):
        #host address and port
        self.host = host
        self.port = port
        #set socket variables
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print('socket binded to port', port)
        #thread array
        self.threads = []


    def listen_for_incoming_connections(self):
        self.sock.listen(3)
        thread_id = 1
        while True:
            print("socket is listening")
            client, address = self.sock.accept()
            print('Connected to :', address[0], ':', address[1])
            #time out if client is inactive
            client.settimeout(30)
            #spawn thread for each client
            t=threading.Thread(name=str(thread_id), target=self.listen_to_client, args=(client,address))
            self.threads.append(t)
            thread_id = thread_id+1
            t.start()

    def listen_to_client(self, client, address):
        #recieve buffer
        rx_data_size = 1024
        while True:
            try:
                data_rx = client.recv(rx_data_size)
                if data_rx:
                    logging.debug('Data recieved')
                    #decode data - json probably
                    response = data_rx.decode('utf-8')
                    print(response)#debug, todo: remove
                    #send echo
                    client.sendall(response.encode('utf-8'))
                else:
                    raise ConnectionError('Client disconnected')
            except ConnectionError:
                logging.debug('Connection error wih client: %s', client)
                client.close()
                return False
            except socket.timeout:
                logging.debug('Socket timeout with client: %s', client)
                client.close()
                return False

    def process_data(self, data):


        return data



if __name__ == "__main__":
    while True:
        print('Initiating Warehouse Server...')
        try:
            server_address = input('Enter server address: ')
            server_port = input('Enter port nr: ')
            server_port = int(server_port)
            break
        except ValueError('Value error: please reenter values'):
            pass

    ThreadedServer(server_address, server_port).listen_for_incoming_connections()

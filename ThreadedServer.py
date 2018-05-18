import TCPData
import socket
import threading
import sys
import json
import logging
import pickle

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 5005
BUFFER_SIZE = 1024
threads = []

class ClientThread(threading.Thread):
    '''
    Client Thread
    '''
    def __init__(self, __name, __client, __address):
        threading.Thread.__init__(self, name=str(__name))
        self.client = __client
        self.address = __address
    def run(self):
        '''
        run thread
        '''
        while True:
            try:
                data_rx = self.client.recv(BUFFER_SIZE)
                if data_rx:
                    logging.debug('Data recieved')
                    #decode data - pickle data
                    response_TCPData = pickle.loads(data_rx)
                    #print(response)#debug, todo: remove
                    print(response_TCPData.option)
                    print(response_TCPData.mode)
                    #send echo
                    self.client.sendall(pickle.dumps(response_TCPData))
                else:
                    raise ConnectionError('Client disconnected')
            except ConnectionError:
                logging.debug('Connection error wih client: %s', self.client)
                self.client.close()
                break
            except socket.timeout:
                logging.debug('Socket timeout with client: %s', self.client)
                self.client.close()
                break
        return False


def listen_for_incoming_connections(sock):

    sock.listen(3)
    thread_id = 1
    thread_name_temp = 'thread_'
    while True:
        print("socket is listening...")
        client, address = sock.accept()
        print('Connected to :', address[0], ':', address[1])
        #time out if client is inactive
        client.settimeout(30)
        #spawn thread for each client
        t_name = thread_name_temp+str(thread_id)
        t = ClientThread(t_name, client, address)
        threads.append(t)
        thread_id = thread_id+1
        t.start()

def main():
    '''
    Server
    '''
    print('Initiating Warehouse Server...')
    while True:
        try:
            host = input('Enter server address: ')
            port = input('Enter port nr: ')
            if host is '':
                host = DEFAULT_IP
            if port is '':
                port = DEFAULT_PORT
            port = int(port)
            break
        except ValueError('Value error: setting default'):
            pass

    #socket config
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host,port))
    print('Server IP: ', host)
    print('Server port: ', port)

    listen_for_incoming_connections(sock)



if __name__ == "__main__":
    main()

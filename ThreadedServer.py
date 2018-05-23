import sys
import socket
import threading
import json
import logging
import pickle
from TCPFeedback import TCPFeedback
from TCPData import TCPData
import robot

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 5005
BUFFER_SIZE = 1024
threads = []

class ClientThread(threading.Thread):
    '''
    Client Thread
    '''
    def __init__(self, __name, __client, __address, __robots):
        threading.Thread.__init__(self, name=str(__name))
        self.client = __client
        self.address = __address
        self.robots = __robots

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
                    #Forward data to robot. TODO need to specify which robot
                    self.robots[0].send(data_rx)
                    #Receive data from robot and forward it to the client
                    #self.poll_and_forward()
                    #get feedback
                    response_TCP_FB = TCPFeedback() #to remove
                    response_TCP_FB.last_action = response_TCPData.option #to remove
                    response_TCP_FB.mode = response_TCPData.mode #to be removed
                    response_TCP_FB.temperature = 30 #to be removed
                    response_TCP_FB.humidity = 30 #to be removed
                    response_TCP_FB.gyro = 123 #to be removed
                    response_TCP_FB.proximity = 1234 #to be removed
                    self.client.sendall(pickle.dumps(response_TCP_FB))
                    
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
            except(KeyboardInterrupt, SystemExit):
                self.client.close()
                break
            except:
                logging.debug('Unknown error with client: %s', self.client)
                self.client.close()
                break
        return False


    def poll_and_forward(self):
        while True:
            response = self.robot[0].receive()
            response = pickle.loads(TCPFeedback)
            if not response:
                break
            self.client.sendall(response)



def listen_for_incoming_connections(sock, robots):
    sock.listen(3)
    thread_id = 1
    thread_name_temp = 'thread_'
    while True:
        try:
            print("socket is listening...")
            client, address = sock.accept()
            print('Connected to :', address[0], ':', address[1])
            #time out if client is inactive
            client.settimeout(30)
            #spawn thread for each client
            t_name = thread_name_temp+str(thread_id)
            t = ClientThread(t_name, client, address, robots)
            threads.append(t)
            thread_id = thread_id+1
            t.setDaemon(True)
            t.start()
        except(KeyboardInterrupt, SystemExit):
            sock.close()
            break

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

    print('Connecting to robots')
    robots = []
    with open("robot.conf") as file:
        for line in file:
            robot_adr, server_adr, bluetooth_port = line.split(",")
            #try:
            robots.append(robot.robot(robot_adr, int(bluetooth_port), server_adr, int(bluetooth_port)))
            #except:
            #    print "Could not find robot on address/port " + robot_adr + "/" + robot_port + "."

    listen_for_incoming_connections(sock, robots)

if __name__ == "__main__":
    main()

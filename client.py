# Python client
# !/usr/bin/python
from __future__ import print_function

import socket
import pickle
import sys
from TCPData import TCPData
from TCPFeedback import TCPFeedback
# Enable for clearing terminal purposes
# import os

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 5005
BUFFER_SIZE = 4096


def connect_to_server(server_ip, server_port):
    try:
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_socket.connect((server_ip, server_port))
        print("Connected to server", server_ip, " on port ", server_port)
        save_recent_server(server_ip, server_port)
    except socket.error:
        print("Could not connect to server.")
        connection_menu()
    return s_socket


def send_msg_to_server(server_socket, msg):
    server_socket.sendall(msg.encode('utf-8'))


def recv_data_from_server(server_socket, buff_size):
    data = server_socket.recv(buff_size)
    return data


def close_connection_to_server(server_socket):
    server_socket.close()


# min, max range allowed in input
def get_int_input(default):
    int_input = input("> ")
    if int_input == '':
        int_input = default
    else:
        int_input = int(int_input)
    return int_input


# min, max range allowed in input
def get_and_validate_int_input(range_min, range_max, default):
    int_input = get_int_input(default)
    while not(int_input >= range_min and int_input <= range_max):
        print("Input not in the specified range [", range_min, range_max, "]")
        int_input = get_int_input(default)

    return int_input


def get_connection_input():
    pass


def save_recent_server(ip, port):
    f = open('recent_server', 'w')
    f.write(str(ip))
    f.write('\n')
    f.write(str(port))
    f.close()


def open_recent_server():
    f = open("recent_server", "r")
    server_ip = f.readline().rstrip('\n')
    server_port = f.readline().rstrip('\n')
    f.close()
    return {'ip': server_ip, 'port': server_port}


def connection_menu():
    print ("-----------------------------------")
    print ("1. Connect to server")
    print ("2. Connect to most recently used server")
    print ("3. List available servers")
    print ("4. Start videofeed here perhaps?")
    print ("5. Quit")
    print ("-----------------------------------")
    chosen_option = get_and_validate_int_input(1, 4, 1)

    if chosen_option == 1:
        print ("Server IP [Default 127.0.0.1]")
        server_ip = input("> ")
        if server_ip == "":
            server_ip = DEFAULT_IP
        print ("Server port [Default 5005]")
        server_port = input("> ")
        if server_port == "":
            server_port = DEFAULT_PORT
        else:
            server_port = int(server_port)
        s_socket = connect_to_server(server_ip, server_port)
    elif chosen_option == 2:
        server = open_recent_server()
        print ("Connecting to " + server['ip'] + ", on port " + server['port'])
        s_socket = connect_to_server(server['ip'], int(server['port']))
    elif chosen_option == 3:
        raise NotImplementedError
    elif chosen_option == 4:
        pass
    else:
        print("Exiting...")
        sys.exit()

    # Enable this to clear the terminal after each menu action/robot input
    # os.system('cls' if os.name == 'nt' else 'clear')
    return s_socket


def test_send_msg_to_server(s_socket):
    xxx = input("Msg: ")
    send_msg_to_server(s_socket, xxx)
    data = recv_data_from_server(s_socket, 1024)
    print ("received data:", data.decode('utf-8'))


def automatic_mode(data):
    print("Prioritize region 0-4 [Default 0] ")
    prio = get_and_validate_int_input(0, 4, 0)
    data.option = prio
    return data


def manual_mode(data):
    print("Move the robot [Default FORWARD]")
    print("0: LEFT, 1: FORWARD, 2: RIGHT, 3: BACKWARD")
    move = get_and_validate_int_input(0, 3, 1)
    data.option = move
    return data


def robot_menu(data):
    print("1. Automatic")
    print("2. Manual")
    print("3. Quit")
    chosen_option = get_and_validate_int_input(1, 3, 1)
    if chosen_option == 1:
        data.mode = 0
    elif chosen_option == 2:
        data.mode = 1
    else:
        sys.exit()
    return data


def serialize_data(data):
    serialized_data = pickle.dumps(data)
    return serialized_data


def send_serialized_data(s_socket, data):
    serialized_data = serialize_data(data)
    s_socket.sendall(serialized_data)


def deserialize_data(data):
    deserialized_data = pickle.loads(data)
    return deserialized_data


def receive_serialized_data(s_socket):
    serialized_data = s_socket.recv(BUFFER_SIZE)
    deserialized_data = deserialize_data(serialized_data)
    return deserialized_data

def print_feedback(feedback):
    feedback.print_feedback()


def main():
    s_socket = connection_menu()
    data = TCPData()
    feedback = TCPFeedback()

    while 1:
        data = robot_menu(data)
        if data.mode == 0:
            data = automatic_mode(data)
        elif data.mode == 1:
            data = manual_mode(data)
        else:
            raise ValueError

        send_serialized_data(s_socket, data)
        feedback = receive_serialized_data(s_socket)

        if isinstance(feedback.mode, int):
            print("Last action: ", feedback.last_action)
            print("Mode: ", feedback.mode)
            print("Temperature: ", feedback.temperature)
        else:
            print("Error")
    test_send_msg_to_server(s_socket)
    # robot_menu()
    # socket = connect_to_server(TCP_IP, TCP_PORT)
    # data = recv_data_from_server(new_socket, BUFFER_SIZE)
    close_connection_to_server(s_socket)
    # print "received data:", data


if __name__ == "__main__":
    main()

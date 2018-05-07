# Python client
# !/usr/bin/python
from __future__ import print_function

import socket
import pickle
import sys
import sys
from TCPData import TCPData
# Enable for clearing terminal purposes
# import os

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 5005
BUFFER_SIZE = 1024
# CURRENT_MODE = -1


def connect_to_server(server_ip, server_port):
    try:
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_socket.connect((server_ip, server_port))
        print("Connected to server", server_ip, " on port ", server_port)
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


def connection_menu():
    print ("-----------------------------------")
    print ("1. Connect to server")
    print ("2. List available servers")
    print ("3. Start videofeed here perhaps?")
    print ("4. Quit")
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
        raise NotImplementedError
    elif chosen_option == 3:
        raise NotImplementedError
        pass
    elif chosen_option == 3:
        pass
        # cv2?
    else:
        print("Exiting...")
        sys.exit()

    # Enable to clear terminal
    # os.system('cls' if os.name == 'nt' else 'clear')
    return s_socket


def test_send_msg_to_server(s_socket):
    xxx = input("Msg: ")
    send_msg_to_server(s_socket, xxx)
    data = recv_data_from_server(s_socket, 1024)
    print ("received data:", data.decode('utf-8'))


def robot_menu():
    print("1. Automatic")
    print("2. Manual")
    print("3. Quit")

    chosen_option = get_and_validate_int_input(1, 4, 4)
    data = TCPData()

    if chosen_option == 1:
        print("Prioritize region 0-4 [Default 0] ")
        prio = get_and_validate_int_input(0, 4, 0)
    # chosen_option = -1
    # while(chosen_option > 0 and chosen_option <= 4):
    chosen_option = get_and_validate_int_input(1, 4, 4)

    data = TCPData()
    if chosen_option == 1:
        prio = int(input("Prioritize region 0-4: [Default 0]"))
        data.set_mode(0)
        data.set_auto_prio(prio)
    elif chosen_option == 2:
        data.set_mode(1)
    else:
        sys.exit()


def main():
    # get_integer_input(0, 4, 2)
    s_socket = connection_menu()
    robot_menu()
    test_send_msg_to_server(s_socket)
    # robot_menu()
    # socket = connect_to_server(TCP_IP, TCP_PORT)
    # data = recv_data_from_server(new_socket, BUFFER_SIZE)
    close_connection_to_server(s_socket)
    # print "received data:", data


if __name__ == "__main__":
    main()

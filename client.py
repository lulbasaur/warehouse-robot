#Python client
#!/usr/bin/python

import socket
import sys
import os


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
#CURRENT_MODE = -1

def connect_to_server(server_ip, server_port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((server_ip, server_port))
        print("Connected to server", server_ip, " on port ", server_port)
    except:
        print("Could not connect to server.")
    return server_socket

def send_msg_to_server(server_socket, msg):
    server_socket.sendall(msg.encode('utf-8'))

def recv_data_from_server(server_socket, buff_size):
    data = server_socket.recv(buff_size)
    return data

def close_connection_to_server(server_socket):
    server_socket.close()

#min, max range allowed in input
def get_and_validate_input(min, max, default):
    int_input = input("> ")
    if(int_input == ''):
        int_input = default
    else:
        int_input = int(int_input)

    if(not(int_input >= min and int_input <= max)):
        print("Input not in the specified range [", min, max, "]")
        get_and_validate_input(min,max,default)
    else:
        return int_input

def create_socket_menu():
    print ("1. Connect to server")
    print ("2. Quit")
    chosen_option = get_and_validate_input(1,2,1)

    if chosen_option == 1:
        server_ip = input("Server IP [Default 127.0.0.1]: ")
        if server_ip == "":
            server_ip = TCP_IP

        server_port = input("Server port [Default 5005]: ")
        if server_port == "":
            server_port = TCP_PORT

        socket = connect_to_server(server_ip, server_port)
    else:
        sys.exit()

    #Enable to clear terminal
    #os.system('cls' if os.name == 'nt' else 'clear')
    return socket

def test_send_msg_to_server(socket):
    xxx = input("Msg: ")
    send_msg_to_server(socket, xxx)
    data = recv_data_from_server(socket, 1024)
    print ("received data:", data.decode('utf-8'))


def robot_menu():
    print("1. Automatic")
    print("2. Manual")
    print("3. Turn on video feed")
    print("4. Quit")
    #chosen_option = -1
    #while(chosen_option > 0 and chosen_option <= 4):
    chosen_option = get_and_validate_input(1,4,4)

    data = Data()

    if chosen_option == 1:

        prio = int(input("Prioritize region 0-4: [Default 0]"))
        data.set_mode(0)
        data.set_auto_prio(prio)
    elif chosen_option == 2:
        data.set_mode(1)
    elif chosen_option == 3:
        pass
        #cv2?
    else:
        sys.exit()

def main():
    #get_integer_input(0, 4, 2)
    socket = create_socket_menu()
    test_send_msg_to_server(socket)
    robot_menu()
    #socket = connect_to_server(TCP_IP, TCP_PORT)
    #data = recv_data_from_server(new_socket, BUFFER_SIZE)
    close_connection_to_server(socket)
    #print "received data:", data

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import carauto
import carmanually
import carauto
import globalvariable
import bluetoothmodule
import time
from threading import Thread
import ev3dev.ev3 as ev3
import pickle
from TCPData import TCPData


command = "0"

btn = ev3.Button()

def car_go():
    global command
    while(True):
        if(globalvariable.model == "A"):
            carauto.go_robot_a()
        while(globalvariable.model == "M"):
            carmanually.go_robot_m(command)
            command = "0"
            time.sleep(1)

if __name__ == '__main__':
    bt = Thread(target=bluetoothmodule.start_bluetooth)
    bt.setDaemon(True)
    bt.start()

    cg = Thread(target=car_go)
    cg.setDaemon(True)
    cg.start()
    
    mode_string = {0:"A", 1:"M", 2:"S"}
    

    while(btn.any()==False):
        if isinstance(globalvariable.bt_server_message, bytes):
            command_object = pickle.loads(globalvariable.bt_server_message)
            globalvariable.model = mode_string[command_object.mode]
            command = str(command_object.option)
        
        if (globalvariable.bt_server_message == "A"):
            globalvariable.model = "A"
        elif (globalvariable.bt_server_message == "M"):
            globalvariable.model = "M"
        elif (globalvariable.bt_server_message == "S"):
            globalvariable.stop_now = True
        elif (globalvariable.bt_server_message == "1"):
            command = "1"
        elif (globalvariable.bt_server_message == "2"):
            command = "2"
        elif (globalvariable.bt_server_message == "3"):
            command = "3"
        elif (globalvariable.bt_server_message == "4"):
            command = "4"
        elif (globalvariable.bt_server_message == "5"):
            command = "5"

        if (globalvariable.bt_arduino_message == "Something"):
            find_terminal = True

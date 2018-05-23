from bluetooth import *

# Create the client socket
client_socket=BluetoothSocket( RFCOMM )

client_socket.connect(("CC:78:AB:51:51:97", 1))

client_socket.send("M")

print ("Finished")

client_socket.close()
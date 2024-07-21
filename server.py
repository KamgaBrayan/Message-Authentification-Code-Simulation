# The socket module allows for low-level network access programming in Python
import socket
import select
import os
import hmac
import hashlib

# Change the working directory
os.chdir('/home/ghosk/Documents/MAC')

# Functions needed for the server to work

# Retrieve the secret key entered by the first user from the key file
def getKey():
    with open("key.txt", 'r') as key_file:
        keys = key_file.readlines()
    key = keys[0]
    return key

# Encryption function
def encrypt_mac(message):
    key = getKey()
    encoded_key = str.encode(key)
    hmac1 = hmac.new(encoded_key, message.encode('UTF-8'), hashlib.sha1)
    digest_value = hmac1.hexdigest()
    return digest_value

# Function to test the integrity of MACs
def test_mac(mac1, mac2):
    return hmac.compare_digest(mac1, mac2)

def read_message(name):
    # Retrieve the message
    with open(f"message_{name}.txt", 'r') as msg_file:
        message = msg_file.readline()

    # Open the MAC file
    with open(f"mac_{name}.txt", 'r') as mac_file:
        mac_bin_send = mac_file.readline().encode('UTF-8')  # This is the MAC accompanying the message

    # If a message is received, recalculate the MAC using the common key between the two interlocutors
    mac_bin = str(encrypt_mac(message)).encode('UTF-8')  # Recalculate the MAC from the message

    # If the MAC (file mac.txt) is modified, notify that the message has been intercepted
    if test_mac(mac_bin, mac_bin_send):
        print(f"{name} >> {message}   (Message intact)")
    else:
        print(f"{name} >> {message}   (Message corrupted!)")

# Main code

# Clear the file that will contain the keys
with open("key.txt", 'w'):
    pass

host = '127.0.0.1'  # Localhost commonly used to identify a machine on the network
port = 55555  # Random port associated with the application managing server requests

server_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket
server_sck.bind((host, port))  # Bind the host to the port
server_sck.listen()  # Put the server in listening mode for client connections

client_connected = True
socket_objects = [server_sck]
print("Welcome to this Chat!")
print("The principle of this Chat is simple: when you write your message and send it (press 'ENTER'), it remains in draft.\nWhen you press 'ENTER' a second time, the message is sent.")

while client_connected:
    readable, writable, exceptional = select.select(socket_objects, [], socket_objects)
    for socket_obj in readable:
        if socket_obj is server_sck:
            client, address = server_sck.accept()
            socket_objects.append(client)
        else:
            received_data = socket_obj.recv(128).decode("UTF-8")
            if received_data:
                val = received_data.split(' ')
                name = val[0]
                if len(val) == 3 and val[2] == '':
                    read_message(name)
                if received_data[0] == '!':
                    print(received_data)
            else:
                socket_objects.remove(socket_obj)
                print("1 participant has disconnected")
                print(f"{len(socket_objects) - 1} participants remaining")

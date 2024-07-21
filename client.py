import socket
import os
import hmac
import hashlib

# Change the working directory
os.chdir('/home/ghosk/Documents/MAC')

# Functions needed for the client to work

# Encryption function
def encrypt_mac(message):
    # Retrieve the correct key from the key file
    with open("key.txt", 'r') as key_file:
        keys = key_file.readlines()
    key = keys[0]
    encoded_key = str.encode(key)
    hmac1 = hmac.new(encoded_key, message.encode('UTF-8'), hashlib.sha1)
    digest_value = hmac1.hexdigest()
    return digest_value

# Function to write received data into a file to store the conversation
def write_to_file(received_data, name):
    # Open the file to save the message in draft
    with open(f"message_{name}.txt", 'w') as msg_file:
        msg_file.write(received_data)
    
    # Create the MAC file
    with open(f"mac_{name}.txt", 'w') as mac_file:
        # Calculate the MAC and save it to the mac file
        mac_bin = encrypt_mac(received_data)
        mac_file.write(str(mac_bin))

# Function to allow people to converse through the chat by sharing the same key
def write_key(key_gift):
    with open("key.txt", "a") as key_file:
        key_file.write(key_gift + "\n")

# Function to check if the provided key is the correct one to access the chat
def is_correct_key(key):
    with open("key.txt", 'r') as key_file:
        keys = key_file.readlines()
    n = len(keys)
    return keys[0] == keys[n-1]

# Main code

# Create a TCP socket
client_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client using the server parameters
client_sck.connect(('127.0.0.1', 55555))
name = input("What is your name?\n")
key = input("Enter the key: ")
write_key(key)

# Verify that the client is authorized to join the chatroom
if __name__ == "__main__":
    if is_correct_key(key):
        print("The key is correct!\nYou are connected!")
        print("The principle of this Chat is simple: when you write your message and send it (press 'ENTER'), it remains in draft.\nWhen you press 'ENTER' a second time, the message is sent.")

        while True:
            # Messages entered are stored in the draft until an empty message is entered (pressing 'ENTER' without typing anything)
            message = input(f"{name} >> ")
            if len(message) != 0:
                write_to_file(message, name)
            client_sck.send(f"{name} >> {message}".encode("utf-8"))
    
    # If the key is incorrect, the client joins the chat but cannot participate, and it is reported on the server
    else:
        while True:
            print("The key is incorrect\nYou cannot participate in this Chat!\n(Each attempt will be reported)")
            void = input("")
            client_sck.send(f"!!!!! {name} is trying to join this Chat without the correct key! They can see this conversation!!!!!".encode("utf-8"))
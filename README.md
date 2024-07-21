# Chatbox with Message Authentication Code (MAC) System

## Overview

This project simulates a chatbox where multiple people can interact. The aim of the project is to implement a Message Authentication Code (MAC) system to ensure the integrity and authenticity of the messages exchanged between users. Messages are stored in text files, and any alteration by an attacker will be detected and signaled to the receiver.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Usage](#usage)
   - [Server](#server)
   - [Client](#client)
5. [Functions](#functions)
6. [File Structure](#file-structure)
7. [Explanation](#explanation)
8. [Security Considerations](#security-considerations)
9. [License](#license)

## Introduction

The chatbox project is designed to allow multiple users to communicate with each other securely. Each message sent by a user is accompanied by a MAC, which ensures that any tampering with the message can be detected. The server and client scripts handle the sending, receiving, and verification of messages.

## Features

- Multiple users can join and communicate in the chatbox.
- Each message is accompanied by a MAC to ensure message integrity.
- Messages are stored in text files.
- Any alteration in the messages is detected and signaled.
- Simple encryption and decryption using a shared secret key.

## Requirements

- Python 3.x
- Basic understanding of networking and socket programming

## Usage

### Server

1. Start the server:
```python
   python3 server.py
```
2. The server will start listening for client connections on 127.0.0.1 and port 55555.

### Client

1. Start the client:

```python
python3 client.py
```
2. Enter your name and the shared secret key when prompted.

3. Start sending messages. Messages will remain in draft until you press 'ENTER' twice.

4. If the entered key is incorrect, you will not be able to participate in the chat.

## Functions

### Server

1. **getKey()**:

    Retrieves the secret key from the key.txt file.

2. **encrypt_mac(message)**:

    Generates a MAC for the given message using the secret key.

3. **test_mac(mac1, mac2)**:

    Compares two MACs to check for integrity.

4. **read_message(name)**:

    Reads the message and its MAC from the respective files and verifies the integrity.

### Client

1. **encrypt_mac(message)**:

    Generates a MAC for the given message using the secret key.

2. **write_to_file(received_data, name)**:

    Writes the received message and its MAC to separate files.

3. **write_key(key)**:

    Writes the shared secret key to the key.txt file.

4. **is_correct_key(key)**:

    Verifies if the provided key matches the stored key.

## File structure

```php
/MAC/
│
├── client.py
├── server.py
├── key.txt
├── message_<username>.txt
└── mac_<username>.txt

```

## Explanation

### Client

- **Connecting to the Server** :
    The client script creates a TCP socket and connects to the server using the provided IP address and port.

- **Message Input** :
    The client prompts the user for their name and the shared secret key. The key is stored in key.txt and used for MAC generation.

- **Sending Messages** :
    Messages are entered by the user and stored in draft. When `ENTER` is pressed twice, the message is sent to the server along with its MAC.

- **Integrity Check** :
    The server checks the integrity of the message using the MAC and signals if the message has been tampered with.

### Server

- **Listening for Connections** :
    The server script creates a TCP socket, binds it to a specified IP address and port, and listens for client connections.

- **Handling Clients** :
    The server accepts connections from clients and adds them to the list of socket objects.

- **Receiving Messages** :
    The server receives messages from clients, splits the message to extract the username, and verifies the message integrity using the MAC.

- **Integrity Verification** :
    The server recalculates the MAC for the received message using the shared secret key and compares it with the received MAC. If they do not match, it signals that the message has been corrupted.

## Security Considerations

- **Shared Secret Key** :
    The security of the MAC system relies on the shared secret key. Ensure that the key is kept confidential and only shared with authorized users.

- **Message Integrity** :
    The MAC ensures that any tampering with the message can be detected. However, it does not prevent tampering. Use encryption for additional security.

- **File Permissions** :
    Ensure that the key and message files have appropriate permissions to prevent unauthorized access.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0). You are free to use, modify, and share the project for non-commercial purposes, provided that you give appropriate credit to the original author.

For more information, visit [License](./License.md).
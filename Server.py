import socket
import socketserver
from socket_functions import Socket_function
import time


class Server(Socket_function):
    def __init__(self):
        self.welcome_socket = socket.socket()
        self.welcome_socket.bind(('', 5005))
        self.welcome_socket.listen(10)
        self.game = Game()

    def run(self):
        # welcome server
        while len(self.game.clients) < 2:
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


server = Server()
server.run()

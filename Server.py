import socket
import socketserver
from socket_functions import Socket_function
from game import Game
from player import Player
import time


class Server(Socket_function):
    def __init__(self, player_number):
        print(1)
        self.welcome_socket = socket.socket()
        self.welcome_socket.bind(('', 5005))
        self.welcome_socket.listen(10)
        self.player_number = player_number
        self.game = Game()

    def run(self):
        # welcome server
        while len(self.game.players) < self.player_number:
            #time.sleep(1)
            print('Server open')
            komm_s, adress = self.welcome_socket.accept()
            
            with socketserver.TCPServer(("localhost", 0), None) as s:
                free_port = s.server_address[1]
            self.sendeStr(komm_s, str(free_port))
            komm_s.close()
            self.game.add_player(Player(free_port))
        self.welcome_socket.close()
        # start game
        self.game.run()


if __name__ == '__main__':
    serv = Server(6)
    serv.run()

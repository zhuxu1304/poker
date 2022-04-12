import socket
import socketserver
import time

from socket_functions import Socket_function
from game import Game
from player import Player
import threading


class Server(Socket_function):
    def __init__(self, player_number):
        print(1)
        self.welcome_socket = socket.socket()
        self.welcome_socket.bind(('', 5005))
        self.welcome_socket.listen(10)
        self.player_number = player_number
        self.game = Game()

    def open_player_socket(self, komm_s, adress):
        with socketserver.TCPServer(("localhost", 0), None) as s:
            free_port = s.server_address[1]
        self.sendeStr(komm_s, str(free_port))
        komm_s.close()
        print('closed')
        self.game.add_player(Player(free_port))
        print('added')

    def run(self):

        # welcome server
        players = 0
        while players < self.player_number:
            # time.sleep(1)
            print('Server open')
            komm_s, adress = self.welcome_socket.accept()
            t = threading.Thread(target=self.open_player_socket, args=(komm_s, adress))
            t.start()
            players += 1
            print('player number', players)

        self.welcome_socket.close()
        while len(self.game.players) < self.player_number:  # wait for all players to enter their name
            time.sleep(0.1)
        # start game
        self.game.run()


if __name__ == '__main__':
    serv = Server(5)
    serv.run()

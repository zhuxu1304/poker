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
        self.welcome_socket.bind(('', 15505))
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

    def send_player_number(self):
        self.number_socket = socket.socket()
        self.number_socket.bind(('',15506))
        self.number_socket.listen(10)
        while True:
            komm_s, adress = self.number_socket.accept()
            self.sendeStr(komm_s,str(self.player_number))
            komm_s.close()

    def run(self):
        # open number socket
        t_number = threading.Thread(target=self.send_player_number)
        t_number.start()

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




import socket
import socketserver
from socket_functions import Socket_function
from game import Game
from player import Player
import time


class Server(Socket_function):
    def __init__(self):
        self.welcome_socket = socket.socket()
        self.welcome_socket.bind(('', 5005))
        self.welcome_socket.listen(10)

        self.cards = [("Kreuz", 2), ("Kreuz", 3), ("Kreuz", 4), ("Kreuz", 5), ("Kreuz", 6), ("Kreuz", 7),
                      ("Kreuz", 8), ("Kreuz", 9), ("Kreuz", 10), ("Kreuz", 11), ("Kreuz", 12), ("Kreuz", 13),
                      ("Kreuz", 14),
                      ("Karo", 2), ("Karo", 3), ("Karo", 4), ("Karo", 5), ("Karo", 6), ("Karo", 7), ("Karo", 8),
                      ("Karo", 9), ("Karo", 10), ("Karo", 11), ("Karo", 12), ("Karo", 13), ("Karo", 14),
                      ("Herz", 2), ("Herz", 3), ("Herz", 4), ("Herz", 5), ("Herz", 6), ("Herz", 7), ("Herz", 8),
                      ("Herz", 9), ("Herz", 10), ("Herz", 11), ("Herz", 12), ("Herz", 13), ("Herz", 14),
                      ("Piek", 2), ("Piek", 3), ("Piek", 4), ("Piek", 5), ("Piek", 6), ("Piek", 7), ("Piek", 8),
                      ("Piek", 9), ("Piek", 10), ("Piek", 11), ("Piek", 12), ("Piek", 13), ("Piek", 14)]

        self.game = Game(self.cards)

    def run(self):
        # welcome server
        while len(self.game.players) < 5:
            komm_s, adress = self.welcome_socket.accept()
            print(1)
            with socketserver.TCPServer(("localhost", 0), None) as s:
                free_port = s.server_address[1]
            self.sendeStr(komm_s, str(free_port))
            komm_s.close()
            self.game.add_player(Player(free_port))
        self.welcome_socket.close()
        # start game
        self.game.run()

if __name__ == '__main__':
    server = Server()
    server.run()

from socket_functions import Socket_function


class Game():
    def __init__(self):
        self.clients = []
        self.round = 1

    def add_player(self, player):
        self.clients.append(player)

    def run(self):
        while True:
            for each in self.clients:
                each.run()
                print('aaa')

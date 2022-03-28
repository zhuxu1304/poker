from socket_functions import Socket_function


class Game():
    def __init__(self):
        self.players = []
        self.round = 1
        self.button = 0
        self.pot = 0
        self.community_cards = []

    def add_player(self, player):
        self.players.append(player)

    def run(self):
        while True:
            # set button, small and big blind
            button = self.players[self.button]
            small_blind = self.button + 1
            big_blind = self.button + 2



            for each in self.players:
                each.run()
                print('aaa')

from socket_functions import Socket_function
from random import choice
from rules import Rules


class Game(Rules):
    def __init__(self, cards):
        self.players = []
        self.round = 1
        self.button = 0
        self.pot = 0
        self.cards = cards
        self.community_cards = []

    def add_player(self, player):
        self.players.append(player)

    def run(self):
        while True:
            # set button, small and big blind
            button = self.players[self.button]
            small_blind = self.button + 1
            big_blind = self.button + 2
            self.cards, self.community_cards = self.get_random_deck(self.cards, 5)

            # give each player two cards
            for each in self.players:
                self.cards, cards = self.get_random_deck(self.cards, 5)
                each.set_card(cards)
                print(each.cards)


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

            # small and big blind pay in the pot
            self.players[small_blind].change_money(-50)
            self.pot += 50
            self.players[big_blind].change_money(-100)
            self.pot += 100

            # deliever cards
            self.cards, self.community_cards = self.get_random_deck(self.cards, 5)

            # give each player two cards
            for player in self.players:
                self.cards, cards = self.get_random_deck(self.cards, 2)
                player.set_card(cards)
                print(each.cards)

            # first round ask for action
            for player in self.players:
                player.ask_for_action_firstround()

            # reveal 3 cards

            # second round ask for action
            for player in self.players:
                player.ask_for_action()

            # reveal 1 card

            # third round ask for action
            for player in self.players:
                player.ask_for_action()

            # reveal 1 card

            # fourth round ask for action
            for player in self.players:
                player.ask_for_action()

            # announce winner, give him money in pot

            # reset pot, choose new button
            self.pot = 0
            self.button += 1

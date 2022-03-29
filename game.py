from socket_functions import Socket_function
from random import choice
from rules import Rules
import json


class Game(Rules):
    def __init__(self, cards):
        self.players = []
        self.current_players = []
        self.current_player = 0
        self.round = 1
        self.button = 0
        self.pot = 0
        self.cards = cards
        self.current_bet = 0
        self.community_cards = []

    def add_player(self, player):
        self.players.append(player)

    def send_to_all_player(self, message):
        for player in self.players:
            player.send(message)

    def set_next_player(self):
        if self.current_player < len(self.current_players) - 1:
            self.current_player += 1
        else:
            self.current_player = 0

    def set_previous_player(self):
        if self.current_player <= 0:
            self.current_player = len(self.current_players)
        else:
            self.current_player -= 1

    def run(self):
        # tell each player to start
        self.send_to_all_player('start')

        while True:
            # set button, small and big blind+
            button = self.players[self.button]
            small_blind = self.button + 1
            big_blind = self.button + 2

            # small and big blind pay in the pot+
            self.players[small_blind].change_money(-25)
            self.pot += 25
            self.players[big_blind].change_money(-50)
            self.pot += 50


            # add player to current_player+
            self.current_players = self.players[:]

            # deliever community cards+
            self.cards, self.community_cards = self.get_random_deck(self.cards, 5)
            self.self.send_to_all_player('1' + json.dumps(self.community_cards))

            # give each player two cards+
            for player in self.players:
                self.cards, cards = self.get_random_deck(self.cards, 2)
                player.set_card(cards)

            # set first player and first round ask for action+
            self.current_player = big_blind
            self.set_next_player()
            end = big_blind
            self.current_bet = 50
            while self.current_player != end:
                action = self.current_players[self.current_player].ask_for_action_firstround(self.current_bet)
                if action[0] == 'fold':
                    del self.current_players[self.current_player]
                elif action[0] == 'call':
                    self.pot += self.current_bet
                elif action[0] == 'raise':
                    self.current_bet = action[1]
                    self.pot += self.current_bet
                    end = self.current_player

                self.set_next_player()

            # reveal 3 cards+
            print(self.community_cards[:2])
            self.send_to_all_player('5')

            # second round ask for action
            self.current_player = small_blind
            self.set_previous_player()
            end = self.current_player
            self.set_next_player()
            self.current_bet = 50
            while self.current_player != end:
                action = self.current_players[self.current_player].ask_for_action(self.current_bet)
                if action[0] == 'fold':
                    del self.current_players[self.current_player]
                elif action[0] == 'call':
                    self.pot += self.current_bet
                elif action[0] == 'raise':
                    self.current_bet = action[1]
                    self.pot += self.current_bet
                    end = self.current_player
                elif action[0] == 'check':
                    pass

                self.set_next_player()
            # reveal 1 card

            # third round ask for action
            for player in self.current_players:
                player.ask_for_action()

            # reveal 1 card

            # fourth round ask for action
            for player in self.current_players:
                player.ask_for_action()

            # announce winner, give him money in pot

            # reset pot, choose new button
            self.pot = 0
            self.button += 1

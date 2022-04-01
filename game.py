import json
from random import choice
from rules import Rules
from socket_functions import Socket_function


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

    def get_next_player(self, pos):
        pos += 1
        return pos % len(self.players)

    def ask_all_players_for_action(self):
        pos = self.get_next_player(self.button)
        while True:
            if self.players[pos] in self.current_players:
                small_blind = self.players[pos]
                for i in len(self.current_players):
                    if self.current_players[i] == small_blind:
                        end = i
                break
            else:
                pos = self.get_next_player(pos)



        self.current_bet = 50
        while self.current_player != end or len(self.current_players) == 1:
            action = self.current_players[self.current_player].ask_for_action(self.current_bet)
            if action[0] == 'fold':
                self.current_player -= 1
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
        if len(self.current_players) == 1:
            self.winner = self.current_players[0]

    def run(self):
        # tell each player to start
        self.send_to_all_player('start')

        while True:
            # set button, small and big blind+
            button = self.players[self.button]
            small_blind = self.get_next_player(self.button)
            big_blind = self.get_next_player(self.get_next_player(self.button))

            # small and big blind pay in the pot+
            self.players[small_blind].change_money(-25)
            self.pot += 25
            self.players[big_blind].change_money(-50)
            self.pot += 50

            # add player to current_player+
            self.current_players = self.players[:]

            # deliever community cards+
            self.cards, self.community_cards = self.get_random_deck(self.cards, 5)
            self.send_to_all_player('b' + json.dumps(self.community_cards))

            # give each player two cards+
            for player in self.players:
                self.cards, cards = self.get_random_deck(self.cards, 2)
                player.set_cards(cards)

            # set first player and first round ask for action+
            self.winner = None
            self.current_player = big_blind
            self.set_next_player()
            end = big_blind
            self.current_bet = 50
            while self.current_player != end or len(self.current_players) == 1:
                action = self.current_players[self.current_player].ask_for_action_firstround(self.current_bet)
                if action[0] == 'fold':
                    del self.current_players[self.current_player]
                    self.current_player -= 1
                elif action[0] == 'call':
                    self.pot += self.current_bet
                elif action[0] == 'raise':
                    self.current_bet = action[1]
                    self.pot += self.current_bet
                    end = self.current_player

                self.set_next_player()
            if len(self.current_players) == 1:
                self.winner = self.current_players[0]

            if not self.winner:
                # reveal 3 cards+
                print(self.community_cards[:2])
                self.send_to_all_player('f')

                # second round ask for action+
                self.ask_all_players_for_action()

            if not self.winner:
                # reveal 1 card+
                print(self.community_cards[3])
                self.send_to_all_player('g')
                # third round ask for action+
                self.ask_all_players_for_action()
            if not self.winner:
                # reveal 1 card+
                print(self.community_cards[4])
                self.send_to_all_player('h')
                # fourth round ask for action+
                self.ask_all_players_for_action()
            if not self.winner:
                biggest = 0
                winner = []
                for player in self.current_players:  # find the winner
                    analyse = self.get_highest_combi(player.cards,self.community_cards)
                    points = analyse[2] + analyse[1][0][1]/100
                    if points >= biggest:
                        biggest = points
                        if len(winner) > 0: # if someone in list winner
                            if winner[0][1] == points:# if same points
                                winner.append((player, points))
                            else:# if this player has higher points than the player in the list winner
                                winner = []
                                winner.append((player, points))
                        else:# if there is no one in the list winner
                            winner.append((player, points))
            else:
                winner = [(self.winner,0)]
                    
            # announce winner, give him money in pot
            for player in winner:
                player[0].change_money(pot//len(winner))
            # reset pot, choose new button
            self.pot = 0
            self.button += 1

import json
import time
from random import choice
from modules.rules import Rules
from modules.socket_functions import Socket_function


class Game(Rules):
    def __init__(self):
        self.players = []
        self.current_players = []
        self.current_player = 0
        self.round = 1
        self.button = 0
        self.pot = 0
        self.cards = [("Kreuz", 2), ("Kreuz", 3), ("Kreuz", 4), ("Kreuz", 5), ("Kreuz", 6), ("Kreuz", 7),
                      ("Kreuz", 8), ("Kreuz", 9), ("Kreuz", 10), ("Kreuz", 11), ("Kreuz", 12), ("Kreuz", 13),
                      ("Kreuz", 14),
                      ("Karo", 2), ("Karo", 3), ("Karo", 4), ("Karo", 5), ("Karo", 6), ("Karo", 7), ("Karo", 8),
                      ("Karo", 9), ("Karo", 10), ("Karo", 11), ("Karo", 12), ("Karo", 13), ("Karo", 14),
                      ("Herz", 2), ("Herz", 3), ("Herz", 4), ("Herz", 5), ("Herz", 6), ("Herz", 7), ("Herz", 8),
                      ("Herz", 9), ("Herz", 10), ("Herz", 11), ("Herz", 12), ("Herz", 13), ("Herz", 14),
                      ("Piek", 2), ("Piek", 3), ("Piek", 4), ("Piek", 5), ("Piek", 6), ("Piek", 7), ("Piek", 8),
                      ("Piek", 9), ("Piek", 10), ("Piek", 11), ("Piek", 12), ("Piek", 13), ("Piek", 14)]
        self.backup_cards = self.cards[:]
        self.current_bet = 0
        self.community_cards = []
        self.name_list = []
        self.current_list = []
        self.money_list = []
        self.status_list = []
        self.flag = False
        self.set_buttons = True
        self.winner = None
        self.button_list = []
        for p in self.players:
            self.name_list.append(p.name)
            self.money_list.append(p.money)
            self.status_list.append('')

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
                break
            else:
                pos = self.get_next_player(pos)

        self.current_bet = 0
        self.current_player = self.current_players.index(small_blind)
        end = self.current_player
        while True:
            self.current_list[self.players.index(self.current_players[self.current_player])] = True
            self.update()
            action = self.current_players[self.current_player].ask_for_action(self.current_bet)
            if action[0] == 'call':
                index = self.players.index(self.current_players[self.current_player])
                if self.money_list[index] == 0:
                    self.status_list[index] = 'call'
                    self.update()
                    self.set_next_player()
                    if self.current_player == end or len(self.current_players) == 1:
                        break
                    continue
                cb = None
                if self.current_bet + action[1] > self.money_list[index]:
                    action[1] = self.money_list[index]
                    if self.money_list[index] < self.current_bet:
                        cb = self.current_bet
                        self.current_bet = self.money_list[index]

                self.pot += self.current_bet

                self.money_list[index] -= self.current_bet
                # self.current_players[self.current_player].change_money(-self.current_bet)
                if self.current_bet == 0:
                    self.status_list[index] = 'check'
                else:
                    self.status_list[index] = 'call'
                if cb:
                    self.current_bet = cb
                # self.current_players[self.current_player].change_money(-self.current_bet)
            elif action[0] == 'raise':
                index = self.players.index(self.current_players[self.current_player])
                if self.money_list[index] == 0:
                    self.status_list[index] = 'call'
                    self.update()
                    self.set_next_player()
                    if self.current_player == end or len(self.current_players) == 1:
                        break
                    continue
                cb = None
                if self.current_bet + action[1] > self.money_list[index]:
                    action[1] = self.money_list[index]
                    if self.money_list[index] < self.current_bet:
                        cb = self.current_bet
                        self.current_bet = self.money_list[index]
                    else:
                        self.current_bet = self.money_list[index]
                else:
                    self.current_bet += action[1]
                self.pot += self.current_bet
                # self.current_players[self.current_player].change_money(-self.current_bet)

                self.money_list[index] -= self.current_bet
                end = self.current_player
                self.status_list[index] = 'raise ' + str(self.current_bet)
                if cb:
                    self.current_bet = cb
            else:  # elif action[0] == 'fold':
                index = self.players.index(self.current_players[self.current_player])
                self.status_list[index] = 'fold'
                del self.current_players[self.current_player]
                self.current_player -= 1
            self.current_list[self.players.index(self.current_players[self.current_player])] = False
            self.update()
            self.set_next_player()
            # print('player and end', self.current_player, end)
            if self.current_player == end or len(self.current_players) == 1:
                break

        if len(self.current_players) == 1:
            self.winner = self.current_players[0]

    def update(self):
        if not self.flag:
            self.current_list = []
            for i in self.players:
                self.current_list.append(False)
            self.flag = True
        # send each player [name_list, money_list, status_list, pot, table_cards]
        print('update winner',self.winner)
        if self.winner and type(self.winner[0][0]) != str:
            for i,each in enumerate(self.winner):
                new_winner = [each[0].name , each[1]]
                self.winner[i] = new_winner
        self.send_to_all_player('i' + json.dumps(
            [self.name_list, self.money_list, self.status_list, self.current_list, self.pot, self.set_buttons,
             self.button_list,self.winner] ))

    def clear_status(self):
        for i in range(len(self.status_list)):
            if not self.status_list[i] == 'fold':
                self.status_list[i] = ''

    def run(self):
        # set name list, money list, status list
        for player in self.players:
            self.name_list.append(player.name)
            self.money_list.append(player.money)
            self.status_list.append('')

        while True:

            # tell each player to start
            self.send_to_all_player('start')
            # send each player [name_list, money_list, status_list, pot,table_cards, own_money]
            # reset all lists
            self.winner = None
            self.flag = False
            self.update()

            # set button, small and big blind+
            button = self.players[self.button]
            small_blind = self.get_next_player(self.button)
            big_blind = self.get_next_player(self.get_next_player(self.button))
            self.button_list = []
            for i in range(len(self.players)):
                if i == self.button:
                    self.button_list.append('d')
                elif i == small_blind:
                    self.button_list.append('s')
                elif i == big_blind:
                    self.button_list.append('b')
                else:
                    self.button_list.append(None)
            self.set_buttons = 'set'
            # small and big blind pay in the pot+
            # self.players[small_blind].change_money(-25)
            self.money_list[small_blind] -= 25
            self.pot += 25
            # self.players[big_blind].change_money(-50)
            self.money_list[big_blind] -= 50
            self.pot += 50
            self.update()
            # print('small and big blind done')

            # add player to current_player+
            self.current_players = self.players[:]

            # deliever community cards+
            self.cards, self.community_cards = self.get_random_deck(self.cards, 5)
            self.send_to_all_player('b' + json.dumps(self.community_cards))
            # print('cummunity cards send')
            self.update()

            # give each player two cards+
            for player in self.players:
                self.cards, cards = self.get_random_deck(self.cards, 2)
                player.set_cards(cards)
            # print('player cards send')
            self.update()
            # self.set_buttons = False
            # set first player and first round ask for action+

            self.current_player = big_blind
            self.set_next_player()
            end = big_blind
            self.current_bet = 50
            flag1 = False
            while self.current_player != end and len(self.current_players) > 1:
                self.current_list[self.players.index(self.current_players[self.current_player])] = True
                self.update()
                action = self.current_players[self.current_player].ask_for_action_firstround(self.current_bet)
                # (action, action[0])
                if action[0] == 'call':
                    index = self.players.index(self.current_players[self.current_player])
                    if self.money_list[index] == 0:
                        self.status_list[index] = 'call'
                        self.update()
                        self.set_next_player()
                        continue
                    cb = None
                    if self.current_bet + action[1] > self.money_list[index]:
                        action[1] = self.money_list[index]
                        if self.money_list[index] < self.current_bet:
                            cb = self.current_bet
                            self.current_bet = self.money_list[index]

                    if self.current_player == small_blind and not flag1:
                        # self.current_players[self.current_player].change_money(-(self.current_bet-25))
                        self.money_list[index] -= self.current_bet - 25
                        flag1 = True
                        self.pot += self.current_bet - 25
                    else:
                        self.money_list[index] -= self.current_bet
                        # self.current_players[self.current_player].change_money(-self.current_bet)
                        self.pot += self.current_bet
                    self.status_list[index] = 'call'
                    if cb:
                        self.current_bet = cb
                elif action[0] == 'raise':
                    index = self.players.index(self.current_players[self.current_player])
                    if self.money_list[index] == 0:
                        self.status_list[index] = 'call'
                        self.update()
                        self.set_next_player()
                        continue
                    cb = None
                    if self.current_bet + action[1] > self.money_list[index]:
                        action[1] = self.money_list[index]
                        if self.money_list[index] < self.current_bet:
                            cb = self.current_bet
                            self.current_bet = self.money_list[index]
                        else:
                            self.current_bet = self.money_list[index]
                    else:
                        self.current_bet += action[1]
                    self.pot += self.current_bet
                    self.money_list[index] -= self.current_bet
                    end = self.current_player
                    self.status_list[index] = 'raise ' + str(self.current_bet)
                    if cb:
                        self.current_bet = cb
                else:  # elif action[0] == 'fold':
                    index = self.players.index(self.current_players[self.current_player])
                    self.status_list[index] = 'fold'
                    del self.current_players[self.current_player]
                    self.current_player -= 1
                self.current_list[self.players.index(self.current_players[self.current_player])] = False
                print(self.current_players)
                self.update()
                self.set_next_player()
                # print('current player', self.current_player, 'end', end)
            if len(self.current_players) == 1:
                self.winner = self.current_players[0]
            # print('1. round done')

            if not self.winner:
                # reveal 3 cards+
                # print(self.community_cards[:3])
                self.send_to_all_player('f')
                self.update()
                time.sleep(1)
                self.clear_status()
                self.update()

                # second round ask for action+
                self.ask_all_players_for_action()
            # print('2. round done')

            if not self.winner:
                # reveal 1 card+
                # print(self.community_cards[3])
                self.send_to_all_player('g')
                self.update()
                time.sleep(1)
                self.clear_status()
                self.update()
                # third round ask for action+
                self.ask_all_players_for_action()
            # print('3. round done')
            if not self.winner:
                # reveal 1 card+
                # print(self.community_cards[4])
                self.send_to_all_player('h')
                self.update()
                time.sleep(1)
                self.clear_status()
                self.update()
                # fourth round ask for action+
                self.ask_all_players_for_action()
            # print('4. round done')
            if not self.winner:
                winner = []
                for player in self.current_players:
                    winner.append((player, self.get_highest_combi(player.cards, self.community_cards)))
                # print(winner)
                winner.sort(key=lambda x: x[1][2], reverse=True)
                # print(winner)
                max_score = winner[0][1][2]
                # print(max_score)
                zw = []
                for each in winner:
                    if each[1][2] == max_score:
                        zw.append(each)
                self.winner = zw
                winner = self.winner[:]

            else:
                self.winner = [(self.winner, self.get_highest_combi(self.winner.cards, self.community_cards))]
                winner = self.winner[:]

            print('winner',self.winner)
            # print('winner found')
            # announce winner, give him money in pot
            # print('pot:', self.pot)
            time.sleep(1)
            self.clear_status()
            self.update()
            for player in winner:
                print(self.players)
                index = self.players.index(player[0])
                self.money_list[index] += self.pot // len(winner)
                self.status_list[index] = 'win!!'
            for i in range(len(self.players)):
                if self.status_list[i] != 'win!!':
                    self.status_list[i] = ''
            self.set_buttons = 'clear'
            self.update()
            time.sleep(5)
            # reset pot, choose new button
            self.pot = 0
            self.button = self.get_next_player(self.button)
            self.cards = self.backup_cards[:]
            for i in range(len(self.players)):
                self.status_list[i] = ''
                self.money_list[i] += 100
            self.send_to_all_player('a')

            self.update()

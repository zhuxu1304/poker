import socket
import time
from socket_functions import Socket_function
import json
from rules import Rules


class User(Socket_function, Rules):
    def __init__(self, ip):  # create socket with welcome port and then a random port
        print(3)
        self.ip = ip
        # set money,community cards, player cards
        self.money = 1000
        self.community_cards = []
        self.cards = []
        self.ingame = False
        self.revealed_cards = []

    def run(self):

        print('client open')
        s = socket.socket()
        s.connect((self.ip, 5005))
        port = int(self.empfangeStr(s))
        # print(port)
        time.sleep(0.1)
        try:
            self.komm_s = socket.socket()
            self.komm_s.connect((self.ip, port))
        except:
            print('client error')
        print(self.empfangeStr(self.komm_s))
        self.name = input()
        self.sendeStr(self.komm_s, self.name)  # send username
        print("waiting for other players")  # waiting for other players

        while True:
            if self.empfangeStr(self.komm_s) == 'start':  # waiting for signal to start
                self.ingame = True
                print('start')
            time.sleep(0.1)

            # waiting for instruction
            while self.ingame:
                instruction = self.empfangeStr(self.komm_s)
                if instruction[0] == 'a':  # change local money
                    self.money = int(instruction[1:])
                    print('money', self.money)
                    # self.gui.set_own_money(self.money)
                    # self.update()
                elif instruction[0] == 'b':  # set commnunity cards
                    self.community_cards = json.loads(instruction[1:])
                    print(self.community_cards)
                    # self.update()
                elif instruction[0] == 'c':  # set player cards
                    self.cards = json.loads(instruction[1:])
                    print(self.cards)
                    # self.gui.set_player_cards(self.cards)
                    # self.update()
                elif instruction[0] == 'd':  # ask for action first round
                    bet = int(instruction[1:])
                    print('current bet is:', bet)
                    action = input('enter your choice:')
                    action = [action, bet + 10]
                    print(action)
                    if action[0] == 'fold':  # [fold,'']
                        self.ingame = False
                        self.sendeStr(self.komm_s, json.dumps(action))
                    else:  # call or raise, depends on user ['call',bet] or ['raise', value]
                        self.sendeStr(self.komm_s, json.dumps(action))
                    # self.update()
                elif instruction[0] == 'e':  # ask for action
                    bet = int(instruction[1:])
                    print('current bet is:', bet)
                    action = input(
                        'enter your choice:')  # if bet = 0: check, rasie or fold # if bet != 0: call, rasie or fold
                    action = [action, bet + 10]
                    print(action)
                    if action[0] == 'fold':  # [fold,'']
                        self.ingame = False
                        self.sendeStr(self.komm_s, json.dumps(action))
                    else:  # call, check or raise, depends on user ['call',bet] or ['raise', value] or ['check',0]
                        self.sendeStr(self.komm_s, json.dumps(action))
                    # self.update()
                elif instruction[0] == 'f':  # reveal 3 cards
                    print(self.community_cards[:3])
                    self.revealed_cards.append(self.community_cards[:3])
                    # print(self.get_highest_combi(self.revealed_cards,self.cards))
                    # self.gui.set_table_cards(self.revealed_cards)
                elif instruction[0] == 'g':  # reveal 4. card
                    print(self.community_cards[3])
                    self.revealed_cards.append(self.community_cards[3])
                    # print(self.get_highest_combi(self.revealed_cards, self.cards))
                    # self.gui.set_table_cards(self.revealed_cards)
                elif instruction[0] == 'h':  # reveal 5. card
                    print(self.community_cards[4])
                    self.revealed_cards.append(self.community_cards[4])
                    # print(self.get_highest_combi(self.revealed_cards, self.cards))
                    # self.gui.set_table_cards(self.revealed_cards)
                elif instruction[0] == 'i':  # update
                    pass
                    # self.update()
                elif instruction[0] == 'j':  # show winner
                    winner_name = json.loads(instruction[1:])
                    print(winner_name, 'win!')

    def update(self):
        instruction = self.empfangeStr(self.komm_s)
        res = json.loads(instruction[1:])
        name_list, money_list, status_list, pot = res[0], res[1], res[2], res[3]
        self.gui.set_money(money_list)
        self.gui.set_names(name_list)
        self.gui.set_status(status_list)
        self.gui.set_pot_money(pot)


if __name__ == '__main__':
    user = User('192.168.100.7')
    user.run()

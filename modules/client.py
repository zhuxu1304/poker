import socket
import time
from modules.socket_functions import Socket_function
import json
from modules.rules import Rules


class User(Socket_function, Rules):
    def __init__(self, ip, name, queueCG, queueGC):  # create socket with welcome port and then a random port
        self.ip = ip
        # set money,community cards, player cards
        self.money = 1000
        self.community_cards = []
        self.cards = []
        self.ingame = False
        self.revealed_cards = []
        self.name = name
        self.queueCG = queueCG
        self.queueGC = queueGC

    def get_action(self):
        last = None
        while not self.queueGC.empty():
            last = self.queueGC.get()
        return last

    def run(self):

        print('client open')
        s = socket.socket()
        s.connect((self.ip, 55555))
        port = int(self.empfangeStr(s))
        # print(port)
        time.sleep(0.1)
        try:
            self.komm_s = socket.socket()
            self.komm_s.connect((self.ip, port))
        except:
            print('client error')
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
                # if instruction[0] == 'a':  # change local money
                # self.money = int(instruction[1:])
                # print('money', self.money)
                # self.gui.set_own_money(self.money)
                if instruction[0] == 'a':  # init
                    self.revealed_cards = []
                if instruction[0] == 'b':  # set commnunity cards
                    self.community_cards = json.loads(instruction[1:])
                    print(self.community_cards)
                elif instruction[0] == 'c':  # set player cards
                    self.cards = json.loads(instruction[1:])
                    print(self.cards)
                    # self.gui.set_player_cards(self.cards)
                elif instruction[0] == 'd':  # ask for action first round
                    bet = int(instruction[1:])
                    print('current bet is:', bet)
                    while not self.queueGC.empty():  # clear queue
                        self.queueGC.get()
                    action = None
                    while not action:
                        action = self.get_action()
                        time.sleep(0.1)
                    print('action is', action)
                    if  action[0] == 'call':
                        action[1] += bet
                    print(action)
                    if action[0] == 'raise':
                        pass
                    if action[0] == 'fold':  # [fold,'']
                        # self.ingame = False
                        self.sendeStr(self.komm_s, json.dumps(action))
                    else:  # call or raise, depends on user ['call',bet] or ['raise', value]
                        self.sendeStr(self.komm_s, json.dumps(action))
                elif instruction[0] == 'e':  # ask for action
                    bet = int(instruction[1:])
                    print('current bet is:', bet)
                    while not self.queueGC.empty():  # clear queue
                        self.queueGC.get()
                    action = None
                    while not action:
                        action = self.get_action()
                        time.sleep(0.1)
                    print('action is', action)
                    if action[0] == 'fold':  # [fold,'']
                        # self.ingame = False
                        self.sendeStr(self.komm_s, json.dumps(action))
                    else:  # call, check or raise, depends on user ['call',bet] or ['raise', value] or ['check',0]
                        self.sendeStr(self.komm_s, json.dumps(action))
                elif instruction[0] == 'f':  # reveal 3 cards
                    print(self.community_cards[:3])
                    self.revealed_cards = self.community_cards[:3]
                    # print(self.get_highest_combi(self.revealed_cards,self.cards))
                    # self.gui.set_table_cards(self.revealed_cards)
                elif instruction[0] == 'g':  # reveal 4. card
                    print(self.community_cards[3])
                    self.revealed_cards = self.community_cards[:4]
                    # print(self.get_highest_combi(self.revealed_cards, self.cards))
                    # self.gui.set_table_cards(self.revealed_cards)
                elif instruction[0] == 'h':  # reveal 5. card
                    print(self.community_cards[4])
                    self.revealed_cards = self.community_cards
                    # print(self.get_highest_combi(self.revealed_cards, self.cards))
                    # self.gui.set_table_cards(self.revealed_cards)
                elif instruction[0] == 'i':  # update
                    self.update(instruction[1:])
                elif instruction[0] == 'j':  # show winner
                    winner_name = json.loads(instruction[1:])
                    print(winner_name, 'win!')

    def update(self, ins):  # [name_list, money_list, status_list, pot, table_cards, player_cards]
        res = json.loads(ins)
        res.append(self.revealed_cards)
        res.append(self.cards)
        self.queueCG.put(res)
        print('put in CG: ', res)
        # name_list, money_list, status_list, pot = res[0], res[1], res[2], res[3]
        # self.gui.set_money(money_list)
        # self.gui.set_names(name_list)
        # self.gui.set_status(status_list)
        # self.gui.set_pot_money(pot)

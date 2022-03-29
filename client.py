import socket
import time
from socket_functions import Socket_function
import json


class User(Socket_function, Rules):
    def __init__(self):  # create socket with welcome port and then a random port
        s = socket.socket()
        s.connect(('127.0.0.1', 5005))
        port = int(self.empfangeStr(s))
        print(port)
        time.sleep(0.1)
        self.komm_s = socket.socket()
        self.komm_s.connect(('192.168.100.7', port))
        print(self.empfangeStr(self.komm_s))
        self.name = input()
        self.sendeStr(self.komm_s, self.name)  # send username
        print("waiting for other players")  # waiting for other players
        # set money,community cards, player cards
        self.money = 1000
        self.community_cards = []
        self.cards = []
        self.ingame = False
        self.run()

    def run(self):

        while True:
            if self.empfangeStr(self.komm_s) == 'start':  # waiting for signal to start
                self.ingame = True
                break
            time.sleep(0.1)

            # waiting for instruction
            while self.ingame:
                instruction = self.empfangeStr(self.komm_s)
                if instruction[0] == '0':  # change local money
                    self.money = int(instruction[1:])
                    self.update()
                elif instruction[0] == '1':  # set commnunity cards
                    self.community_cards = json.loads(instruction[1:])
                    self.update()
                elif instruction[0] == '2':  # set player cards
                    self.cards = json.loads(instruction[1:])
                    self.update()
                elif instruction[0] == '3':  # ask for action first round
                    bet = int(instruction[1:])
                    print('current bet is:', bet)
                    action = input('enter your choice:')
                    if not action:  # [fold,'']
                        self.ingame = False
                        self.sendeStr(json.dumps(action))
                    else:  # call or raise, depends on user ['call',bet] or ['raise', value]
                        self.sendeStr(json.dumps(action))
                elif instruction[0] == '4': # ask for action
                    bet = int(instruction[1:])
                    print('current bet is:', bet)
                    action = input('enter your choice:')# if bet = 0: check, rasie or fold # if bet != 0: call, rasie or fold
                    if not action:  # [fold,'']
                        self.ingame = False
                        self.sendeStr(json.dumps(action))
                    else:  # call, check or raise, depends on user ['call',bet] or ['raise', value] or ['check',0]
                        self.sendeStr(json.dumps(action))
                elif instruction[0] == '5': # reveal 3 cards
                    print(self.community_cards[:2])


    def update(self):
        pass


user = User()

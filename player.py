from socket_functions import Socket_function
import socket
import json


class Player(Socket_function):
    def __init__(self, port):  # create socket, get username, wait till 5 players, set amount of money
        self.money = 1000
        self.cards = []
        self.bind(port)

    def bind(self, port):
        self.s = socket.socket()
        self.s.bind((socket.gethostname(), port))
        self.port = port
        self.s.listen(1)
        self.komm_s, self.adress = self.s.accept()
        self.name = self.empfangeStr(self.komm_s)
        # self.sendeStr(self.komm_s, "waiting for other players")

        print(self.name)

    def set_cards(self, cards):
        self.cards = cards
        self.send('c' + json.dumps(self.cards))

    def run(self):
        print(self.name, self.empfangeStr(self.komm_s))

    def send(self, message):
        self.sendeStr(self.komm_s, str(message))

    def get(self):
        return self.empfangeStr(self.komm_s)

    def get_money(self):
        return self.money

    def change_money(self, amount):
        self.money += amount
        self.send('a' + str(self.get_money()))
        print('money changed')

    def ask_for_action(self, bet):
        self.send('e' + str(bet))
        # time.sleep(5)
        action = json.loads(self.get())
        return action

    def ask_for_action_firstround(self, bet):  # get a list object via json,return a list object [operation,value]
        self.send('d' + str(bet))
        # time.sleep(5)
        action = json.loads(self.get())
        return action

from socket_functions import Socket_function
import socket
import json

class Player(Socket_function):
    def __init__(self, port):  # create socket, get username, wait till 5 players, set amount of money

        self.s = socket.socket()
        self.s.bind((socket.gethostname(), port))
        self.port = port
        self.s.listen(1)
        self.komm_s, self.adress = self.s.accept()
        self.sendeStr(self.komm_s, "what's your name?")
        self.name = self.empfangeStr(self.komm_s)
        # self.sendeStr(self.komm_s, "waiting for other players")

        self.money = 1000
        self.cards = []
        print(self.name)

    def set_cards(self,cards):
        self.cards = cards
        self.send('2'+json.dumps(self.cards))
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
        self.send('0'+str(self.get_money))

    def ask_for_action(self):
        self.send('4')
        action = self.get()
        if action == 'fold':
            pass
        elif action == 'raise':
            pass
        elif action == 'call':
            pass
        elif action == 'check':
            pass
        elif action == 'bet':
            pass

    def ask_for_action_firstround(self):
        self.send('3')
        action = self.get()
        if action == 'fold':
            pass
        elif action == 'raise':
            pass
        elif action == 'call':
            pass

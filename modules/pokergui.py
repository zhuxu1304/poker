import sys
import threading
from tkinter import *
import socket
from PIL import Image, ImageTk
# from random_deck import *
from time import sleep
from modules.server import Server
from threading import Thread
from modules.client import User
from multiprocessing import Process, Queue
import time
from modules.socket_functions import *


class Poker_Gui(Socket_function):

    def __init__(self):
        cards = [("Kreuz", 2), ("Kreuz", 3), ("Kreuz", 4), ("Kreuz", 5), ("Kreuz", 6), ("Kreuz", 7),
                 ("Kreuz", 8)]
        self.status_list = ["Call", "Raise", "Check", "Call", "Raise", "Check"]
        self.card_list_table = cards[:5]
        self.card_list_player = cards[5:7]
        self.money_labels = []
        self.name_labels = []
        self.status_labels = []
        self.player_cards = []
        self.table_cards = []
        self.own_money = 0
        self.player_name = ""
        self.numb_players = 0
        self.ip_adress_server = ""
        self.queueCG = Queue()
        self.queueGC = Queue()
        self.server = None
        self.client = None
        self.main_menu()

    def set_buttons(self, gamewindow, flag, pos_list):  # [dealer,small blind, big blind]
        print('setting...',flag,pos_list)
        if flag == 'set':

            for i, each in enumerate(pos_list):
                if not each:
                    continue
                if each == 'b':
                    print('big blind')
                    image = ImageTk.PhotoImage(file='images/big_blind.png')
                elif each == 's':
                    print('small blind')
                    image = ImageTk.PhotoImage(file='images/small_blind.png')
                else:
                    print('dealer')
                    image = ImageTk.PhotoImage(file='images/dealer_button.png')
                self.player_buttons_list[i].create_image(1.5, 1.5, image=image, anchor='nw')
                self.player_buttons_list[i].image = image
        elif flag == 'clear':
            print('cleaning...')
            for i, each in enumerate(pos_list):
                self.player_buttons_list[i].delete('all')

    def set_money(self, money_list):
        for i, label in enumerate(self.money_labels):
            label['text'] = str(money_list[i]) + "$"

    def set_names(self, name_list):
        for i, label in enumerate(self.name_labels):
            label['text'] = name_list[i]

    def set_status(self, status_list):
        for i, label in enumerate(self.status_labels):
            label['text'] = status_list[i]

    def set_pot_money(self, pot_money):
        self.pot_money['text'] = "Pot Money: " + str(pot_money) + "$"

    def set_own_money(self, own_money):
        self.own_money = own_money
        self.Money_label['text'] = "Your current money:\n" + str(own_money) + "$"

    def set_player_cards(self, card_list, game_window):
        if card_list:
            card_images_player = []
            for card in card_list:
                card = tuple(card)
                card_images_player.append(
                    ImageTk.PhotoImage(Image.open("cards/" + str(card) + ".png").resize((80, 100), Image.ANTIALIAS)))

            for i, element in enumerate(self.player_cards):
                element.configure(image=card_images_player[i])
                element.image = card_images_player[i]

    def set_current(self, current_list):
        for i, each in enumerate(current_list):
            if each:
                player_image = PhotoImage(file="images/player1_your_turn.png")
            else:
                player_image = PhotoImage(file="images/player1.png")
            self.label_list[i].configure(image=player_image)
            self.label_list[i].image = player_image

    def set_table_cards(self, card_list, game_window):
        if card_list:
            card_images_table = []
            for card in card_list:
                card = tuple(card)
                card_images_table.append(
                    ImageTk.PhotoImage(Image.open("cards/" + str(card) + ".png").resize((120, 180), Image.ANTIALIAS)))

            for i, element in enumerate(card_images_table):
                self.table_cards[i].configure(image=element)
                self.table_cards[i].image = element
        else:
            card_images_table = []
            for card in range(5):
                card_images_table.append(
                    ImageTk.PhotoImage(Image.open("cards/back.png").resize((120, 180), Image.ANTIALIAS)))

            for i, element in enumerate(card_images_table):
                self.table_cards[i].configure(image=element)
                self.table_cards[i].image = element

    def set_player_input(self):
        self.player_name = self.user_input.get()
        self.numb_players = self.var.get()
        self.ip_adress_server = socket.gethostbyname(socket.gethostname())

    def set_input_join(self):
        self.player_name = self.user_name.get()
        self.ip_adress_server = self.input_ip.get()

    def set_client(self, ip):
        komm_s = socket.socket()
        komm_s.connect((ip, 55556))
        self.player_number = int(self.empfangeStr(komm_s))  # should ask server how many players
        self.side = 'client'

    def set_server(self):
        self.side = 'server'

    def open_host_window(self):

        host_window = Tk()

        host_window.geometry('600x597')

        host_window.title("Coffee-Poker - Host a Game")

        background_image = PhotoImage(file="images/welcome_background1.png")
        background_label = Label(host_window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        heading = Label(host_window, text="Welcome to Coffee-Poker", font="Arial 30 bold underline", foreground="white",
                        bg="#303030")

        heading.place(relx=0.5, rely=0.07, anchor=CENTER)

        Label_server_ip = Label(host_window, text="Your IP is:\n" + socket.gethostbyname(socket.gethostname()),
                                font="Arial 25 bold", foreground="white", bg="#303030")
        Label_server_ip.place(relx=0.5, rely=0.2, anchor=CENTER)

        Label_name = Label(host_window, text="Enter Name:", font="Arial 20 bold", foreground="white", bg="#303030")
        Label_name.place(relx=0.5, rely=0.35, anchor=CENTER)

        # Input Name
        self.user_input = StringVar()
        self.input_name = Entry(host_window, font="Arial 20", justify=CENTER, textvariable=self.user_input)
        self.input_name.place(relx=0.5, rely=0.45, anchor=CENTER)

        Label_player = Label(host_window, text="Enter number of players:", font="Arial 20 bold", foreground="white",
                             bg="#303030")
        Label_player.place(relx=0.5, rely=0.55, anchor=CENTER)

        # Select player number
        option_list = [2, 3, 4, 5, 6]

        self.var = StringVar(host_window)
        self.var.set(option_list[0])

        input_player = OptionMenu(host_window, self.var, *option_list)
        input_player.config(width=10, font=("Arial", 20), relief="solid")
        input_player.place(relx=0.5, rely=0.65, anchor=CENTER)

        connect_button = Button(host_window, text="Run", font="Arial 20",
                                command=lambda: [self.set_player_input(), self.set_server(), host_window.destroy(),
                                                 self.open_game_window(int(self.var.get()))])
        connect_button.place(relx=0.5, rely=0.8, anchor=CENTER)

        Back_button = Button(host_window, text="Back", font="Arial 20",
                             command=lambda: [host_window.destroy(), self.main_menu()])
        Back_button.place(relx=0.5, rely=0.9, anchor=CENTER)

        host_window.mainloop()

    def open_join_window(self):

        join_window = Tk()

        join_window.geometry('600x597')

        join_window.title("Coffee-Poker - Join a Game")

        background_image = PhotoImage(file="images/welcome_background1.png")
        background_label = Label(join_window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        heading = Label(join_window, text="Welcome to Coffee-Poker", font="Arial 30 bold underline", foreground="white",
                        bg="#303030")

        heading.place(relx=0.5, rely=0.07, anchor=CENTER)

        Label_server_ip = Label(join_window, text="Enter Host IP:", font="Arial 20 bold", foreground="white",
                                bg="#303030")
        Label_server_ip.place(relx=0.5, rely=0.25, anchor=CENTER)

        self.input_ip = StringVar()
        input_server_ip = Entry(join_window, font="Arial 20", justify=CENTER, textvariable=self.input_ip)
        input_server_ip.place(relx=0.5, rely=0.35, anchor=CENTER)

        Label_name = Label(join_window, text="Enter Name:", font="Arial 20 bold", foreground="white", bg="#303030")
        Label_name.place(relx=0.5, rely=0.45, anchor=CENTER)

        self.user_name = StringVar()
        self.input_name = Entry(join_window, font="Arial 20", justify=CENTER, textvariable=self.user_name)
        self.input_name.place(relx=0.5, rely=0.55, anchor=CENTER)

        connect_button = Button(join_window, text="Connect", font="Arial 20",
                                command=lambda: [self.set_input_join(), self.set_client(self.ip_adress_server),
                                                 join_window.destroy(),
                                                 self.open_game_window(self.player_number)])
        connect_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        Back_button = Button(join_window, text="Back", font="Arial 20",
                             command=lambda: [join_window.destroy(), self.main_menu()])
        Back_button.place(relx=0.5, rely=0.85, anchor=CENTER)

        join_window.mainloop()

    def update(self, game_window):  # [name_list, money_list, status_list, pot, table_cards, player_cards]
        self.index = None
        self.flag = True
        while self.flag:
            last = None
            while not self.queueCG.empty():
                last = self.queueCG.get()
                print('got', last)
            if last:
                name_list, money_list, status_list, current_list, pot, op, button_list, table_cards, player_cards = \
                    last[0], last[1], last[2], last[3], \
                    last[4], last[5], last[6], last[7], last[8]
                if not self.index:
                    self.index = name_list.index(self.player_name)
                    time.sleep(0.1)

                self.set_current(current_list[self.index:] + current_list[:self.index])
                self.set_names(name_list[self.index:] + name_list[:self.index])
                self.set_money(money_list[self.index:] + money_list[:self.index])
                self.set_status(status_list[self.index:] + status_list[:self.index])
                self.set_pot_money(pot)
                self.set_own_money(money_list[self.index])
                self.set_table_cards(table_cards, game_window)
                self.set_player_cards(player_cards, game_window)
                self.set_buttons(game_window, op, button_list[self.index:] + button_list[:self.index])
            time.sleep(0.1)

    def wrap_update(self, game_window):
        t = threading.Thread(target=self.update, args=(game_window,))
        t.start()

    # Main Window for Poker Game
    def open_game_window(self, number_of_players):

        self.client = User(self.ip_adress_server, self.player_name, self.queueCG, self.queueGC)
        self.process_client = Process(target=self.client.run)
        if self.side == 'server':
            self.server = Server(int(self.numb_players))
            self.process_server = Process(target=self.server.run)
            self.process_server.start()
        self.process_client.start()

        game_window = Tk()
        self.wrap_update(game_window)

        game_window.geometry('1200x720')

        game_window.title("Coffee-Poker - Game")

        # Background
        background_image = ImageTk.PhotoImage(Image.open("images/pokertisch1.png"))
        background_label = Label(game_window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Placing Player icons
        # player_coords = [(43,500),(43,5),(1040,500),(1040,20),(540,0),(540,520)]
        player_coords = [(500, 520), (500, 0), (23, 20), (970, 20), (23, 500), (970, 500)]
        player_image = PhotoImage(file="images/player1.png")
        self.label_list = []
        for i in range(0, number_of_players):
            player_label = Label(game_window, image=player_image, bg="white")
            player_label.place(x=player_coords[i][0], y=player_coords[i][1])
            self.label_list.append(player_label)

        # Placing Money Labels
        money_coords = [(650, 555), (650, 35), (175, 55), (1120, 55), (175, 535), (1120, 535)]
        for i in range(0, number_of_players):
            money_label = Label(game_window, text="0$", bg="white", font="Arial 11 bold")
            money_label.place(x=money_coords[i][0], y=money_coords[i][1], anchor=CENTER)
            self.money_labels.append(money_label)

        # Placing Name Labels
        name_coords = [(655, 580), (655, 60), (180, 80), (1125, 80), (175, 560), (1125, 560)]
        for i in range(0, number_of_players):
            player_label = Label(game_window, text="", bg="white", font="Arial 11 bold")
            player_label.place(x=name_coords[i][0], y=name_coords[i][1], anchor=CENTER)
            self.name_labels.append(player_label)

        # Placing Status Labels

        status_coords = [(630, 590), (625, 70), (150, 90), (1100, 90), (145, 570), (1090, 570)]
        for i in range(0, number_of_players):
            status_label = Label(game_window, text="", bg="white", font="Arial 11 bold")
            status_label.place(x=status_coords[i][0], y=status_coords[i][1])
            self.status_labels.append(status_label)
        # Placing table cards

        card_images = []
        for card in self.card_list_table:
            card_images.append(ImageTk.PhotoImage(Image.open("cards/back.png").resize((120, 180), Image.ANTIALIAS)))
        card_coords = [(340, 320), (470, 320), (600, 320), (730, 320), (860, 320)]
        for i, card in enumerate(self.card_list_table):
            # card_image = ImageTk.PhotoImage(Image.open("cards/"+str(card)+".png").resize((120,180), Image.ANTIALIAS))
            card_label = Label(game_window, image=card_images[i], bg="white")
            card_label.place(x=card_coords[i][0], y=card_coords[i][1], anchor=CENTER)
            self.table_cards.append(card_label)

        # Placing player cards
        card_images_player = []
        for card in range(0, 2):
            card_images_player.append(
                ImageTk.PhotoImage(Image.open("cards/back.png").resize((80, 100), Image.ANTIALIAS)))
        card_coords_player = [(50, 60), (140, 60)]

        frame_cards = Frame(game_window, bg="#303030")
        frame_cards.place(x=300, y=520, width=190, height=120)

        for i in range(0, 2):
            card_label = Label(frame_cards, image=card_images_player[i], bg="white")
            card_label.place(x=card_coords_player[i][0], y=card_coords_player[i][1], anchor=CENTER)
            self.player_cards.append(card_label)

        # Button for Call, Raise, Check, Fold, Quit
        # Quit
        Quit_Button = Button(game_window, text="Quit", font="Arial 20",
                             command=lambda: [self.on_closing(game_window), self.main_menu()])
        Quit_Button.place(relx=0.05, rely=0.95, anchor=CENTER, height=55)

        def check_call():
            self.queueGC.put(['call', 0])

        # Check/Call
        Check_Button = Button(game_window, text="Check\nCall", font="Arial 15", command=check_call)
        Check_Button.place(relx=0.95, rely=0.95, anchor=CENTER, width=100, height=55)

        # Money
        self.Money_label = Label(game_window, text="Your current money:\n0$", font="Arial 20", foreground="white",
                                 bg="#393939")
        self.Money_label.place(relx=0.5, rely=0.94, anchor=CENTER)

        # Raise
        def save(value, button):
            self.queueGC.put(['raise', value])
            button['command'] = raise_fct
            raise_fct()

        def raise_fct():
            if Raise_Button['text'] == 'Raise':
                global Raise_slider
                Raise_slider = Scale(game_window, from_=self.own_money, to=1, relief="solid", font="Arial 20")
                Raise_slider.place(relx=0.85, rely=0.84, anchor=CENTER, width=100)
                Raise_Button['text'] = "Okay"
                Raise_Button['command'] = lambda: save(Raise_slider.get(), Raise_Button)

            else:
                Raise_slider.destroy()
                Raise_Button["text"] = 'Raise'

        Raise_Button = Button(game_window, text="Raise", font="Arial 20", command=raise_fct)
        Raise_Button.place(relx=0.85, rely=0.95, anchor=CENTER, width=100, height=55)

        def fold():
            self.queueGC.put(['fold', 0])

        # Checkd
        Fold_Button = Button(game_window, text="Fold", font="Arial 20", command=fold)
        Fold_Button.place(relx=0.75, rely=0.95, anchor=CENTER, width=100, height=55)

        # Pot Money
        self.pot_money = Label(game_window, text="Pot Money: 0$", font="Arial 20", foreground="white", bg="#393939")
        self.pot_money.place(relx=0.5, rely=0.65, anchor=CENTER)

        # Dealer Buttons
        ##        button_coords = [(500+220, 520+30), (500+220, 0+30), (23+220, 20+30), (970-45, 20+30), (23+220, 500+30), (970-45, 500+30)]
        ##        for i in range(len(button_coords)):
        ##            dealer_image = ImageTk.PhotoImage(file='dealer_button.png')
        ##            dealer_label = Canvas(width=50, height=50,bg = 'yellow')
        ##            dealer_label.place(x=button_coords[i][0],y = button_coords[i][1])
        ##            dealer_label.create_image(1.5, 1.5, image=dealer_image, anchor='nw')

        # Mainloop2
        # print(self.user_name.get())
        # place buttons
        button_coords = [(500 + 220, 520 + 30), (500 + 220, 0 + 30), (23 + 220, 20 + 30), (970 - 45, 20 + 30),
                         (23 + 220, 500 + 30), (970 - 45, 500 + 30)]
        self.player_buttons_list = []
        for i in range(0, number_of_players):
            label = Canvas(game_window, width=50, height=50, bg='white')
            label.place(x=button_coords[i][0], y=button_coords[i][1])
            self.player_buttons_list.append(label)

        game_window.protocol("WM_DELETE_WINDOW", func=lambda: self.on_closing(game_window))
        game_window.mainloop()

    def on_closing(self, game_window):
        if self.server:
            self.process_server.terminate()
            del self.server
        self.process_client.terminate()
        del self.client
        self.flag = False
        game_window.destroy()

    # To DO
    # small blind, big blind, dealer Button
    # menu select start money automatic adapt small/big blind
    # winner of the round screen
    # (half done) update function for player connected and money etc.
    # Class -> finish setter methodes

    def main_menu(self):
        welcome_window = Tk()

        welcome_window.geometry('600x397')

        welcome_window.title("Coffee-Poker")

        background_image = PhotoImage(file="images/welcome_background1.png")
        background_label = Label(welcome_window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        heading = Label(welcome_window, text="Welcome to Coffee-Poker", font="Arial 30 bold underline",
                        foreground="white", bg="#303030")

        heading.place(relx=0.5, rely=0.1, anchor=CENTER)

        join_button = Button(welcome_window, text="Join a Game", font="Arial 20",
                             command=lambda: [welcome_window.destroy(), self.open_join_window()])

        join_button.place(relx=0.5, rely=0.4, anchor=CENTER, width=250)

        Host_button = Button(welcome_window, text="Host a Game", font="Arial 20",
                             command=lambda: [welcome_window.destroy(), self.open_host_window()])

        Host_button.place(relx=0.5, rely=0.7, anchor=CENTER, width=250)

        welcome_window.mainloop()


if __name__ == '__main__':
    gui = Poker_Gui()

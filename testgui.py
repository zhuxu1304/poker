from tkinter import *

t = Tk()
t.geometry('777x997')

background_image = PhotoImage(file="//MNSplusFile/kleinmor04$/Eigene Dateien/Poker/welcome_background1.png")

background_label = Label(t, image=background_image)

background_label.place(x=0,y=0,relwidth=1, relheight=1)

t.mainloop()

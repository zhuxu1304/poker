class Card():
    def __init__(self,data):
        self.color = data[0]
        self.number = data[1]
        self.back = None
        self.front = None

    def get_color(self):
        return self.color

    def get_number(self):
        return self.number

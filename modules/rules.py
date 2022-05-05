from random import choice


class Rules():
    def get_random_deck(self, cards, size):
        random_deck = []
        for i in range(size):
            random_card = choice(cards)
            cards.remove(random_card)
            random_deck.append(random_card)
        return cards, random_deck

    def sort_cards(self, cards):
        cards.sort(key=lambda x: x[1], reverse=True)
        return cards
    
    def remove_double_values(self, random_deck):
        last = ""
        without_doubles = []
        for element in random_deck:
            if element[1] != last:
                without_doubles.append(element)
                last = element[1]
            else:
                last = element[1]
        return without_doubles

    def check_for_straight(self, random_deck):
        is_straight = False
        found = []
        i=0
        t=1
        random_deck = self.remove_double_values(random_deck)
        while len(random_deck[i:])>4 and t < 5:
            last=random_deck[i]
            t=1
            for element in random_deck[i:i+5]:
                if element[1]+1 == last:
                    t+=1
                    last = element[1]
                else:
                    last = element[1]

            if t >= 5:
                is_straight = True
                found = random_deck[i:i+5]
            else:
                i+=1

        return is_straight,found

    # Check for flush

    def check_for_flush(self, random_deck,all=False):
        is_flush = False
        found = []
        Kreuz = [item for item in random_deck if item[0] == "Kreuz"]
        Piek = [item for item in random_deck if item[0] == "Piek"]
        Herz = [item for item in random_deck if item[0] == "Herz"]
        Karo = [item for item in random_deck if item[0] == "Karo"]
        if len(Herz) >= 5:
            is_flush = True
            found = Herz
        elif len(Piek) >= 5:
            is_flush = True
            found = Piek
        elif len(Kreuz) >= 5:
            is_flush = True
            found = Kreuz
        elif len(Karo) >= 5:
            is_flush = True
            found = Karo
        if not all:
            found = found[:5]

        return is_flush, found

    # Check for Royal Flush

    def check_for_royal_flush(self, random_deck):
        is_royal_flush = False
        found = []

        straight_flush = self.check_for_straight_flush(random_deck)

        #print(straight_flush)

        if straight_flush[0] and straight_flush[1][0][1] == 14:
            is_royal_flush = True
            found = straight_flush[1]

        return is_royal_flush, found

    # Check for Two Pair

    def check_for_two_pair(self, random_deck):
        is_two_pair = False
        found = []
        if len(self.check_for_one_pair(random_deck)[1]) >= 4:
            is_two_pair = True
            found = self.check_for_one_pair(random_deck)[1]
            self.sort_cards(found)
        return is_two_pair, found[:4]

    # Check for one Pair

    def check_for_one_pair(self, random_deck):
        is_one_pair = False
        pairs_found = []
        values = [item[1] for item in random_deck]
        for i in range(2, 15):
            if values.count(i) >= 2:
                for item in random_deck:
                    if item[1] == i:
                        pairs_found.append(item)
                is_one_pair = True
        return is_one_pair, pairs_found

    # Check for three of a kind

    def check_for_three_of_a_kind(self, random_deck):
        is_three_of_a_kind = False
        triple_found = []
        values = [item[1] for item in random_deck]
        for i in range(14, 1, -1):
            if values.count(i) == 3:
                for item in random_deck:
                    if item[1] == i:
                        triple_found.append(item)
                is_three_of_a_kind = True
                break
        return is_three_of_a_kind, triple_found

    # Check for Straight Flush

    def check_for_straight_flush(self, random_deck):
        is_straight_flush = False
        found = []
        
        flush = self.check_for_flush(random_deck,True)[1]
        is_straight_flush = self.check_for_straight(flush)[0]

        if is_straight_flush:
            found = self.check_for_straight(flush)[1]

        return is_straight_flush, found[:5]

    # Check fot Fullhouse

    def check_for_fullhouse(self, random_deck):
        is_fullhouse = False
        three_of_a_kind = self.check_for_three_of_a_kind(random_deck)
        one_pair = []
        if three_of_a_kind[0]:
            for triple in three_of_a_kind[1]:
                random_deck.remove(triple)
            if self.check_for_one_pair(random_deck)[0]:
                one_pair = self.check_for_one_pair(random_deck)[1][:2]
                is_fullhouse = True
            for triple in three_of_a_kind[1]:
                random_deck.append(triple)
                self.sort_cards(random_deck)
            for double in one_pair:
                three_of_a_kind[1].append(double)
                # sort_cards(three_of_a_kind[1])
        return is_fullhouse, three_of_a_kind[1]

    # Check fot a Four of a Kind

    def check_for_four_of_a_kind(self, random_deck):
        is_three_of_a_kind = False
        triple_found = []
        values = [item[1] for item in random_deck]
        for i in range(14, 1, -1):
            if values.count(i) == 4:
                for item in random_deck:
                    if item[1] == i:
                        triple_found.append(item)
                is_three_of_a_kind = True

        return is_three_of_a_kind, triple_found

    # Check for highest Card

    def check_for_highcard(self, random_deck):
        return True, random_deck[0]

    def get_highest_combi(self, player_deck, table_deck):
        random_deck = player_deck + table_deck
        ##        print()
        ##        print("Zufälliges Karten:", random_deck)
        ##        print("Karten sortiert anhand ihrem Wert:", sort_cards(random_deck))
        random_deck = self.sort_cards(random_deck)
        player_deck = self.sort_cards(player_deck)

        if self.check_for_royal_flush(random_deck)[0]:
            res = self.check_for_royal_flush(random_deck)[1]
            return ("Royal Flush", res, 10 + res[0][1] / 100)
            ## print("Your highest combination is a Royal Flush:", random_deck[:5])

        elif self.check_for_straight_flush(random_deck)[0]:
            res = self.check_for_straight_flush(random_deck)[1]
            return ("Straight Flush", res, 9 + res[0][1] / 100)
            ## print("Your highest combination is a Straight Flush:", check_for_straight_flush(random_deck)[1])

        elif self.check_for_four_of_a_kind(random_deck)[0]:
            res = self.check_for_four_of_a_kind(random_deck)[1]
            return ('Four of a Kind', res, 8 + res[0][1] / 100)
            ## print("Your highest combination is a Four of a Kind:", check_for_four_of_a_kind(random_deck)[1])

        elif self.check_for_fullhouse(random_deck)[0]:
            res = self.check_for_fullhouse(random_deck)[1]
            return ('Fullhouse', res, 7 + res[0][1] / 100)
            ## print("Your highest combination is a Fullhouse:", check_for_fullhouse(random_deck)[1])

        elif self.check_for_flush(random_deck)[0]:
            res = self.check_for_flush(random_deck)[1]
            return ('Flush', res, 6 + res[0][1] / 100)
            ## print("Your highest combination is a Flush:", check_for_flush(random_deck)[1])

        elif self.check_for_straight(random_deck)[0]:
            res = self.check_for_straight(random_deck)[1]
            return ('Straight', res, 5 + res[0][1] / 100)
            ## print("Your highest combination is a Straight:", check_for_straight(random_deck)[1])

        elif self.check_for_three_of_a_kind(random_deck)[0]:
            res = self.check_for_three_of_a_kind(random_deck)[1]
            return ('Three of a Kind', res, 4 + res[0][1] / 100)
            ## print("Your highest combination is a Three of a Kind:", check_for_three_of_a_kind(random_deck)[1])

        elif self.check_for_two_pair(random_deck)[0]:
            res = self.check_for_two_pair(random_deck)[1]
            return ('Two Pair', res, 3 + res[0][1] / 100)
            ## print("Your highest combination is a Two Pair:", check_for_two_pair(random_deck)[1])

        elif self.check_for_one_pair(random_deck)[0]:
            res = self.check_for_one_pair(random_deck)[1]
            return ('One Pair', res, 2 + res[0][1] / 100)
            ## print("Your highest combination is a One Pair:", check_for_one_pair(random_deck)[1])

        else:
            res = self.check_for_highcard(player_deck)[1]
            return ('High Card', [res], 1 + res[1] / 100)
            ## print("Your highest card is:", check_for_highcard(random_deck))


if __name__ == '__main__':
    #for i in range(10000):
    r = Rules()
    cards = [("Kreuz", 2), ("Kreuz", 3), ("Kreuz", 4), ("Kreuz", 5), ("Kreuz", 6), ("Kreuz", 7),
                 ("Kreuz", 8), ("Kreuz", 9), ("Kreuz", 10), ("Kreuz", 11), ("Kreuz", 12), ("Kreuz", 13),
                 ("Kreuz", 14),
                 ("Karo", 2), ("Karo", 3), ("Karo", 4), ("Karo", 5), ("Karo", 6), ("Karo", 7), ("Karo", 8),
                 ("Karo", 9), ("Karo", 10), ("Karo", 11), ("Karo", 12), ("Karo", 13), ("Karo", 14),
                 ("Herz", 2), ("Herz", 3), ("Herz", 4), ("Herz", 5), ("Herz", 6), ("Herz", 7), ("Herz", 8),
                 ("Herz", 9), ("Herz", 10), ("Herz", 11), ("Herz", 12), ("Herz", 13), ("Herz", 14),
                 ("Piek", 2), ("Piek", 3), ("Piek", 4), ("Piek", 5), ("Piek", 6), ("Piek", 7), ("Piek", 8),
                 ("Piek", 9), ("Piek", 10), ("Piek", 11), ("Piek", 12), ("Piek", 13), ("Piek", 14)]
    #random_deck = r.get_random_deck(cards, 7)[1]
    random_deck = [("Herz",14),("Herz",10),("Herz",7),("Herz",7),("Herz",7),("Herz",6),("Herz",5)]
    print("Zufälliges Karten:", random_deck)
    print("Karten sortiert anhand ihrem Wert:", r.sort_cards(random_deck))
    #print(r.check_for_straight(random_deck))
    print(r.get_highest_combi(random_deck, []))

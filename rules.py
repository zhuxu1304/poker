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

    def check_for_straight(self, random_deck):
        is_straight = False
        found = []
        if random_deck[0][1] == random_deck[1][1] + 1 and random_deck[1][1] == random_deck[2][1] + 1 and random_deck[2][
            1] == random_deck[3][1] + 1 and random_deck[3][1] == random_deck[4][1] + 1:
            is_straight = True
            found = random_deck[:5]
        elif random_deck[1][1] == random_deck[2][1] + 1 and random_deck[2][1] == random_deck[3][1] + 1 and \
                random_deck[3][1] == random_deck[4][1] + 1 and random_deck[4][1] == random_deck[5][1] + 1:
            is_straight = True
            found = random_deck[1:6]
        elif random_deck[2][1] == random_deck[3][1] + 1 and random_deck[3][1] == random_deck[4][1] + 1 and \
                random_deck[4][1] == random_deck[5][1] + 1 and random_deck[5][1] == random_deck[6][1] + 1:
            is_straight = True
            found = random_deck[2:7]
        else:
            is_straight = False

        return is_straight, found

    # Check for flush

    def check_for_flush(self, random_deck):
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

        return is_flush, found

    # Check for Royal Flush

    def check_for_royal_flush(self, random_deck):
        is_royal_flush = False
        if random_deck[0][1] == 14 and random_deck[0][1] == random_deck[1][1] + 1 and random_deck[1][1] == \
                random_deck[2][1] + 1 and random_deck[2][1] == random_deck[3][1] + 1 and random_deck[3][1] == \
                random_deck[4][1] + 1:
            Kreuz = [item for item in random_deck[:5] if item[0] == "Kreuz"]
            Piek = [item for item in random_deck[:5] if item[0] == "Piek"]
            Herz = [item for item in random_deck[:5] if item[0] == "Herz"]
            Karo = [item for item in random_deck[:5] if item[0] == "Karo"]
            if len(Herz) >= 5 or len(Piek) >= 5 or len(Karo) >= 5 or len(Kreuz) >= 5:
                is_royal_flush = True
        return is_royal_flush

    # Check for Two Pair

    def check_for_two_pair(self, random_deck):
        is_two_pair = False
        found = []
        if len(check_for_one_pair(random_deck)[1]) >= 4:
            is_two_pair = True
            found = check_for_one_pair(random_deck)[1]
            sort_cards(found)
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
        if random_deck[0][1] == random_deck[1][1] + 1 and random_deck[1][1] == random_deck[2][1] + 1 and random_deck[2][
            1] == random_deck[3][1] + 1 and random_deck[3][1] == random_deck[4][1] + 1 and \
                check_for_flush(random_deck[:5])[0]:
            is_straight_flush = True
            found = random_deck[:5]
        elif random_deck[1][1] == random_deck[2][1] + 1 and random_deck[2][1] == random_deck[3][1] + 1 and \
                random_deck[3][1] == random_deck[4][1] + 1 and random_deck[4][1] == random_deck[5][1] + 1 and \
                check_for_flush(random_deck[1:6])[0]:
            is_straight_flush = True
            found = random_deck[1:6]
        elif random_deck[2][1] == random_deck[3][1] + 1 and random_deck[3][1] == random_deck[4][1] + 1 and \
                random_deck[4][1] == random_deck[5][1] + 1 and random_deck[5][1] == random_deck[6][1] + 1 and \
                check_for_flush(random_deck[2:7])[0]:
            is_straight_flush = True
            found = random_deck[2:7]
        else:
            is_straight_flush = False

        return is_straight_flush, found

    # Check fot Fullhouse

    def check_for_fullhouse(self, random_deck):
        is_fullhouse = False
        three_of_a_kind = check_for_three_of_a_kind(random_deck)
        one_pair = []
        if three_of_a_kind[0]:
            for triple in three_of_a_kind[1]:
                random_deck.remove(triple)
            if check_for_one_pair(random_deck)[0]:
                one_pair = check_for_one_pair(random_deck)[1][:2]
                is_fullhouse = True
            for triple in three_of_a_kind[1]:
                random_deck.append(triple)
                sort_cards(random_deck)
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
        return random_deck[0]

    def get_highest_combi(self, player_deck, table_deck):
        random_deck = player_deck + table_deck
##        print()
##        print("Zufälliges Karten:", random_deck)
##        print("Karten sortiert anhand ihrem Wert:", sort_cards(random_deck))

        if check_for_royal_flush(random_deck):
            return("Royal Flush", random_deck[:5])
            ## print("Your highest combination is a Royal Flush:", random_deck[:5])

        elif check_for_straight_flush(random_deck)[0]:
            return("Straight Flush", check_for_straight_flush(random_deck)[1])
            ## print("Your highest combination is a Straight Flush:", check_for_straight_flush(random_deck)[1])

        elif check_for_four_of_a_kind(random_deck)[0]:
            return ('Four of a Kind',check_for_four_of_a_kind(random_deck)[1])
            ## print("Your highest combination is a Four of a Kind:", check_for_four_of_a_kind(random_deck)[1])

        elif check_for_fullhouse(random_deck)[0]:
            return ('Fullhouse',check_for_fullhouse(random_deck)[1])
            ## print("Your highest combination is a Fullhouse:", check_for_fullhouse(random_deck)[1])

        elif check_for_flush(random_deck)[0]:
            return ('Flush',check_for_flush(random_deck)[1])
            ## print("Your highest combination is a Flush:", check_for_flush(random_deck)[1])

        elif check_for_straight(random_deck)[0]:
            return ('Straight',check_for_straight(random_deck)[1])
            ## print("Your highest combination is a Straight:", check_for_straight(random_deck)[1])

        elif check_for_three_of_a_kind(random_deck)[0]:
            return ('Three of a Kind',check_for_three_of_a_kind(random_deck)[1])
            ## print("Your highest combination is a Three of a Kind:", check_for_three_of_a_kind(random_deck)[1])

        elif check_for_two_pair(random_deck)[0]:
            return ('Two Pair',check_for_two_pair(random_deck)[1])
            ## print("Your highest combination is a Two Pair:", check_for_two_pair(random_deck)[1])

        elif check_for_one_pair(random_deck)[0]:
            return ('One Pair',check_for_one_pair(random_deck)[1])
            ## print("Your highest combination is a One Pair:", check_for_one_pair(random_deck)[1])

        else:
            return ('High Card',check_for_highcard(random_deck))
            ## print("Your highest card is:", check_for_highcard(random_deck))


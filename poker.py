from random import choice


def get_random_deck(size=7):
    random_deck = []
    list_of_cards = [("Kreuz",2),("Kreuz",3),("Kreuz",4),("Kreuz",5),("Kreuz",6),("Kreuz",7),("Kreuz",8),("Kreuz",9),("Kreuz",10),("Kreuz",11),("Kreuz",12),("Kreuz",13),("Kreuz",14),
                ("Karo",2),("Karo",3),("Karo",4),("Karo",5),("Karo",6),("Karo",7),("Karo",8),("Karo",9),("Karo",10),("Karo",11),("Karo",12),("Karo",13),("Karo",14),
                ("Herz",2),("Herz",3),("Herz",4),("Herz",5),("Herz",6),("Herz",7),("Herz",8),("Herz",9),("Herz",10),("Herz",11),("Herz",12),("Herz",13),("Herz",14),
                ("Piek",2),("Piek",3),("Piek",4),("Piek",5),("Piek",6),("Piek",7),("Piek",8),("Piek",9),("Piek",10),("Piek",11),("Piek",12),("Piek",13),("Piek",14)]
    
    for i in range(size):
        random_card = choice(list_of_cards)
        list_of_cards.remove(random_card)
        random_deck.append(random_card)
    return random_deck

def sort_cards(cards):
    cards.sort(key=lambda x:x[1], reverse=True)
    return cards

####################
#check combinations#
####################

# Check for Straight

def check_for_straight(random_deck):
    is_straight = False
    found = []
    if random_deck[0][1] == random_deck[1][1]+1 and random_deck[1][1] == random_deck[2][1]+1 and random_deck[2][1] == random_deck[3][1]+1 and random_deck[3][1] == random_deck[4][1]+1:
        is_straight = True
        found = random_deck[:5]
    elif random_deck[1][1] == random_deck[2][1]+1 and random_deck[2][1] == random_deck[3][1]+1 and random_deck[3][1] == random_deck[4][1]+1 and random_deck[4][1] == random_deck[5][1]+1 :
        is_straight = True
        found = random_deck[1:6]
    elif random_deck[2][1] == random_deck[3][1]+1 and random_deck[3][1] == random_deck[4][1]+1 and random_deck[4][1] == random_deck[5][1]+1 and random_deck[5][1] == random_deck[6][1]+1:
        is_straight = True
        found = random_deck[2:7]
    else:
        is_straight = False

    return is_straight,found

# Check for flush

def check_for_flush(random_deck):
    is_flush = False
    found = []
    Kreuz = [item for item in random_deck if item[0] == "Kreuz"]
    Piek = [item for item in random_deck if item[0] == "Piek"]
    Herz = [item for item in random_deck if item[0] == "Herz"]
    Karo = [item for item in random_deck if item[0] == "Karo"]
    if len(Herz)>=5:
        is_flush = True
        found = Herz
    elif len(Piek)>=5:
        is_flush = True
        found = Piek
    elif len(Kreuz)>=5:
        is_flush = True
        found = Kreuz
    elif len(Karo)>=5:
        is_flush = True
        found = Karo
    
    return is_flush,found

# Check for Royal Flush

def check_for_royal_flush(random_deck):
    is_royal_flush = False
    if random_deck[0][1] == 14 and random_deck[0][1] == random_deck[1][1]+1 and random_deck[1][1] == random_deck[2][1]+1 and random_deck[2][1] == random_deck[3][1]+1 and random_deck[3][1] == random_deck[4][1]+1:
        Kreuz = [item for item in random_deck[:5] if item[0] == "Kreuz"]
        Piek = [item for item in random_deck[:5] if item[0] == "Piek"]
        Herz = [item for item in random_deck[:5] if item[0] == "Herz"]
        Karo = [item for item in random_deck[:5] if item[0] == "Karo"]
        if len(Herz)>=5 or len(Piek)>=5 or len(Karo)>=5 or len(Kreuz)>=5:
            is_royal_flush = True
    return is_royal_flush

# Check for Two Pair

def check_for_two_pair(random_deck):
    is_two_pair = False
    found = []
    if len(check_for_one_pair(random_deck)[1]) >= 4:
        is_two_pair = True
        found = check_for_one_pair(random_deck)[1]
        sort_cards(found)
    return is_two_pair, found[:4]
        

# Check for one Pair

def check_for_one_pair(random_deck):
    is_one_pair = False
    pairs_found = []
    values = [item[1] for item in random_deck]
    for i in range(2,15):
        if values.count(i)>=2:
            for item in random_deck:
                if item[1] == i:
                    pairs_found.append(item)
            is_one_pair = True
    return is_one_pair,pairs_found

# Check for three of a kind

def check_for_three_of_a_kind(random_deck):
    is_three_of_a_kind = False
    triple_found = []
    values = [item[1] for item in random_deck]
    for i in range(14,1,-1):
        if values.count(i)==3:
            for item in random_deck:
                if item[1] == i:
                    triple_found.append(item)
            is_three_of_a_kind = True
            break
    return is_three_of_a_kind,triple_found

# Check for Straight Flush

def check_for_straight_flush(random_deck):
    is_straight_flush = False
    found = []
    if random_deck[0][1] == random_deck[1][1]+1 and random_deck[1][1] == random_deck[2][1]+1 and random_deck[2][1] == random_deck[3][1]+1 and random_deck[3][1] == random_deck[4][1]+1 and check_for_flush(random_deck[:5])[0]:    
        is_straight_flush = True
        found = random_deck[:5]
    elif random_deck[1][1] == random_deck[2][1]+1 and random_deck[2][1] == random_deck[3][1]+1 and random_deck[3][1] == random_deck[4][1]+1 and random_deck[4][1] == random_deck[5][1]+1 and check_for_flush(random_deck[1:6])[0]:
        is_straight_flush = True
        found = random_deck[1:6]
    elif random_deck[2][1] == random_deck[3][1]+1 and random_deck[3][1] == random_deck[4][1]+1 and random_deck[4][1] == random_deck[5][1]+1 and random_deck[5][1] == random_deck[6][1]+1 and check_for_flush(random_deck[2:7])[0]:
        is_straight_flush = True
        found = random_deck[2:7]
    else:
        is_straight_flush = False

    return is_straight_flush,found

# Check fot Fullhouse

def check_for_fullhouse(random_deck):
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
                #sort_cards(three_of_a_kind[1])
    return is_fullhouse,three_of_a_kind[1]

# Check fot a Four of a Kind

def check_for_four_of_a_kind(random_deck):
    is_three_of_a_kind = False
    triple_found = []
    values = [item[1] for item in random_deck]
    for i in range(14,1,-1):
        if values.count(i)==4:
            for item in random_deck:
                if item[1] == i:
                    triple_found.append(item)
            is_three_of_a_kind = True
            
    return is_three_of_a_kind,triple_found

# Check for highest Card

def check_for_highcard(random_deck):
    return random_deck[0]

def get_highest_combi(player_deck,table_deck):
    random_deck = [('Herz', 8), ('Kreuz', 8), ('Karo', 13), ('Herz', 5), ('Kreuz', 5), ('Herz', 8), ('Herz', 5)]
    print()
    print("Zufälliges Karten:",random_deck)
    print("Karten sortiert anhand ihrem Wert:",sort_cards(random_deck))

    if check_for_royal_flush(random_deck):
        print("Your highest combination is a Royal Flush:",random_deck[:5])

    elif check_for_straight_flush(random_deck)[0]:
        print("Your highest combination is a Straight Flush:",check_for_straight_flush(random_deck)[1])

    elif check_for_four_of_a_kind(random_deck)[0]:
        print("Your highest combination is a Four of a Kind:",check_for_four_of_a_kind(random_deck)[1])

    elif check_for_fullhouse(random_deck)[0]:   
        print("Your highest combination is a Fullhouse:",check_for_fullhouse(random_deck)[1])

    elif check_for_flush(random_deck)[0]:
        print("Your highest combination is a Flush:",check_for_flush(random_deck)[1])

    elif check_for_straight(random_deck)[0]:
        print("Your highest combination is a Straight:",check_for_straight(random_deck)[1])
    
    elif check_for_three_of_a_kind(random_deck)[0]:
        print("Your highest combination is a Three of a Kind:",check_for_three_of_a_kind(random_deck)[1])

    elif check_for_two_pair(random_deck)[0]:
        print("Your highest combination is a Two Pair:",check_for_two_pair(random_deck)[1])

    elif check_for_one_pair(random_deck)[0]:
        print("Your highest combination is a One Pair:",check_for_one_pair(random_deck)[1])

    else:
        print("Your highest card is:",check_for_highcard(random_deck))
    
    print()

def create_decks():
    player_deck = get_random_deck(2)
    table_deck = get_random_deck(5)
    get_highest_combi(player_deck,table_deck)

create_decks()


#print("Zufälliges Karten:",random_deck)
#print("Karten sortiert anhand ihrem Wert:",sort_cards(random_deck))
#print("Is straight:",check_for_straight(random_deck))
#print("Is flush:",check_for_flush(random_deck))
#print("Is straight flush:",check_for_straight_flush(random_deck))
#print("Is royal flush:",check_for_royal_flush(random_deck))
#print("Is One Pair:",check_for_one_pair(random_deck))
#print("Is Two Pair:",check_for_two_pair(random_deck))
#print("Is Three of a Kind:",check_for_three_of_a_kind(random_deck))
#print("Is Full House:",check_for_fullhouse(random_deck))
#print("Is Four of a Kind:",check_for_four_of_a_kind(random_deck))
#print("The highest Card is:",check_for_highcard(random_deck))
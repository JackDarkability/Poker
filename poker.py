import random, copy
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
HANDS = [
    "High Card",
    "Pair",
    "Two Pair",
    "Three of a Kind",
    "Straight",
    "Flush",
    "Full House",
    "Four of a Kind",
    "Straight Flush",
]

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        # So can print name of Card
        return f"{self.value} of {self.suit}"

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __gt__(self, other):
        # For comparing cards
        if VALUES.index(self.value) > VALUES.index(other.value):
            return True
        else:
            return False

    def __lt__(self, other):
        # For comparing cards
        if VALUES.index(self.value) < VALUES.index(other.value):
            return True
        else:
            return False

    def __le__(self, other):
        # For comparing cards
        if VALUES.index(self.value) <= VALUES.index(other.value):
            return True
        else:
            return False

    def __ge__(self, other):
        # For comparing cards
        if VALUES.index(self.value) >= VALUES.index(other.value):
            return True
        else:
            return False


class Player:
    def __init__(self, starting_money, name):
        #id info
        self.name = name

        # Current round information
        self.hand = []
        self.amount_betted = 0
        self.folded = False

        # Money information
        self.current_money = starting_money
        self.money_won = (
            0  # This will be how much money won in total throughout the game
        )
        self.money_lost = (
            0  # This will be how much money lost in total throughout the game
        )

        # Final hand information
        self.result = 0  # Holds numerical value on hand result, 0 being high Card and 8 being straight flush
        self.top_card = None  # Holds top Card so can be compared when equal hand type

    def lose(self):
        self.money_lost += self.amount_betted

    def win(self, money_in_pot):
        self.money_won += money_in_pot
        self.current_money += money_in_pot

    def bet(self, amount):
        if amount > self.current_money:
            raise Exception("Not enough money to bet that much")
        else:
            self.amount_betted += amount
            self.current_money -= amount

    def fold(self):
        self.folded = True
        self.lose()

    def __gt__(self, other):
        # For seeing who wins. No functionality for if have same result yet (e.g. two players have pairs and so gets decided by the values.)
        if self.result > other.result:
            return True
        else:
            return False

    def __lt__(self, other):
        # For seeing who wins
        if self.result < other.result:
            return True
        else:
            return False

    def __le__(self, other):
        # For seeing who wins
        if self.result <= other.result:
            return True
        else:
            return False

    def __ge__(self, other):
        # For seeing who wins
        if self.result >= other.result:
            return True
        else:
            return False

    def get_hand(self):
        hand_readable = []
        for i in self.hand:
            hand_readable.append(i.__str__())
        return hand_readable

    def calculate_hand_result(self, cards_on_table):
        full_hand = [copy.deepcopy(card) for card in self.hand]
        full_hand.extend(cards_on_table)
        self.result, self.top_card = calculate_hand_result(full_hand)

    def reset(self):
        self.hand = []
        self.amount_betted = 0
        self.folded = False
        self.result = 0  # Holds numerical value on hand result, 0 being high Card and 8 being straight flush
        self.top_card = None  # Holds top Card so can be compared when equal hand type


def calculate_hand_result(
    cards,
):  # cards is 7 cards in a list, representing the 5 cards on the table and 2 cards in hand.

    # Need to add functionality for where same hand can be made by multiple players, e.g. two players have pairs and so gets decided by the values.
    cards.sort()
    card_is_straight, max_card_straight = is_straight(cards)
    card_is_flush, max_card_flush = is_flush(cards)
    counts = get_counts_of_cards(cards)
    highest_card = get_highest_card(cards)

    if card_is_straight and card_is_flush:  # Straight flush
        return (8, max_card_straight.value)

    if counts[max(counts, key=counts.get)] >= 4:  # 4 of a kind
        return 7, max(counts, key=counts.get)

    if (3 in counts.values() and 2 in counts.values()) or (
        list(counts.values()).count(3) == 2
    ):  # Full house
        return 6, max(counts, key=counts.get)

    if card_is_flush:  # Flush
        return (5, max_card_flush.value)

    if card_is_straight:  # Straight
        return (4, max_card_straight.value)

    if counts[max(counts, key=counts.get)] == 3:  # 3 of a kind
        return (3, max(counts, key=counts.get))

    if list(counts.values()).count(2) == 2:  # Two pair
        num_1 = max(counts, key=counts.get)
        counts[max(counts, key=counts.get)] = 0 # So can find the other pair
        num_2 = max(counts, key=counts.get)
        if VALUES.index(num_1) > VALUES.index(num_2):
            return (2, num_1)
        else:
            return (2, num_2)

    if counts[max(counts, key=counts.get)] == 2:  # Pair
        return (1, max(counts, key=counts.get))

    return 0, highest_card.value  # High Card


def is_straight(cards):
    max_sequence_counter = 0
    max_card_of_sequence = cards[0]
    sequence_counter = 0
    if cards[0].value == "2" and cards[-1].value == "A":
        max_card_of_sequence = cards[-1]
        max_sequence_counter = 1
    for index, card in enumerate(cards):
        try:
            if VALUES.index(card.value) + 1 == VALUES.index(cards[index + 1].value):
                sequence_counter += 1
            else:
                if sequence_counter > max_sequence_counter:
                    max_sequence_counter = sequence_counter
                    max_card_of_sequence = card
                sequence_counter = 0
        except IndexError:
            if sequence_counter > max_sequence_counter:
                max_sequence_counter = sequence_counter
            sequence_counter = 0

    if max_sequence_counter >= 4:
        return (True, max_card_of_sequence)

    else:
        return (False, max_card_of_sequence)


def is_flush(cards):
    suits_of_cards = []
    for card in cards:
        suits_of_cards.append(card.suit)

    for suit in SUITS:
        if suits_of_cards.count(suit) >= 5:
            for card in cards:
                if card.suit == suit:
                    maxCardOfFlush = card
            return (True, maxCardOfFlush)

    return (False, None)


def get_counts_of_cards(cards):
    # Gets the counts of each Card in the list of cards
    counts = {}
    for card in cards:
        amount = sum(x.value == card.value for x in cards)
        counts[card.value] = (
            amount  # Slight inefficiency here as will check same Card multiple times, but it's fine as the list of cards is small
        )

    return counts


def get_highest_card(cards):
    # For high Card
    highest_card = cards[0]
    for card in cards:
        if card > highest_card:
            highest_card = card

    return highest_card


def get_winner(players, cards_on_table):
    for player in players:
        player.calculate_hand_result(cards_on_table)

    players.sort(reverse=True)
    winning_index = 0
    winning_player = players[0]
    while winning_player.folded:
        print(winning_index)
        winning_index += 1
        winning_player = players[winning_index]

    for player in players:
        if player.result == winning_player.result and player.folded == False:
            if Card(player.top_card, "Hearts") > Card(winning_player.top_card, "Hearts"):
                # Hearts is just a random suit to compare by
                winning_player = player
    return winning_player


def deal_to_all(players, cards_on_table, deck):
    (players, deck) = deal_to_players(players, deck)
    (cards_on_table, deck) = deal_to_table(cards_on_table, deck)
    return (players, cards_on_table, deck)


def deal_to_players(players, deck):
    for i in range(len(players)):
        if players[i].folded:
            continue
        players[i].hand.append(deck.pop())

    return (players, deck)


def deal_to_table(cards_on_table, deck):
    cards_on_table.append(deck.pop())
    return (cards_on_table, deck)


def make_cards_readable(list):
    readable_list = []
    for i in list:
        readable_list.append(i.__str__())
    return readable_list


def betting_round(players, first_round):
    if one_person_left(players) == False:
        for index, player in enumerate(players):  # First pass
            if player.folded or ((index==0 or index==1) and first_round):
                continue
            print_betted_amount(players)
            print(
                player.name
                + ", you have "
                + str(player.get_hand())
                + " and have $"
                + str(player.current_money)
                + ". would you like to fold,check/call or raise?"
            )
            action = input()
            if action == "fold":
                player.fold()
            elif action == "call" or action == "check":
                player.bet(get_max_betted(players) - player.amount_betted)
            elif action == "raise":
                print("How much would you like to raise by?")
                amount_to_bet = int(input())
                player.bet(amount_to_bet)
            else:
                print("INVALID INPUT, WRONG. FOLDING.")
                player.fold()

    # Circular betting loop until all players have bet the same amount
    while (all_bet_same(players) == False) and one_person_left(players) == False:
        for player in players:
            if player.folded or (player.amount_betted == get_max_betted(players)):
                continue
            print_betted_amount(players)
            print(
                player.name
                + ", you have "
                + str(player.get_hand())
                + " and have $"
                + str(player.current_money)
                + ". would you like to fold,call or raise?"
            )
            action = input()
            if action == "fold":
                player.fold()
            elif action == "call":
                player.bet(get_max_betted(players) - player.amount_betted)
            elif action == "raise":
                print("How much would you like to raise by?")
                amount_to_bet = int(input())
                player.bet(amount_to_bet)
            else:
                print("INVALID INPUT, WRONG. FOLDING.")
                player.fold()

            if all_bet_same(players) or one_person_left(players):
                break
    return players


def all_bet_same(players):
    bet_amount = players[0].amount_betted
    for player in players:
        if player.amount_betted != bet_amount and (not player.folded):
            return False
    return True


def one_person_left(players):
    players_left = 0
    for player in players:
        if not player.folded:
            players_left += 1
    if players_left == 1:
        return True
    return False


def print_betted_amount(players):
    for player in players:
        if player.folded:
            continue
        print(player.name + " has betted $" + str(player.amount_betted))


def get_max_betted(players):
    maxBetted = 0
    for player in players:
        if player.amount_betted > maxBetted:
            maxBetted = player.amount_betted
    return maxBetted

def play_round(players, deck, blind_cost = 10):
    cards_on_table = []

    players.append(players.pop(0))  # Rotate players
    cards_on_table = []
    for player in players:
        player.reset()

    players, deck = deal_to_players(players, deck)
    players, deck = deal_to_players(players, deck)

    for index, player in enumerate(players): # Beginnning blind
        if index == 0:
            players[0].bet(blind_cost // 2)
            print(players[0].name + " bets a small blind of $" + str(blind_cost // 2))

        elif index == 1:
            players[1].bet(blind_cost)
            print(players[1].name + " bets a big blind of $" + str(blind_cost))

    players = betting_round(players,True)

    stages = [3,1,1] # How many cards to flip before each round of betting
    for stage in stages:
        for i in range(stage): 
            cards_on_table,deck = deal_to_table(cards_on_table, deck)
        print(make_cards_readable(cards_on_table))
        players = betting_round(players,False)
        if one_person_left(players):
            print("Only one person left, they win!")
            for player in players:
                if not player.folded:
                    print(player.name + " wins!")
                    player.win(sum([player2.amount_betted for player2 in players]))
                else:
                    player.lose()
            break

    print(players[0].name + " has " + str(players[0].get_hand()))
    print(players[1].name + " has " + str(players[1].get_hand()))
    print(make_cards_readable(cards_on_table))
    players[0].calculate_hand_result(cards_on_table)
    players[1].calculate_hand_result(cards_on_table)
    print(
        players[0].name
        + " has "
        + HANDS[players[0].result]
        + " with a "
        + str(players[0].top_card)
    )
    print(
        players[1].name
        + " has "
        + HANDS[players[1].result]
        + " with a "
        + str(players[1].top_card)
    )
    winner = get_winner(players, cards_on_table)
    print(winner.name + " wins!")

    for player in players:
        if player.name == winner.name:
            player.win(sum([player.amount_betted for player in players]))
        else:
            player.lose()

    return (players, deck)  # for changes in money and cards




def main():
    deck = []

    players = []
    starting_money = 1000
    blind_cost = 10

    for suit in SUITS:
        for value in VALUES:
            deck.append(Card(value, suit))

    random.shuffle(deck)


    players.append(Player(starting_money, "Dave"))
    players.append(Player(starting_money, "Jim"))





    while True:
        players, deck = play_round(players, deck,blind_cost)
        for player in players:
            print(player.name + " has $" + str(player.current_money))

        print("Would you like to play another round?")
        action = input()
        if action == "no":
            break

if __name__ == "__main__":
    main()
    



"""
BUGS
Does not discriminate between HANDS results being separate, e.g not a straight flush but a straight and a flush separately in the hand.
"""

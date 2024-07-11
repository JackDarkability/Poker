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
    def __init__(self, value="2", suit="Hearts"):
        self.value = value
        self.suit = suit

    def __str__(self):
        # So can print name of Card
        return f"{self.value} of {self.suit}"

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __gt__(self, other):
        # For comparing cards
        return VALUES.index(self.value) > VALUES.index(other.value)

    def __lt__(self, other):
        # For comparing cards
        return VALUES.index(self.value) < VALUES.index(other.value)

    def __le__(self, other):
        # For comparing cards
        return VALUES.index(self.value) <= VALUES.index(other.value)

    def __ge__(self, other):
        # For comparing cards
        return VALUES.index(self.value) >= VALUES.index(other.value)
        
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

def make_cards_readable(list):
    readable_list = []
    for i in list:
        readable_list.append(i.__str__())
    return readable_list

import copy
from hand_functionality import calculate_hand_result

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
        self.top_card = None  # Holds top Card value so can be compared when equal hand type

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
        return self.result > other.result

    def __lt__(self, other):
        # For seeing who wins
        return self.result < other.result

    def __le__(self, other):
        # For seeing who wins
        return self.result <= other.result

    def __ge__(self, other):
        # For seeing who wins
        return self.result >= other.result

    def get_hand(self):
        hand_readable = []
        for i in self.hand:
            hand_readable.append(str(i))
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
    

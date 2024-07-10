import random

class card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        # So can print name of card
        return f"{self.value} of {self.suit}"
    
    def __eq__(self,other):
        return (self.value == other.value and self.suit == other.suit)
    
    def __gt__(self,other):
        # For comparing cards
        if(values.index(self.value) > values.index(other.value)):
            return True
        else:
            return False

    def __lt__(self,other):
        # For comparing cards
        if(values.index(self.value) < values.index(other.value)):
            return True
        else:
            return False
    
    def __le__(self,other):
        # For comparing cards
        if(values.index(self.value) <= values.index(other.value)):
            return True
        else:
            return False
    
    def __ge__(self,other):
        # For comparing cards
        if(values.index(self.value) >= values.index(other.value)):
            return True
        else:
            return False
    
class player:
    def __init__(self,startingMoney,name):
        self.name = name
        self.hand = []
        self.amountBetted = 0
        self.currentMoney = startingMoney
        self.moneyWon = 0 # This will be how much money won in total throughout the game
        self.moneyLost = 0 # This will be how much money lost in total throughout the game
        self.folded = False
        self.result=0 # Holds numerical value on hand result, 0 being high card and 8 being straight flush

    def lose(self):
        self.moneyLost += self.amountBetted
        self.amountBetted = 0

    def win(self,moneyInPot):
        self.moneyWon += moneyInPot
        self.amountBetted = 0
    
    def bet(self, amount):
        if(amount > self.currentMoney):
            raise Exception("Not enough money to bet that much")
        else:
            self.amountBetted += amount
            self.currentMoney -= amount

    def fold(self):
        self.folded = True
        self.lose()

    def __gt__(self,other):
        # For seeing who wins. No functionality for if have same result yet (e.g. two players have pairs and so gets decided by the values.)
        if(self.result > other.result):
            return True
        else:
            return False

    def __lt__(self,other):
        # For seeing who wins
        if(self.result < other.result):
            return True
        else:
            return False
    
    def __le__(self,other):
        # For seeing who wins
        if(self.result <= other.result):
            return True
        else:
            return False
    
    def __ge__(self,other):
        # For seeing who wins
        if(self.result >= other.result):
            return True
        else:
            return False
    
    def getHand(self):
        handReadable=[]
        for i in self.hand:
            handReadable.append(i.__str__())
        return handReadable
        
    def getHandResult(self,cardsOnTable):
        fullHand = self.hand
        fullHand.extend(cardsOnTable)
        self.result = getHandResult(fullHand)

def getHandResult(cards): # cards is 7 cards in a list, representing the 5 cards on the table and 2 cards in hand.

    #Need to add functionality for where same hand can be made by multiple players, e.g. two players have pairs and so gets decided by the values.
    cards.sort()
    cardIsStraight = isStraight(cards)
    cardIsFlush = isFlush(cards)
    counts = getCountsOfCards(cards)
    highestCard = getHighestCard(cards)

    if(cardIsStraight and cardIsFlush):
        return 8
    
    if(counts[max(counts,key=counts.get)]>=4):
        return 7
    
    if((3 in counts.values() and 2 in counts.values()) or (list(counts.values()).count(3) == 2)):
        return 6
    
    if(cardIsFlush):
        return 5
    
    if(cardIsStraight):
        return 4
    
    if(counts[max(counts,key=counts.get)]==3):
        return 3

    if(list(counts.values()).count(2) == 2):
        return 2
    
    if(counts[max(counts,key=counts.get)]==2):
        return 1

    return 0


def isStraight(cards):
    #Does not take into account A working as 1 yet!!!
    maxSequenceCounter=0
    sequenceCounter=0
    for index,card in enumerate(cards):
        try:
            if(values.index(card.value)+1 == values.index(cards[index+1].value)):
                sequenceCounter+=1
            else:
                if(sequenceCounter > maxSequenceCounter):
                    maxSequenceCounter = sequenceCounter
                sequenceCounter=0
        except IndexError:
            if(sequenceCounter > maxSequenceCounter):
                maxSequenceCounter = sequenceCounter
            sequenceCounter=0
    if(maxSequenceCounter >= 5):
        return True

    else:
        return False

def isFlush(cards):
    suitsOfCards = []
    for card in cards:
        suitsOfCards.append(card.suit)
    
    for suit in suits:
        if(suitsOfCards.count(suit) >= 5):
            return True
    
    return False

def getCountsOfCards(cards):
    # Gets the counts of each card in the list of cards
    counts = {}
    for card in cards:
        amount = sum(x.value == card.value for x in cards)
        counts[card.value] = amount # Slight inefficiency here as will check same card multiple times, but it's fine as the list of cards is small
    
    return counts

def getHighestCard(cards):
    # For high card
    highestCard = cards[0]
    for card in cards:
        if(card>highestCard):
            highestCard = card

    return highestCard
        
def getWinner(players,cardsOnTable):

    for player in players:
        player.hand = player.hand + cardsOnTable
        player.hand.sort()
        player.getHandResult()

    results=players
    results.sort()
    results.reverse()
    return results[0]

    
def dealToAll(players,cardsOnTable,deck):
    (players,deck)=dealToPlayers(players,deck)
    (cardsOnTable,deck)=dealToTable(cardsOnTable,deck)
    return (players,cardsOnTable,deck)

def dealToPlayers(players,deck):
    for i in range(len(players)):
        if(players[i].folded):
            continue
        players[i].hand.append(deck.pop())
    
    return (players,deck)

def dealToTable(cardsOnTable,deck):
    cardsOnTable.append(deck.pop())
    return (cardsOnTable,deck)

def makeCardsReadable(list):
    readableList = []
    for i in list:
        readableList.append(i.__str__())
    return readableList

deck = []
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
values = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
hands = ["High Card","Pair","Two Pair","Three of a Kind","Straight","Flush","Full House","Four of a Kind","Straight Flush"]
players = [] 
cardsOnTable = []
startingMoney = 1000

for suit in suits:
    for value in values:
        deck.append(card(value, suit))

random.shuffle(deck)


players.append(player(startingMoney,"Dave"))

'''
players,cardsOnTable,deck = dealToAll(players,cardsOnTable,deck)
players,cardsOnTable,deck = dealToAll(players,cardsOnTable,deck)
cardsOnTable,deck = dealToTable(cardsOnTable,deck)
cardsOnTable,deck = dealToTable(cardsOnTable,deck)
cardsOnTable,deck = dealToTable(cardsOnTable,deck)

print(players[0].getHand())

print(makeCardsReadable(cardsOnTable))
players[0].hand.extend(cardsOnTable)
print(players[0].getHand())
players[0].getHandResult()
print(hands[players[0].result])
print(makeCardsReadable(deck))

'''

'''
players[0].hand=[card("A","Diamonds"),card("K","Hearts"),card("Q","Clubs"),card("J","Hearts"),card("10","Hearts"),card("9","Spades"),card("8","Hearts")]
print(players[0].getHand())
players[0].getHandResult(cardsOnTable)
print(hands[players[0].result])
'''

def playRound(players,deck):
    cardsOnTable = []
    players,cardsOnTable,deck = dealToAll(players,cardsOnTable,deck)
    players,cardsOnTable,deck = dealToAll(players,cardsOnTable,deck)
    cardsOnTable,deck = dealToTable(cardsOnTable,deck)
    cardsOnTable,deck = dealToTable(cardsOnTable,deck)
    cardsOnTable,deck = dealToTable(cardsOnTable,deck)
    print(makeCardsReadable(cardsOnTable))
    print(players[0].getHand())
    players[0].getHandResult(cardsOnTable)
    print(hands[players[0].result])

    return (players,deck) # for changes in money and cards

players,deck = playRound(players,deck)

'''
BUGS
No way to deal with two players having the same hand, e.g. two players have pairs and so gets decided by the values.
No way to deal with A working as 1 in a straight
Does not discriminate between hands results being separate, e.g not a straight flush but a straight and a flush separately in the hand.
'''
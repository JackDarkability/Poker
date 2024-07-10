import random, copy

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
        self.topCard = None # Holds top card so can be compared when equal hand type

    def lose(self):
        self.moneyLost += self.amountBetted

    def win(self,moneyInPot):
        self.moneyWon += moneyInPot
        self.currentMoney += moneyInPot

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
        
    def calculateHandResult(self,cardsOnTable):
        fullHand = [copy.deepcopy(card) for card in self.hand]
        fullHand.extend(cardsOnTable)
        self.result,self.topCard = calculateHandResult(fullHand)

    def reset(self):
        self.hand = []
        self.amountBetted = 0
        self.folded = False
        self.result=0 # Holds numerical value on hand result, 0 being high card and 8 being straight flush
        self.topCard = None # Holds top card so can be compared when equal hand type


def calculateHandResult(cards): # cards is 7 cards in a list, representing the 5 cards on the table and 2 cards in hand.

    #Need to add functionality for where same hand can be made by multiple players, e.g. two players have pairs and so gets decided by the values.
    cards.sort()
    cardIsStraight,maxCardStraight = isStraight(cards)
    cardIsFlush,maxCardFlush = isFlush(cards)
    counts = getCountsOfCards(cards)
    highestCard = getHighestCard(cards)

    if(cardIsStraight and cardIsFlush): # Straight flush
        return (8,maxCardStraight.value)
    
    if(counts[max(counts,key=counts.get)]>=4): #4 of a kind
        return 7,max(counts,key=counts.get)
    
    if((3 in counts.values() and 2 in counts.values()) or (list(counts.values()).count(3) == 2)): # Full house
        return 6,max(counts,key=counts.get)
    
    if(cardIsFlush): # Flush
        return (5,maxCardFlush.value)
    
    if(cardIsStraight): # Straight
        return (4,maxCardStraight.value)
    
    if(counts[max(counts,key=counts.get)]==3):  # 3 of a kind
        return (3,max(counts,key=counts.get))

    if(list(counts.values()).count(2) == 2): # Two pair
        return (2,max(counts,key=counts.get)) # Might get lower of the 2 pairs, will have to check
    
    if(counts[max(counts,key=counts.get)]==2): # Pair
        return (1,max(counts,key=counts.get))

    return 0,highestCard.value # High card


def isStraight(cards):
    maxSequenceCounter=0
    maxCardOfSequence = cards[0]
    sequenceCounter=0
    if cards[0].value=="2" and cards[-1].value=="A":
        maxCardOfSequence = cards[-1]
        maxSequenceCounter = 1
    for index,card in enumerate(cards):
        try:
            if(values.index(card.value)+1 == values.index(cards[index+1].value)):
                sequenceCounter+=1
            else:
                if(sequenceCounter > maxSequenceCounter):
                    maxSequenceCounter = sequenceCounter
                    maxCardOfSequence = card
                sequenceCounter=0
        except IndexError:
            if(sequenceCounter > maxSequenceCounter):
                maxSequenceCounter = sequenceCounter
            sequenceCounter=0

    if(maxSequenceCounter >= 4):
        return (True,maxCardOfSequence)

    else:
        return (False,maxCardOfSequence)

def isFlush(cards):
    suitsOfCards = []
    for card in cards:
        suitsOfCards.append(card.suit)
    
    for suit in suits:
        if(suitsOfCards.count(suit) >= 5):
            for card in cards:
                if(card.suit == suit):
                    maxCardOfFlush = card
            return (True,maxCardOfFlush)
    
    return (False,None)

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
    #tempHand = [copy.deepcopy(player) for player in players]
    for player in players:
        player.calculateHandResult(cardsOnTable)
        #print(player.name+" has "+str(hands[player.result]) + ", a "+str(player.result))

    players.sort(reverse=True)
    winningIndex = 0
    winningPlayer = players[0]
    while(winningPlayer.folded):
        print(winningIndex)
        winningIndex+=1
        winningPlayer = players[winningIndex]

    for player in players:
        if(player.result == winningPlayer.result and player.folded == False):
            if(card(player.topCard,"Hearts") > card(winningPlayer.topCard,"Hearts")):
                # Hearts is just a random suit to compare by
                winningPlayer = player
    return winningPlayer

    
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

def bettingRound(players):
    if(onePersonLeft(players)==False):
        for player in players: # First pass
            if(player.folded):
                continue
            printBettedAmount(players)
            print(player.name + ", you have "+str(player.getHand()) +" and have $"+str(player.currentMoney)+". would you like to fold,check/call or raise?")
            action = input()
            if(action == "fold"):
                player.fold()
            elif(action == "call"):
                player.bet(getMaxBetted(players)-player.amountBetted)
            elif(action == "raise"):
                print("How much would you like to raise by?")
                amountToBet = int(input())
                player.bet(amountToBet)
            else:
                print("INVALID INPUT, WRONG. FOLDING.")
                player.fold()


    while((allBetSame(players)==False) and onePersonLeft(players)==False):
        for player in players:
            if(player.folded or (player.amountBetted == getMaxBetted(players))):
                continue
            printBettedAmount(players)
            print(player.name + ", you have "+str(player.getHand()) +" and have $"+str(player.currentMoney)+". would you like to fold,call or raise?")
            action = input()
            if(action == "fold"):
                player.fold()
            elif(action == "call"):
                player.bet(getMaxBetted(players)-player.amountBetted)
            elif(action == "raise"):
                print("How much would you like to raise by?")
                amountToBet = int(input())
                player.bet(amountToBet)
            else:
                print("INVALID INPUT, WRONG. FOLDING.")
                player.fold()

            if(allBetSame(players) or onePersonLeft(players)):
                break
    return players

def allBetSame(players):
    betAmount=players[0].amountBetted
    for player in players:
        if(player.amountBetted != betAmount and (not player.folded)):
            return False
    return True

def onePersonLeft(players):
    playersLeft = 0
    for player in players:
        if(not player.folded):
            playersLeft+=1
    if(playersLeft == 1):
        return True
    return False

def printBettedAmount(players):
    for player in players:
        if(player.folded):
            continue
        print(player.name + " has betted $"+str(player.amountBetted))

def getMaxBetted(players):
    maxBetted = 0
    for player in players:
        if(player.amountBetted > maxBetted):
            maxBetted = player.amountBetted
    return maxBetted

deck = []
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
values = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
hands = ["High Card","Pair","Two Pair","Three of a Kind","Straight","Flush","Full House","Four of a Kind","Straight Flush"]
players = [] 
cardsOnTable = []
startingMoney = 1000
blindCost = 10

for suit in suits:
    for value in values:
        deck.append(card(value, suit))

random.shuffle(deck)


players.append(player(startingMoney,"Dave"))
players.append(player(startingMoney,"Jim"))

def playRound(players,deck):
    players.append(players.pop(0)) # Rotate players
    cardsOnTable = []
    for player in players:
        player.reset()

    players,deck = dealToPlayers(players,deck)
    players,deck = dealToPlayers(players,deck)

    for index,player in enumerate(players):
        if(index == 0):
            players[0].bet(blindCost//2)
            print(players[0].name + " bets a small blind of $"+str(blindCost//2))

        elif(index == 1):
            players[1].bet(blindCost)
            print(players[1].name + " bets a big blind of $"+str(blindCost))
        
        else:
            if(player.folded):
                continue
            printBettedAmount(players)
            print(player.name + ", you have "+str(player.getHand()) +" and have $"+str(player.currentMoney)+". would you like to fold,check/call or raise?")
            action = input()
            if(action == "fold"):
                player.fold()
            elif(action == "call"):
                player.bet(getMaxBetted(players)-player.amountBetted)
            elif(action == "raise"):
                print("How much would you like to raise by?")
                amountToBet = int(input())
                player.bet(amountToBet)
            else:
                print("INVALID INPUT, WRONG. FOLDING.")
                player.fold()

    while(allBetSame(players)==False and onePersonLeft(players)==False):
        for player in players:
            if(player.folded or (player.amountBetted == getMaxBetted(players))):
                continue
            printBettedAmount(players)
            print(player.name + ", you have "+str(player.getHand()) +" and have $"+str(player.currentMoney)+". would you like to fold,check/call or raise?")
            action = input()
            if(action == "fold"):
                player.fold()
            elif(action == "call"):
                player.bet(getMaxBetted(players)-player.amountBetted)
            elif(action == "raise"):
                print("How much would you like to raise by?")
                amountToBet = int(input())
                player.bet(getMaxBetted(players)-player.amountBetted)
                player.bet(amountToBet)

            else:
                print("INVALID INPUT, WRONG. FOLDING.")
                player.fold()

            if(allBetSame(players) or onePersonLeft(players)):
                break

    if(onePersonLeft(players)):
        print("Only one person left, they win!")
        for player in players:
            if(not player.folded):
                print(player.name +" wins!")
                player.win(sum([player.amountBetted for player in players]))
            else:
                player.lose()
        return (players,deck)
    
    cardsOnTable,deck = dealToTable(cardsOnTable,deck)
    cardsOnTable,deck = dealToTable(cardsOnTable,deck)
    cardsOnTable,deck = dealToTable(cardsOnTable,deck)

    print(makeCardsReadable(cardsOnTable))
    players = bettingRound(players)
    
    if(onePersonLeft(players)):
        print("Only one person left, they win!")
        for player in players:
            if(not player.folded):
                print(player.name +" wins!")
                player.win(sum([player.amountBetted for player in players]))
            else:
                player.lose()
        return (players,deck)
            
    cardsOnTable,deck = dealToTable(cardsOnTable,deck)
    print(makeCardsReadable(cardsOnTable))
    players = bettingRound(players)

    if(onePersonLeft(players)):
        print("Only one person left, they win!")
        for player in players:
            if(not player.folded):
                print(player.name +" wins!")
                player.win(sum([player.amountBetted for player in players]))
            else:
                player.lose()
        return (players,deck)
    
    cardsOnTable,deck = dealToTable(cardsOnTable,deck)
    print(makeCardsReadable(cardsOnTable))
    players = bettingRound(players)

    if(onePersonLeft(players)):
        print("Only one person left, they win!")
        for player in players:
            if(not player.folded):
                print(player.name +" wins!")
                player.win(sum([player.amountBetted for player in players]))
            else:
                player.lose()
        return (players,deck)

    print(players[0].name+" has "+str(players[0].getHand()))
    print(players[1].name+" has "+str(players[1].getHand()))
    print(makeCardsReadable(cardsOnTable))
    players[0].calculateHandResult(cardsOnTable)
    players[1].calculateHandResult(cardsOnTable)
    print(players[0].name+" has "+hands[players[0].result] +" with a "+str(players[0].topCard))
    print(players[1].name+" has "+hands[players[1].result] +" with a "+str(players[1].topCard))
    winner = getWinner(players,cardsOnTable)
    print(winner.name +" wins!")

    for player in players:
        if(player.name==winner.name):
            player.win(sum([player.amountBetted for player in players]))
        else:
            player.lose()

    return (players,deck) # for changes in money and cards

players,deck = playRound(players,deck)
for player in players:
    print(player.name + " has $"+str(player.currentMoney))


#players[0].hand=[card("J","Hearts"),card("J","Diamonds")]
#players[1].hand = [card("9","Spades"),card("A","Spades")]
#players.sort()
#cardsOnTable = [card("8","Diamonds"),card("3","Diamonds"),card("10","Clubs"),card("5","Hearts"),card("A","Hearts")]
#print(getWinner(players,cardsOnTable).name +" wins!")
#print(players[0].topCard)
#print(players[1].topCard)
'''
BUGS
Does not discriminate between hands results being separate, e.g not a straight flush but a straight and a flush separately in the hand.
'''


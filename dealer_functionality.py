from hand_functionality import Card, SUITS, VALUES
import random


def get_winner(players, cards_on_table):
    """
    Calculates the winner of the round based on the players' hands and the cards on the table
    players: list of Players which holds the players' hands
    cards_on_table: list of Cards which are the 5 cards in the flop
    """
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
            if Card(value=player.top_card) > Card(value=winning_player.top_card):
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


def all_bet_same(players):
    bet_amount = 0
    for player in players:
        if player.amount_betted > bet_amount and (not player.folded):
            bet_amount = player.amount_betted

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
    max_betted = 0
    for player in players:
        if player.amount_betted > max_betted:
            max_betted = player.amount_betted

    return max_betted


def get_winner(players, cards_on_table):
    for player in players:
        player.calculate_hand_result(cards_on_table)

    players.sort(reverse=True)
    winning_index = 0
    winning_player = players[0]
    while winning_player.folded:
        winning_index += 1
        winning_player = players[winning_index]

    for player in players:
        if player.result == winning_player.result and player.folded == False:
            if Card(value=player.top_card) > Card(value=winning_player.top_card):
                winning_player = player

    return winning_player


def create_deck():
    deck = []

    for suit in SUITS:
        for value in VALUES:
            deck.append(Card(value, suit))

    random.shuffle(deck)
    return deck

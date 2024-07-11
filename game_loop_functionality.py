from hand_functionality import make_cards_readable, HANDS
from dealer_functionality import (
    one_person_left,
    print_betted_amount,
    all_bet_same,
    get_winner,
    deal_to_players,
    deal_to_table,
    get_max_betted,
)


def play_round(players, deck, blind_cost=10):
    """
    Play a full round of poker
    players: list of Player objects from player_functionality.py
    deck: list of Card objects from hand_functionality.py
    blind_cost: int, the cost of the big blind

    Returns: tuple of list of updated Players and updated deck (with used cards removed) as a list of Cards
    """

    cards_on_table = []

    players.append(players.pop(0))  # Rotate players
    cards_on_table = []
    for player in players:
        player.reset()

    players, deck = deal_to_players(players, deck)
    players, deck = deal_to_players(players, deck)

    for index, player in enumerate(players):  # Beginnning blind
        if index == 0:
            players[0].bet(blind_cost // 2)
            print(players[0].name + " bets a small blind of $" + str(blind_cost // 2))

        elif index == 1:
            players[1].bet(blind_cost)
            print(players[1].name + " bets a big blind of $" + str(blind_cost))

    players = betting_round(players, True)

    stages = [3, 1, 1]  # How many cards to flip before each round of betting
    for stage in stages:
        for i in range(stage):
            cards_on_table, deck = deal_to_table(cards_on_table, deck)
        print(make_cards_readable(cards_on_table))
        players = betting_round(players, False)
        if one_person_left(players):
            print("Only one person left, they win!")
            for player in players:
                if not player.folded:
                    print(player.name + " wins!")
                    player.win(sum([player2.amount_betted for player2 in players]))
                else:
                    player.lose()
            break

    for player in players:
        print(player.name + " has " + str(player.get_hand()))
        player.calculate_hand_result(cards_on_table)
        print(
            player.name
            + " has "
            + HANDS[player.result]
            + " with a "
            + str(player.top_card)
        )

    winner = get_winner(players, cards_on_table)
    print(winner.name + " wins!")

    for player in players:
        if player.name == winner.name:
            player.win(sum([player2.amount_betted for player2 in players]))
        else:
            player.lose()

    return (players, deck)  # for changes in money and cards


def betting_round(players, first_round):
    '''
    One round of betting, goes around the table of players until all players have bet the same amount or folded
    first_round: bool, if it is the first round of betting and therefore whether to skip the first 2 players as they have already bet the blinds
    '''

    if one_person_left(players) == False:
        for index, player in enumerate(players):  # First pass
            if player.folded or ((index == 0 or index == 1) and first_round):
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
                player.bet((get_max_betted(players) - player.amount_betted) + amount_to_bet)
            else:
                print("INVALID INPUT, WRONG. FOLDING.")
                player.fold()

            if(one_person_left(players)):
                break

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
                player.bet((get_max_betted(players) - player.amount_betted) + amount_to_bet)
            else:
                print("INVALID INPUT, WRONG. FOLDING.")
                player.fold()

            if all_bet_same(players) or one_person_left(players):
                break
    return players

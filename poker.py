from player_functionality import Player
from dealer_functionality import create_deck
from game_loop_functionality import play_round


def main():
    deck = create_deck()
    players = []
    num_players = int(input("How many players are there?"))
    starting_money = int(input("How much money does each player start with?"))

    for i in range(num_players):
        name = input("What is player " + str(i + 1) + "'s name?")
        players.append(Player(starting_money, name))

    blind_cost = int(input("How much is the big blind?"))

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
Does not discriminate between hands results being separate, e.g not a straight flush but a straight and a flush separately in the hand.
"""

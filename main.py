#! /usr/bin/python
import argparse
from game import Game
from game_info import GameInfo

# Define the command line arguments for the program
parser = argparse.ArgumentParser(description="Simulate games of the card game Fuck the Dealer")
parser.add_argument("num_players", metavar="num_players", type=int, help="Specify the number of players that you would like to add to the game in range [2, 8]", choices=range(2, 9))
parser.add_argument("num_rounds", metavar="num_rounds", type=int, help="Specify the number of rounds that you would like to simulate in the range [1, 1000000]", choices=range(1, 1000000))
parser.add_argument("--verbose", dest="verbose", default=False, help="Include in order to see a print out of what's being run in the program.", action="store_true")
args = parser.parse_args()

if args.verbose:
    print "Starting the game....\n"
    game = Game(GameInfo(args.num_players), args.verbose, args.num_players)
    while len(game.game_info.main_deck) != 0:
        print "\nHere's the main deck"
        print ', '.join(game.game_info.main_deck)
        print "Dealer is currently " + str(game.game_info.dealer)
        print "Guesser is currently " + str(game.game_info.guesser)
        for i in range(6):
            print "Player " + str(i) + " has drunk " + str(game.game_info.players[i].imbibed) + " drinks."
        game.turn()
        print "Table deck now has"
        print ', '.join(game.game_info.table)
        print "Main deck now has"
        print ', '.join(game.game_info.main_deck)


wins = 0.0
drinks = [ 0 for _ in range(args.num_players)]
for i in range(args.num_rounds):
    game = Game(GameInfo(args.num_players), args.verbose, args.num_players)
    while len(game.game_info.main_deck) != 0:
        game.turn()

    smart_player_drinks = game.game_info.players[0].imbibed
    least_drinks = True
    for player in game.game_info.players:
        if player.imbibed < smart_player_drinks:
            least_drinks = False
    for i in range(len(game.game_info.players)):
        drinks[i] += game.game_info.players[i].imbibed

    if least_drinks:
        wins += 1.0

print "The smart player won " + str((wins / args.num_rounds) * 100) + "% of the time"
print drinks




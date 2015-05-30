# Play a game of Fuck the Dealer with the Deck class that exists in this directory
from deck import Deck
from random import randrange
from player import Player
import sys

class GameInfo:

    def __init__(self, num_players):
        # Face values in a list that will facilitate guessing
        self.FACE_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']
        self.main_deck = Deck().deck
        self.table = []

        # To simulate the amount that each player would have to drink, I'll assume that each "drink" of beer would be 1 oz.
        # The game will be simulated with 6 players
        self.players = [Player() for _ in range(num_players)]
        self.players[0].playing_smart = True

        # Make the first player the dealer. The dealer variable stores the index of the current dealer. The guesser variable stores the index of the player who is currently guessing the card
        self.dealer = 0
        self.guesser = 1



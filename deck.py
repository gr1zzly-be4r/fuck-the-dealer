# Class for creating a deck of cards
import random

class Deck:

    # This is the "base" deck of cards. Each of the cards has their face value followed by a single letter which denotes their suit.
    UNSHUFFLED_DECK = [
            'as', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', 'js', 'qs', 'ks',
            'ac', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', 'jc', 'qc', 'kc',
            'ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', 'jh', 'qh', 'kh',
            'ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', 'jd', 'qd', 'kd']

    def __init__(self):
        self.deck = []
        for card in range(52):
            # Crude way of shuffling the deck. The pop function will remove a random card from the deck
            # and then that card will be appended to the deck of this Deck class.
            self.deck.append(Deck.UNSHUFFLED_DECK.pop(random.randrange(len(Deck.UNSHUFFLED_DECK))))
        self.played = []


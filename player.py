# Player class for the fuck_the_dealer.py game

class Player:

    def __init__(self):
        self.imbibed = 0
        self.dealer = False
        self.missed_guesses = 0
        self.playing_smart = False

    def not_dealer(self):
        return self.missed_guesses == 3

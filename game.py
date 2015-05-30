#! /usr/bin/env python
from random import randrange

# Script meant to better organize methods for the fuck-the-dealer game

class Game:

    def __init__(self, game_info, verbose, num_players):
        self.game_info = game_info
        self.verbose = verbose
        self.num_players = num_players

    def face_to_int(self, face_value):
        if face_value == 'a':
            return 14
        elif face_value == 'k':
            return 13
        elif face_value == 'q':
            return 12
        elif face_value == 'j':
            return 11
        else:
            return int(face_value)

    # Method for moving the dealer index through the list of players
    def move_index(self, index):
        return (index + 1) % self.num_players

    # Method for moving the guesser index through the list of players.
    # Difference between this method and the one above is that this
    # method ensures that the new guesser index will not be the same
    # as the current dealer index.
    def move_guesser_index(self, g_index, d_index):
        n_index = self.move_index(g_index)
        if n_index == d_index:
            n_index = self.move_index(n_index)
        return n_index

    # The following method will be define how a player can play "smart" instead of random.
    # This means that the player will choose the card with the highest probability of being correct. In theory, this should
    # ensure that the player drinks the least amount out of all the other players if those players
    # playing randomly.
    def play_smart(self, first, first_guess, higher):
        # Get the necessary numbers for making the smartest guess.
        table = self.game_info.table
        FACE_VALUES = self.game_info.FACE_VALUES
        remaining_cards = 52 - len(table)
        cards_left = { key: 4.0 for key in FACE_VALUES }

        for card in table:
            # This loop will find the amount of remaining cards for each face value left in the deck
            cards_left[card[:-1]] -= 1

        if first:
            # The first guess should be made by factoring the probability of three things for each card
            # 1. The probability of the card being the top card
            # 2. The summed probability of the cards with a higher face value being the top card
            # 3. The summed probability of the cards with a lower face value being the top card
            expected_value = { key: 0.0 for key in FACE_VALUES }

            for key, value in expected_value.iteritems():
                first_guess_correct = cards_left[key] / remaining_cards
                top_card_higher = 0.0
                higher_cards = 0.0
                # Iterate over the entire FACE_VALUES array to get expected values for the higher cards
                for i in range(FACE_VALUES.index(key) + 1, len(FACE_VALUES)):
                    top_card_higher += cards_left[FACE_VALUES[i]] / remaining_cards
                    higher_cards += cards_left[FACE_VALUES[i]]

                # "Weighting" the number of cards that are higher/lower
                prob_higher = (higher_cards / remaining_cards) * top_card_higher

                top_card_lower = 0.0
                # Iterate over the entire FACE_VALUES array to get expected values for the lower cards
                for i in range(0, FACE_VALUES.index(key)):
                    top_card_lower += cards_left[FACE_VALUES[i]] / remaining_cards

                # Subtraction here is to find the amount of cards left in the deck that are lower than the current card
                prob_lower = ((remaining_cards - cards_left[key] - higher_cards) / remaining_cards) * top_card_lower

                # Last thing to do is set the value of the key to the probability
                expected_value[key] = first_guess_correct * prob_higher * prob_lower
                if cards_left[key] == 0:
                    expected_value[key] = 0

            # Iterate through the expected value dictionary to get the maximum probability
            best_guess = '2'
            best_prob = expected_value[best_guess]
            for key, value in expected_value.iteritems():
                if value > best_prob:
                    best_prob = value
                    best_guess = key

            if self.verbose:
                print expected_value
                print "returning..." + best_guess
            return best_guess
        else:
            # The second guess should be made by choosing the card with the highest probability
            expected_value = { key: 0.0 for key in FACE_VALUES }

            # The "higher" boolean variable dictates the iteration over the remaining cards
            # "first_guess" gets passed into this entire method and gives the relative position for the iteration
            if higher:
                for i in range(FACE_VALUES.index(first_guess) + 1, len(FACE_VALUES)):
                    expected_value[FACE_VALUES[i]] = cards_left[FACE_VALUES[i]] / remaining_cards
            else:
                for i in range(0, FACE_VALUES.index(first_guess)):
                    expected_value[FACE_VALUES[i]] = cards_left[FACE_VALUES[i]] / remaining_cards

            # Iterate through the expected value dictionary to get the maximum probability
            best_guess = '2'
            best_prob = expected_value[best_guess]
            for key, value in expected_value.iteritems():
                if value > best_prob:
                    best_prob = value
                    best_guess = key

            if self.verbose:
                print expected_value
                print "returning..." + best_guess
            return best_guess

    def turn(self):
        # We are going to want to .pop() the first card in the deck everytime
        # because the cards are always taken out of the deck regardless of
        # whether or not the card has been guessed correctly.
        game = self.game_info
        index_of_first_guess = randrange(len(game.FACE_VALUES))
        first_guess = game.FACE_VALUES[index_of_first_guess]

        # If the guesser is playing smart then we just change the guess
        if game.players[game.guesser].playing_smart:
            first_guess = self.play_smart(True, None, False)
            index_of_first_guess = game.FACE_VALUES.index(first_guess)

        if self.verbose:
            print "First guess is a " + first_guess

        # The first card in the deck is going to get removed from the main deck
        # on every turn.
        top_card = game.main_deck.pop(0)

        if first_guess == top_card[:-1]:
            if self.verbose:
                print "The first guess was correct!"
            # In the event that the first guess is correct, the dealer has to drink 4 drinks
            game.players[game.dealer].imbibed += 4

            # Simulates placing the top card onto the table
            game.table.insert(0, top_card)

            game.guesser = self.move_guesser_index(game.guesser, game.dealer)

        elif self.face_to_int(first_guess) > self.face_to_int(top_card[:-1]):
            if self.verbose:
                print "The top card is lower than what the player guessed"
            # Now the player will randomly guess a face value between the first guess
            # and the lower end of the face values
            second_guess = game.FACE_VALUES[randrange(index_of_first_guess)]

            # If the guesser is playing smart then we need to change our guess
            if game.players[game.guesser].playing_smart:
                second_guess = self.play_smart(False, first_guess, False)

            if self.verbose:
                print "Second guess is a " + second_guess

            game.table.insert(0, top_card)
            # Two options now, the second guess was correct and the dealer has to
            # drink, or the second guess wasn't correct and the dealer gets a pass
            if second_guess == top_card[:-1]:
                if self.verbose:
                    print "Dealer has to drink!"
                # If the guesser guesses correctly on the second attempt, the dealer has to drink two drinks. The missed_guesses number for the dealer also gets reset to 0.
                game.players[game.dealer].imbibed += 2
                game.players[game.dealer].missed_guesses = 0

                game.guesser = self.move_guesser_index(game.guesser, game.dealer)
            else:
                if self.verbose:
                    print "Player has to drink!"
                # If the player doesn't guess correctly then they have to drink an amount equal to the difference in face value between their guess and the card on the top of the deck.
                game.players[game.guesser].imbibed += abs((self.face_to_int(second_guess)) - self.face_to_int(top_card[:-1]))
                game.players[game.dealer].missed_guesses += 1

                game.guesser = self.move_guesser_index(game.guesser, game.dealer)

                if game.players[game.dealer].not_dealer():
                    game.dealer = self.move_index(game.dealer)
        else:
            if self.verbose:
                print "The top card is higher than what the player guessed"
            # Same logic as above, only the random guess is now going to be in the range of the index of the first guess and one less than the length of the FACE_VALUES list
            second_guess = game.FACE_VALUES[randrange(index_of_first_guess, len(game.FACE_VALUES))]

            # If the guesser is playing smart then we need to change our guess
            if game.players[game.guesser].playing_smart:
                second_guess = self.play_smart(False, first_guess, True)

            if self.verbose:
                print "Second guess is a " + second_guess

            game.table.insert(0, top_card)

            if (second_guess) == self.face_to_int(top_card[:-1]):
                if self.verbose:
                    print "Dealer has to drink!"
                # If the guesser guesses correctly on the second attempt, the dealer has to drink two drinks. The missed_guesses number for the dealer also gets reset to 0.
                game.players[game.dealer].imbibed += 2
                game.players[game.dealer].missed_guesses = 0
                game.guesser = self.move_guesser_index(game.guesser, game.dealer)
            else:
                if self.verbose:
                    print "Player has to drink!"
                # If the player doesn't guess correctly then they have to drink an amount equal to the difference in face value between their guess and the card on the top of the deck.
                game.players[game.guesser].imbibed += abs((self.face_to_int(second_guess)) - self.face_to_int(top_card[:-1]))
                game.players[game.dealer].missed_guesses += 1

                game.guesser = self.move_guesser_index(game.guesser, game.dealer)

                if game.players[game.dealer].not_dealer():
                    game.dealer = self.move_index(game.dealer)






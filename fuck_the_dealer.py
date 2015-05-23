# Play a game of Fuck the Dealer with the Deck class that exists in this directory
from deck import Deck
from random import randrange
from player import Player

FACE_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']

class Game:

    def __init__(self):
        # Face values in a list that will facilitate guessing
        self.FACE_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']
        self.main_deck = Deck().deck
        self.table = []

# To simulate the amount that each player would have to drink, I'll assume that each "drink" of beer would be 1 oz.
# The game will be simulated with 6 players
        player_one = Player()
        player_two = Player()
        player_three = Player()
        player_four = Player()
        player_five = Player()
        player_six = Player()

        # player_one will be playing smart!
        player_one.playing_smart = True

        self.players = [player_one, player_two, player_three, player_four, player_five, player_six]
# Make the first player the dealer. The dealer variable stores the index of the current dealer. The guesser variable stores the index of the player who is currently guessing the card
        self.dealer = 0
        self.guesser = 1

def face_to_int(face_value):
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
def move_index(index):
    if index < 5:
        index += 1
    else:
        index = 0
    return index

def move_guesser_index(g_index, d_index):
    if g_index < 5:
        g_index += 1
        if g_index == d_index and g_index != 5:
            g_index += 1
        if g_index == d_index and g_index == 5:
            g_index = 0
    else:
        g_index = 0
        if g_index == d_index:
            g_index += 1
    return g_index

# The following method will be define how a player can play "smart" instead of random.
# This means that the player will choose the card with the highest probability of being correct. In theory, this should
# ensure that the player drinks the least amount out of all the other players if those players
# playing randomly.

def play_smart(main_deck, table, first, first_guess, higher):
    # Get the necessary numbers for making the smartest guess.
    remaining_cards = 52 - len(table)
    cards_left = {
            '2': 4.0,
            '3': 4.0,
            '4': 4.0,
            '5': 4.0,
            '6': 4.0,
            '7': 4.0,
            '8': 4.0,
            '9': 4.0,
            '10': 4.0,
            'j': 4.0,
            'q': 4.0,
            'k': 4.0,
            'a': 4.0
    }
    for card in table:
        # This loop will find the amount of remaining cards for each face value left in the deck
        cards_left[card[:-1]] -= 1

    if first:
        # The first guess should be made by factoring the probability of three things for each card
        # 1. The probability of the card being the top card
        # 2. The summed probability of the cards with a higher face value being the top card
        # 3. The summed probability of the cards with a lower face value being the top card
        expected_value = {
                '2': 0.0,
                '3': 0.0,
                '4': 0.0,
                '5': 0.0,
                '6': 0.0,
                '7': 0.0,
                '8': 0.0,
                '9': 0.0,
                '10': 0.0,
                'j': 0.0,
                'q': 0.0,
                'k': 0.0,
                'a': 0.0
        }

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
        print expected_value
        print "returning..." + best_guess
        return best_guess
    else:
        # The second guess should be made by choosing the card with the highest probability
        expected_value = {
                '2': 0.0,
                '3': 0.0,
                '4': 0.0,
                '5': 0.0,
                '6': 0.0,
                '7': 0.0,
                '8': 0.0,
                '9': 0.0,
                '10': 0.0,
                'j': 0.0,
                'q': 0.0,
                'k': 0.0,
                'a': 0.0
        }

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

        print expected_value
        print "returning..." + best_guess
        return best_guess

def turn(game):
    # We are going to want to .pop() the first card in the deck everytime
    # because the cards are always taken out of the deck regardless of
    # whether or not the card has been guessed correctly.
    index_of_first_guess = randrange(len(game.FACE_VALUES))
    first_guess = game.FACE_VALUES[index_of_first_guess]

    # If the guesser is playing smart then we just change the guess
    if game.players[game.guesser].playing_smart:
        first_guess = play_smart(game.main_deck, game.table, True, None, False)
        index_of_first_guess = game.FACE_VALUES.index(first_guess)

    print "First guess is a " + first_guess

    # The first card in the deck is going to get removed from the main deck
    # on every turn.
    top_card = game.main_deck.pop(0)

    if first_guess == top_card[:-1]:
        print "The first guess was correct!"
        # In the event that the first guess is correct, the dealer has to drink 4 drinks
        game.players[game.dealer].imbibed += 4

        # Simulates placing the top card onto the table
        game.table.insert(0, top_card)

        game.guesser = move_guesser_index(game.guesser, game.dealer)

    elif face_to_int(first_guess) > face_to_int(top_card[:-1]):
        print "The top card is lower than what the player guessed"
        # Now the player will randomly guess a face value between the first guess
        # and the lower end of the face values
        second_guess = game.FACE_VALUES[randrange(index_of_first_guess)]

        # If the guesser is playing smart then we need to change our guess
        if game.players[game.guesser].playing_smart:
            second_guess = play_smart(game.main_deck, game.table, False, first_guess, False)

        print "Second guess is a " + second_guess

        game.table.insert(0, top_card)
        # Two options now, the second guess was correct and the dealer has to
        # drink, or the second guess wasn't correct and the dealer gets a pass
        if second_guess == top_card[:-1]:
            print "Dealer has to drink!"
            # If the guesser guesses correctly on the second attempt, the dealer has to drink two drinks. The missed_guesses number for the dealer also gets reset to 0.
            game.players[game.dealer].imbibed += 2
            game.players[game.dealer].missed_guesses = 0

            game.guesser = move_guesser_index(game.guesser, game.dealer)
        else:
            print "Player has to drink!"
            # If the player doesn't guess correctly then they have to drink an amount equal to the difference in face value between their guess and the card on the top of the deck.
            game.players[game.guesser].imbibed += abs(face_to_int(second_guess) - face_to_int(top_card[:-1]))
            game.players[game.dealer].missed_guesses += 1

            game.guesser = move_guesser_index(game.guesser, game.dealer)

            if game.players[game.dealer].not_dealer():
                game.dealer = move_index(game.dealer)
    else:
        print "The top card is higher than what the player guessed"
        # Same logic as above, only the random guess is now going to be in the range of the index of the first guess and one less than the length of the FACE_VALUES list
        second_guess = game.FACE_VALUES[randrange(index_of_first_guess, len(game.FACE_VALUES))]

        # If the guesser is playing smart then we need to change our guess
        if game.players[game.guesser].playing_smart:
            second_guess = play_smart(game.main_deck, game.table, False, first_guess, True)

        print "Second guess is a " + second_guess

        game.table.insert(0, top_card)

        if face_to_int(second_guess) == face_to_int(top_card[:-1]):
            print "Dealer has to drink!"
            # If the guesser guesses correctly on the second attempt, the dealer has to drink two drinks. The missed_guesses number for the dealer also gets reset to 0.
            game.players[game.dealer].imbibed += 2
            game.players[game.dealer].missed_guesses = 0
            game.guesser = move_guesser_index(game.guesser, game.dealer)
        else:
            print "Player has to drink!"
            # If the player doesn't guess correctly then they have to drink an amount equal to the difference in face value between their guess and the card on the top of the deck.
            game.players[game.guesser].imbibed += abs(face_to_int(second_guess) - face_to_int(top_card[:-1]))
            game.players[game.dealer].missed_guesses += 1

            game.guesser = move_guesser_index(game.guesser, game.dealer)

            if game.players[game.dealer].not_dealer():
                game.dealer = move_index(game.dealer)


#print "Starting the game....\n"
#    game = Game()
#    while len(game.main_deck) != 0:
#        print "\nHere's the main deck"
#        print ', '.join(game.main_deck)
#        print "Dealer is currently " + str(game.dealer)
#        print "Guesser is currently " + str(game.guesser)
#        for i in range(6):
#            print "Player " + str(i) + " has drunk " + str(game.players[i].imbibed) + " drinks."
#        turn(game)
#        print "Table deck now has"
#        print ', '.join(game.table)
#        print "Main deck now has"
#        print ', '.join(game.main_deck)

# Uncomment the code above if you'd like to see a printout of every single game.
# Well simulate 10,000 games to see how often the smart player drinks the least.

wins = 0.0
drinks = [0, 0, 0, 0, 0, 0]
for i in range(10000):
    game = Game()
    while len(game.main_deck) != 0:
        turn(game)

    smart_player_drinks = game.players[0].imbibed
    least_drinks = True
    for player in game.players:
        if player.imbibed < smart_player_drinks:
            least_drinks = False
    for i in range(len(game.players)):
        drinks[i] += game.players[i].imbibed

    if least_drinks:
        wins += 1.0

    print "new game\n"

print "The smart player won " + str((wins / 10000) * 100) + "% of the time"
print drinks




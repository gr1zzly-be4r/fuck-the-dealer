# fuck-the-dealer
Simulates playing a game of fuck the dealer with "smart" and "random" players.

Instructions for playing the game can be found [here](http://www.drinkinggames.com/game.php/21/fuck+the+dealer).

Run the game by cloning the repo and running

`python main.py num_players num_rounds [--verbose]`

Specifying the `--verbose` option will result in a print out of a summary for each round in every game that you simulate. It will print out a lot. You can run the game over as many different values for the number of players and number of rounds in the allowable ranges, and you should see that the "smart" player will have the least amount of total drinks over all of the rounds.

You can verify this by looking at the final print out of the program. `main.py` will print out a list showing the amount of drinks that each player has drunk over all of the games that you've simulated. So an output like:

`[100, 200, 200]`

would mean that the 0th player -- the smart player -- would have drank 100 oz. of whatever drink these imaginary players are playing with over all of the games. 

Here are some example results that I've gotten when running the program:

`python main.py 4 100000` yields:

`[2312292, 4229665, 4310160, 4315151]`

`python main.py 6 1000` yields:

`[18125, 27308, 27720, 26537, 26353, 26354]`

`python main.py 8 10000 yields` yields:

`[162708, 225095, 207257, 195392, 190523, 189216, 192967, 191476]`



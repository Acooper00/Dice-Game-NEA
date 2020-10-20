# Dice-Game-NEA
A dice game created for my computer science GCSE (exam date 08/2019)

Before playing each user must enter a valid name. The valid names are displayed in /FILES/Players.txt.
In the 'Settings' menu the user may upload a config file. These are stored in /FILES/CONFIG/ and when prompted the name should be given without the '.cfg' file extension.

The rules of the game are:

The players roll two 6-sided dice each and get points depending on what they
roll. There are 5 rounds in a game. In each round, each player rolls the two dice.
• The points rolled on each player’s dice are added to their score.
• If the total is an even number, an additional 10 points are added to their score.
• If the total is an odd number, 5 points are subtracted from their score.
• If they roll a double, they get to roll one extra die and get the number of points rolled added to
their score.
• The score of a player cannot go below 0 at any point.
• The person with the highest score at the end of the 5 rounds wins.
• If both players have the same score at the end of the 5 rounds, they each roll 1 die and
whoever gets the highest score wins (this repeats until someone wins).

# Battleship
"""
This is the game of Battleship, where the computer puts some ships somewhere in the ocean. You can then shoot and try to hit the ships.
If you hit all parts of a ship, it is sunk! Try to sink all the enemy ships before you run out of ammo :)

First, you can choose a level (the size of the ocean)
Then, the ocean (='board') is created, as a 2D list (a list of lists)
The computer generates some random ships in the ocean, making sure they fit on the board and don't overlap with each other.
Then, the game starts!
You choose a coordinate to shoot, the game checks if it's a legal shot, and in case you hit a ship, the board is updated.
If you hit a ship part, but the ship is not completely destroyed, a 'H' is shown (for 'hit')
If a ship is completely sunk, an 'S' is shown at all its coordinates (for 'sunk')
This continues until you run out of turns, or all the ships are sunk :)
"""


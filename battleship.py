# -*- coding: cp1252 -*-
from random import randint
import re
import copy

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

def main():
    print("Hello! Welcome to the game of Battleship!!")

    play = True
    while play:
        play_Battleship()
        play = ask_new_game()

    print("Goodbye! Thanks for playing Battleship!!")


def ask_new_game():
    # ask for another game
    yn = input("Do you want to play some more? \n")
    yn = yn.lower()
    yn = re.sub(r'([^\s\w]|_)+', '', yn)  # keep only alphabetical characters (thanks google :D)
    yesses = ["y", "yes", "ye", "yeah", "yea", "sure", "of course"]
    if yn in yesses:
        keep_playing = True
    else:
        keep_playing = False
    return keep_playing


def play_Battleship():
    # define the ships in the game
    # -> list of names
    # -> list of sizes (lengths) of those ships
    ship_names_list = ["this ship doesn't exist", "this ship doesn't exist", "Destroyer", "Cruiser", "Aircraft Carrier",
                       "Battleship"]  # used to tell the player what kind of ship they sunk.
    ship_sizes_list = [2, 2, 3, 3, 4, 5]  # list of the shipsizes to use

    # I only tested the game till lvl 3, but it's perfectly expandable. You might have to change the number of tries/ships
    print(
        'Welcome to Battleship! There are three sizes of the game: one, two or three. Higher level ships are bigger too!')
    lvl = -1
    while lvl > 3 or lvl < 1:
        lvl = int(input("Not an existing lvl. Which lvl do you choose? 1,2 or 3?\n"))

    # set difficulty based on level chosen
    nb_ships = lvl + 1
    size_x = lvl + 4
    size_y = lvl + 4
    maxturns = int(8 + 4 * lvl ** 1.5)  # formula determined through testing

    # create the board
    board = create_board(size_y, size_x)  # 2D list (= matrix)
    board_height = len(board)  # number of rows
    board_width = len(board[0])  # number of columns

    # create the ships
    # how it works: list of ships. Each ship is a list of coordinates.
    #               If you fire, search through the ship_list and if the fired coorindate is in ships_left, remove it (so that part of the ship is destroyed).
    #               If all coordinates of a ship are gone (its list is empty), the ship is destroyed!
    # ships_left keeps track of which parts of which ships have already been hit.
    ships_left = []
    for i in range(0, nb_ships):
        # we need to pass ships_left, to make sure we don't put ships in places where there's already another ship!
        # also the board, because a ship has to completely fit inside the board
        ship = create_ship(ship_sizes_list[i], board, ships_left)
        ships_left.append(ship)
    nb_ships_left = len(ships_left)

    # make a copy so even after all ships are destroyed, we still know where they started (eg so we can display the not found ships)
    ships_original_location = copy.deepcopy(ships_left)

    ############################
    ####### LET'S PLAY! ########
    ############################
    print("Let's play Battleship!")

    turn = 0
    while turn < maxturns and nb_ships_left > 0:

        # 1. Graphics & info for player
        print('----------------------------------------')
        print_board(board)

        if nb_ships_left == 1:
            print("There is ", nb_ships_left, "ship left")
        else:
            print("There are ", nb_ships_left, "ships left")

        print("This is shot number ", turn + 1)  # +1 to show the 'logical' number (so "turn 1" instead of "turn 0")

        # show how many shots are left
        if maxturns - turn == 1:
            print("You have ", maxturns - turn, " shot left")
        else:
            print("You have ", maxturns - turn, " shots left")

        # enter target coordinates for the new shot
        # coordinates are a bit annoying to work with. For users, starting at '1' is logical. But the computer starts at '0'. So we need to do some conversion.
        #   for X: we have to do -1 to use the 'logical', not 'computer' number as input (so '1' instead of '0'). We want the axis to start at 1, not at 0
        #   for Y: board_height - y. Y-axis is downward because of how we contstructed the board 2D list... This feels weird to the player, we want to have a Y-axis pointing upward!
        guess_x = int(input("Enter X-coordinates to hit:")) - 1
        guess_y = board_height - int(input("Enter Y-coordinates to hit:"))
        print("\n")

        # 2. Process the input
        #    options:   a) shot not inside the board    -> tell user and give another shot (:D)
        #               b) shot same as previous shot   -> tell user and give another shot (:D)
        #               c) shot hits a ship             -> process shot, update board, check if ship completely destroyed, tell user
        #               d) shot was a miss              -> update board, tell user
        # first y, then x because the height is the y-th sublist of 'board'
        # 2.a) check if shot is out of bounds
        if (guess_y < 0 or guess_y >= board_height) or (guess_x < 0 or guess_x >= board_width):
            print("Oops, that's not even in the ocean. Try again.\n")
            continue # continue goes back to where the while started -> start new turn

        # 2.b) if already guessed, hit or sunk
        elif board[guess_y][guess_x] != 'O': # or board[guess_y][guess_x] == "H" or board[guess_y][guess_x] == "S"):
            print("You guessed that one already. Try again\n")
            continue

        # 2.c) check if shot hits a ship
        elif (occupied_by_other_ship([guess_y, guess_x], ships_left)):

            print("Congratulations! You hit a ship!\n")
            board[guess_y][guess_x] = "H" # show a 'H' to the player, because it was a hit

            # find out which ship was hit, sink its coordinate (=remove from ships_left list), and see if whole ship is destroyed now
            i = 0
            while i < nb_ships:
                # is the i'th ship damaged?
                if [guess_y, guess_x] in ships_left[i]:
                    # delete this ship coordinate from the list of this ship's intact parts
                    ships_left[i].remove([guess_y, guess_x])

                    # if the ship has no intact parts left, it is completely sunk
                    if len(ships_left[i]) == 0:
                        print("You sunk my ship of class ", ship_names_list[ship_sizes_list[i]], "!!!\n")
                        nb_ships_left -= 1
                        for sunken_shippart in ships_original_location[i]:
                            board[sunken_shippart[0]][
                                sunken_shippart[1]] = "S"  # show 'S' at all coordinates of the sunken ship
                    break  # the ship has been found, so we don't need to search further. exit the while loop
                i += 1

        # 2.d) not outside board, not already guessed, and not hit -> this is a miss
        else:
            print("You missed my battleship!" "\n")
            board[guess_y][guess_x] = "X"

        # we've processed the shot, so this turn is over
        turn += 1

    # all turns are used up or nb_ships_left==0, so the game ended
    if nb_ships_left <= 0:
        print("\n Congratulations!! You destroyed all of my ships!")
    else:
        print("Oooh, you lost!!")

        # print ships that were not found
        print("The ships that are left(M) were at the following positions: ")
        for ship in ships_left:
            for shippart in ship:
                board[shippart[0]][shippart[1]] = "M"

    # print final state of the ocean
    print("\n")
    print_board(board)
    print("\n")


# CREATING THE BOARD
# first y because the height is the y-th sublist of board. x is the position in that sublist.
def create_board(size_y, size_x):
    board = []
    for y in range(size_y):
        board.append(["O"] * size_x)
    return board


def print_board(board):
    # print all rows, add spaces in between the coordinates (looks nicer)
    for row in board:
        print(" ".join(row))
    print("\n")


# CREATING THE SHIPS -> generate random (integer) numbers for the coordinates
def random_y(board):
    return randint(0, len(board) - 1)

def random_x(board):
    return randint(0, len(board[0]) - 1)


def check_next_to_shippart(pos, shipparts):  # shipparts is the list of coordinates of this ship
    is_next_to_ship = False
    for part in shipparts:  # check if any any of the neighbouring squares to pos is part of a ship
        if (((part[0] + 1 == pos[0] or part[0] - 1 == pos[0]) and (part[1] == pos[1])) or (
                (part[0] == pos[0]) and (part[1] + 1 == pos[1] or part[1] - 1 == pos[1]))):
            is_next_to_ship = True
    return is_next_to_ship


def in_line_with_ship(pos, shipparts):  # asserts if the part is on a straight line with the other shipparts

    if len(shipparts) > 1:
        if shipparts[0][0] == shipparts[1][0] and pos[0] == shipparts[0][0]:  # in line horizontally
            in_line = 1
        elif shipparts[0][1] == shipparts[1][1] and pos[1] == shipparts[0][1]:  # in line vertically
            in_line = 1
        else:
            in_line = 0
    else:
        if pos[0] == shipparts[0][0] or pos[1] == shipparts[0][1]:  # same x or y as the first shippart
            in_line = 1

    if check_next_to_shippart(pos, shipparts) and in_line == 1:
        return 1
    else:
        return 0


def occupied_by_other_ship(pos, ships_left):  # asserts if the space has already been taken by a part of another ship
    occupied = 0
    for i in range(len(ships_left)):
        if pos in ships_left[i]:
            occupied = 1
    return occupied


def create_ship(size, board, ships_left):
    tries = 0
    board_height = len(board)
    board_width = len(board[1])
    ship_coordinates = []

    ship_coordinates.append([random_y(board), random_x(board)])
    while (occupied_by_other_ship(ship_coordinates[-1], ships_left)):  # make sure the first part of the ship is well positioned
        ship_coordinates[0] = [random_y(board), random_x(board)]

    i = 1
    while i < size:
        # make sure all of the other shipparts are in line with the previous ones and not already occupied
        ship_coordinates.append([random_y(board), random_x(board)])
        while (occupied_by_other_ship(ship_coordinates[-1], ships_left)) \
                or (ship_coordinates[-1] in ship_coordinates[:-1]) \
                or (not in_line_with_ship(ship_coordinates[-1], ship_coordinates)):
            ship_coordinates[-1] = [random_y(board), random_x(board)]
            tries += 1
            if tries > 100:  # if too many tries, there is no good position left for the part. try with a new first coordinate (see 'if' underneath)
                break

        if tries >= 100:  # infinite loop due to bad positioning of the first ship section, try to start this ship at another place. (Very rarely, an infinite loop still occurs when the positioning of all the previous ships just doesn't allow the placement of the new ship.)
            tries = 0
            i = 0
            ship_coordinates = []
            ship_coordinates.append([random_y(board), random_x(board)])
            while (occupied_by_other_ship(ship_coordinates[-1], ships_left)):
                ship_coordinates[0] = [random_y(board), random_x(board)]
        i += 1

    return ship_coordinates

if __name__ == "__main__":
    main()

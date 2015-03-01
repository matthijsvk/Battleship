# -*- coding: cp1252 -*-
from random import randint
import re
import copy

def play_Battleship():
    ship_names_list=["this ship doesn't exist","this ship doesn't exist","Destroyer","Cruiser","Aircraft Carrier","Battleship"] #used to tell the player what kind of ship they sunk.
    ship_sizes_list=[2,2,3,3,4,5] #list of the shipsizes to use
    
    print('Welcome to Battleship! There are three sizes of the game: one, two or three. Higher level ships are bigger too!')
    lvl= int(input("Which lvl do you choose? 1,2 or 3?\n")) #I only tested the game till lvl 3, but it's perfectly expandable. You might have to change the number of tries/ships
    
    while lvl>3 or lvl<1:
        lvl= int(input("Not an existing lvl. Which lvl do you choose? 1,2 or 3?\n"))

    nb_ships = lvl+1
    size_x= lvl+4
    size_y= lvl+4
    maxturns = int(8+4*lvl**1.5) #determined through testing
    
    #create the board
    board = create_board(size_y,size_x)
    board_height=len(board)#number of rows
    board_width=len(board[0])#number of columns
    
    #create the ships
    ships_left=[] #keeps track of which parts of which ships have already been hit. if one of its sublists gets empty, a ship has been fully destroyed.
    for i in range(0,nb_ships):
        ship= create_ship(ship_sizes_list[i],board,ships_left)
        ships_left.append(ship)
        
    nb_ships_left= len(ships_left)
    ships_localization= copy.deepcopy(ships_left)  #  make a copy to be able to display the sunken ships afterward
    

    #######LET'S PLAY!########
    print ("Let's play Battleship!")
    
    turn=0
    while turn< maxturns and nb_ships_left>0:

        #graphics & info for player
        print ('----------------------------------------')
        print_board(board)
        
        if nb_ships_left==1:
            print( "There is ",nb_ships_left, "ship left")
        else:
            print( "There are ",nb_ships_left, "ships left")

        print( "This is shot number ",turn+1) #+1 to show the 'logical' number (so "turn 1" instead of "turn 0")
        if maxturns-turn==1:
            print ("You have ", maxturns-turn," shot left")
        else: print ("You have ", maxturns-turn," shots left")

        #entering target coordinates
        guess_x = int(input("Enter X-coordinates to hit:"))-1 #-1 to use the 'logical' number as input (so '1' instead of '0')
        guess_y = board_height- int(input("Enter Y-coordinates to hit:")) #board_height- to have a Y-axis pointing upward
        print("\n")

        #process the input
        if (occupied_by_other_ship([guess_y,guess_x],ships_left)): #first y, then x because the height is the y-th sublist of 'board'
            
            print ("Congratulations! You hit my ship!\n")
            board[guess_y][guess_x]="H"
            
            i=0
            while i < nb_ships: 
                if [guess_y,guess_x] in ships_left[i]:      #see which ship has been damaged
                    ships_left[i].remove([guess_y,guess_x]) #and delete this ship section from the list of this ship's intact parts
                    
                    if len(ships_left[i])==0:#if the ship has no intact parts left
                        print ("You sunk my ship of class ",ship_names_list[ship_sizes_list[i]],"!!!\n")
                        nb_ships_left-=1
                        for sunken_shippart in ships_localization[i]:
                            board[sunken_shippart[0]][sunken_shippart[1]]="S" #show 'S' at coordinates of the sunken ship
                    break #the ship has been found
                i+=1
                
            turn+=1
            
        else:
            #if guess is out of bounds
            if (guess_y < 0 or guess_y >= board_height) or (guess_x < 0 or guess_x >= board_width): 
              print ("Oops, that's not even in the ocean.\n")
            #if already guessed, hit or sunk
            elif(board[guess_y][guess_x] == "X" or board[guess_y][guess_x]== "H" or board[guess_y][guess_x]== "S"): 
                print ("You guessed that one already.\n")
            else:
                print( "You missed my battleship!" "\n")
                board[guess_y][guess_x] = "X"
                turn+=1
                
    #the game ended, you lost            
    if turn >= maxturns and nb_ships_left>0:
        print( "Oooh, you lost!!")
        print ("The ships that are left(M) were at the following positions: ")  #print ships that were not found
        for ship in ships_left:
            for shippart in ship:
                board[shippart[0]][shippart[1]]= "M"
                shippart[0]= board_height-shippart[0]
                shippart[1]= shippart[1] +1
##        for ship in ships_left:   #debug purposes
##            if len(ship)> 0:
##                for shippart in ship:
##                    temp= shippart[0]
##                    shippart[0]=shippart[1]
##                    shippart[1]= temp
##                print ship

    #the game ended, you won
    if nb_ships_left==0:
        print( "\n Congratulations!! You destroyed all of my ships!")

    print( "\n")
    print_board(board)
    
    #ask for another game    
    yn=input("Do you want to play some more? \n")
    yn=yn.lower()
    yn=re.sub(r'([^\s\w]|_)+', '', yn) #keep only alphabetical characters
    yesses=["y","yes","ye","yeah","yea","sure","of course"]
    
    if yn in yesses:
        print( "\n")
        play_Battleship()
    else:
        print( "Goodbye then! Thanks for playing Battleship!!")


#CREATING THE BOARD
def create_board(size_y,size_x): #first y because the height is the y-th sublist of board. x is the position in that sublist.
    board=[]
    for y in range(size_y):
        board.append(["O"] * size_x)
    return board
    
def print_board(board):
    for row in board:
        print( " ".join(row))
    print( "\n")

#CREATING THE SHIPS
def random_y(board):
    return randint(0, len(board) - 1)

def random_x(board):
    return randint(0, len(board[0]) - 1)
        
def next_to_shippart(pos, shipparts): #shipparts is the list of coordinates of this ship
    is_next_to_ship=0
    for part in shipparts: #check if any any of the neighbouring squares to pos is part of a ship
        if (( (part[0]+1==pos[0] or part[0]-1==pos[0]) and (part[1]==pos[1]) ) or ( (part[0]==pos[0]) and (part[1]+1==pos[1] or part[1]-1==pos[1]) )):
            is_next_to_ship=1
    return is_next_to_ship

def in_line_with_ship(pos,shipparts): #asserts if the part is on a straight line with the other shipparts
    
    if len(shipparts)>1:
        if shipparts[0][0]==shipparts[1][0] and pos[0]==shipparts[0][0]:  #in line horizontally     
            in_line=1
        elif shipparts[0][1]==shipparts[1][1] and pos[1]==shipparts[0][1]:#in line vertically     
            in_line=1
        else:
            in_line=0
    else:
        if pos[0]==shipparts[0][0] or pos[1]==shipparts[0][1]: #same x or y as the first shippart
            in_line=1 
        
    if next_to_shippart(pos,shipparts) and in_line==1:
        return 1
    else:
        return 0

def occupied_by_other_ship(pos,ships_left): #asserts if the space has already been taken by a part of another ship
    occupied=0
    for i in range(len(ships_left)):
        if pos in ships_left[i]:
            occupied=1
    return occupied    
            

def create_ship(size,board,ships_left):
    tries=0
    board_height = len(board)
    board_width = len(board[1])
    ship_coordinates =[]
    
    ship_coordinates.append([random_y(board),random_x(board)])
    while (occupied_by_other_ship(ship_coordinates[-1],ships_left)): #make sure the first part of the ship is well positioned
            ship_coordinates[0]=[random_y(board),random_x(board)]
            
    i=1
    while i < size:
        
        ship_coordinates.append([random_y(board),random_x(board)]) #make sure all of the other shipparts are in line with the previous ones and not already occupied
        while (occupied_by_other_ship(ship_coordinates[-1],ships_left)) or (ship_coordinates[-1] in ship_coordinates[:-1]) or (not in_line_with_ship(ship_coordinates[-1],ship_coordinates)):
            ship_coordinates[-1]= [random_y(board),random_x(board)]
            tries +=1
            if tries >100: #if too many tries, there is no good position left for the part. try with a new first coordinate (see 'if' underneath)
                break
            
        if tries >=100:#infinite loop due to bad positioning of the first ship section, try to start this ship at another place. (Very rarely, an infinite loop still occurs when the positioning of all the previous ships just doesn't allow the placement of the new ship.)
            tries=0
            i=0
            ship_coordinates=[]
            ship_coordinates.append([random_y(board),random_x(board)])
            while (occupied_by_other_ship(ship_coordinates[-1],ships_left)): 
                ship_coordinates[0]=[random_y(board),random_x(board)]
        i += 1
        
    return ship_coordinates

play_Battleship()#start the game the first time

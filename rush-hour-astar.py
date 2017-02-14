#! /usr/bin/env python
"""
support code for the rush-hour game


ASSUMPTIONS
 1. game file is formatted correctly
 2. goal is always in the 3rd row
 3. empty positions are indicated by '0'

INITIALIZATION
  LOAD-GAME:  Load a game from a file, and create a game instance
  to record all of the information.  
"""
import copy

class State():
	
	def __init__(self, current_game, before):
		self.game = current_game
		self.donemoves = before	
		self.cost = len(self.donemoves)

def load_game(filename):
    """Reads filename and returns a list representing the initial state of the game.
    Code is fragile -- assumes dimensions on first line are correct"""
    fin = open(filename)
    nextline = fin.readline()
    maxX, maxY = [int(token) for token in nextline.split()]
    gameArray = []
    for i in range(maxX):
        nextline = fin.readline()
        gameArray.append(nextline.split())
    fin.close()
    return gameArray

# UTILITIES
# PRINT_BOARD: nicely formats a game board
def print_board(board):
    """pretty print the board"""
    for i in board:
        for j in i:
            print j.rjust(4),
        print

# COPY_GAME: lists are mutable in python. sometimes a full copy is needed of a board
def copy_game(alist):
    """alist should be a 2D matrix representing a game state. returns a copy of the game state"""
    newlist = []
    for row in range(len(alist)):
        newlist = newlist + [list(alist[row])]
    return newlist

# EQUAL_GAMES: returns True if two game boards have the same values at all the positions
def equal_games(game1, game2):
    """games are board states, returns True if two game boards have the same values at all the positions"""
    # do they have the same number of rows?
    if len(game1) == len(game2):
        for i in range(len(game1)):
            # do they have the same number of columns?
            if len(game1[i]) == len(game2[i]):
                for j in range(len(game1[i])):
                    # as soon as a position has a different value, they are not equal
                    if game1[i][j] != game2[i][j]:
                        return False
        return True
    else:
        return False

# LEGAL_POSITION: returns True if x y position on the board exists
def legal_position(board, x, y):
    """returns True if (x, y) is on the board""" 
    return x >= 0 and y >= 0 and x < len(board) and y < len(board[0])

# EMPTY: check to see if an x y position on the board exists and is empty
#        returns True or False
def empty(board, x, y):
    """returns True if the (x, y) position on the board is empty"""
    if legal_position(board, x, y):
        if board[x][y] == '0':
            return True
    return False

# AT_GOAL: checks whether a board is actually at the goal state
#          i.e., g is at the rightmost column
def at_goal(board):
    """returns True if goal is in the rightmost column"""
    for row in range(len(board)):
	
        if board[row][len(board[2]) - 1] == 'g':
            return True
    return False

def possible_move(game, row, column):
	length = 0
	move = ()
	flag = False
	if row+1 ==len(game):
		flag = True
	if row == 0:
		flag = True
	if column+1 == len(game[0]):
		flag = True
	if column == 0:
		flag = True
	if empty(game, row-1, column) == False and legal_position(game, row-1, column) == True:	
		if game[row][column] in game[row-1][column]:

			if 't' in game[row][column]:
				length = 3 
			else:
				length = 2
			
			if legal_position(game,row+1,column) == True:

					if not game[row-1][column] == game[row+1][column]:
						if empty(game,row-length,column) == True:
							move = (row,column,0)
							return move
			else:
                                        if empty(game,row-length,column) == True:
                                                        move = (row,column,0)
                                                        return move


	if empty(game, row, column+1) == False and legal_position(game, row, column+1) == True:
        	if game[row][column] in game[row][column+1]:
                	if 't' in game[row][column]:
                        	length = 3
                	else:
                        	length = 2
                        
			if legal_position(game,row,column-1) == True:	
					if not game[row][column-1] ==  game[row][column+1]:
		                		if empty(game,row,column+length) == True:
                		        		move = (row,column,1)
							return move
                        else:
                                        if empty(game,row,column+length) == True:
                                                        move = (row,column,1)
                                                        return move
			
                        
	if empty(game,row+1,column) == False and legal_position(game, row+1, column) == True:
		if game[row][column] in game[row+1][column]:

			if 't' in game[row][column]:
				length = 3
			else:
				length = 2
		
			if legal_position(game, row-1, column) ==True:
                                	if game[row-1][column] not in game[row+1][column]:
						if empty(game,row+length,column) == True:
							move = (row, column, 2)
							return move
                        else:
                                        if empty(game,row+length,column) == True:
                                                        move = (row,column,2)
                                                        return move 
		
	if empty(game,row,column-1) == False and legal_position(game, row, column-1) == True:
		
        	if game[row][column-1] in  game[row][column]:

	
			if 't' in game[row][column]:
				length = 3
			else:
				length = 2
                        
			if legal_position(game,row,column+1) == True:
                                	if game[row][column-1] not in game[row][column+1]:
						if empty(game,row,column-length) == True:
							move = (row, column, 3)
        						return move
                        else:
                                        if empty(game,row,column-length) == True:
                                                        move = (row,column,3)
                                                        return move
			

       

def move_up(game, row, column):
	length = 0
	tempgame= copy_game(game.game)
	if 't' in game.game[row][column]:
		length = 3
	else:
		length = 2
	
	if empty(game.game, row-length, column):
		piece = tempgame[row][column]
		tempgame[row][column] = '0'
		tempgame[row-length][column] = piece
	return tempgame

def move_down(game, row, column):
        length = 0
        tempgame = copy_game(game.game)

        if 't' in game.game[row][column]:
                length = 3
        else:
                length = 2
				
	if empty(game.game,row+length,column):
        	piece = tempgame[row][column]
        	tempgame[row][column] = '0'
        	tempgame[row+length][column] = piece
		
        return tempgame


def move_right(game, row, column):
        length = 0
	
        tempgame = copy_game(game.game)

        if 't' in game.game[row][column]:
                length = 3
        else:
                length = 2
	
	if empty(game.game,row,column+length):
        	piece= tempgame[row][column]
        	tempgame[row][column] = '0'
        	tempgame[row][column+length] = piece

        return tempgame


def move_left(game, row, column):
        length = 0
	tempgame = copy_game(game.game)
        if 't' in game.game[row][column]:
                length = 3
        else:
                length = 2

	if empty(game.game,row,column-length):
        	piece = tempgame[row][column]
        	tempgame[row][column] = '0'
        	tempgame[row][column-length] = piece
	
        return tempgame

def ids(game,maxLimit):

	salt = 0
	p_moves= []
	state = game
      	if at_goal(game.game):
		salt = salt + 1
	

		return game
	else:
		salt = salt + 1
	if maxLimit == 0:
		return game

        for k in range (0,len(game.game)):
                for l in range (0,len(game.game[0])):
                        if game.game[k][l] != '0':
                                if not possible_move(game.game,k,l) == None:
                                        p_moves.append(possible_move(game.game,k,l))
        
	for a in p_moves:
                moves = []
		flag = False
                for g in game.donemoves:
                        moves.append(list(g))
                if a[2] == 0:
                        new_game = move_up(game,a[0],a[1])
                        moves.append(list(a))
                        new_state = State(new_game,moves)


                        for i in unexploredstates:
                                if equal_games(i.game, new_state.game) == True:
                                                flag = True

                        if flag == False:
                                        unexploredstates.append(new_state)
                                        state = ids(new_state, maxLimit-1)
					if at_goal(state.game):
						return state
					
                if a[2] == 1:
			
                        new_game = move_right(game,a[0],a[1])
                        moves.append(list(a))
			
                        new_state = State(new_game,moves)
                             
			
                        for i in unexploredstates:
                                if equal_games(i.game, new_state.game) == True:
                                                flag = True

                        if flag == False:
                                        unexploredstates.append(new_state)
                                        state = ids(new_state, maxLimit-1)
					if at_goal(state.game):
						return state

                if a[2] == 2:
                        new_game = move_down(game,a[0],a[1])
                        moves.append(list(a))
                        new_state = State(new_game,moves)


                        for i in unexploredstates:
                        	if equal_games(i.game, new_state.game) == True:
                                                flag = True
                                
                       	if flag == False:
                                        unexploredstates.append(new_state)
                                        state = ids(new_state, maxLimit-1)
                                        if at_goal(state.game):
                                                return state



                if a[2] == 3:
			
                        new_game = move_left(game,a[0],a[1])
                        moves.append(list(a))
                        new_state = State(new_game,moves)
        		print "////////////////////////////////////////////////////////"
        		print_board(new_state.game)
		        print "????????????????????????????????????????????????????????/"
	

                        for i in unexploredstates:
                                if equal_games(i.game, new_state.game) == True:
                                                flag = True
                       	if flag == False:
                                        unexploredstates.append(new_state)
					print "b"                   				
				       	state = ids(new_state, maxLimit-1)
                                        if at_goal(state.game):
                                                return state
		return state
	
def getstore(current_game):
	p_moves = []
	flag = False
	flag2 = False
	for k in range (0,len(current_game.game)):
        	for l in range (0,len(current_game.game[0])):
			if current_game.game[k][l] != '0':
				if not possible_move(current_game.game,k,l) == None:
					p_moves.append(possible_move(current_game.game,k,l))
	for a in p_moves:
		moves = []
		for g in current_game.donemoves:
			moves.append(list(g))
		if a[2] == 0:
			new_game = move_up(current_game,a[0],a[1])
			moves.append(list(a))
			salt= 0 
	
                        for l in exploredstates:
                                if equal_games(l.game, new_game):
                                        flag2 = True
					salt = salt +1
                        if flag2 == False:
                                new_state = State(new_game,moves)

				for i in unexploredstates:
					if equal_games(i.game, new_state.game) == True:
						flag = True
						salt = salt +1
				if flag == False:				
					unexploredstates.append(new_state)
			
		if a[2] == 1:
                        new_game = move_right(current_game,a[0],a[1]) 
                        moves.append(list(a))
			salt = 0
			
                        for l in exploredstates:
                                if equal_games(l.game, new_game):
                                        flag2 = True
					salt = salt +1
                        if flag2 == False:
                                new_state = State(new_game,moves)


                        	for i in unexploredstates:
                                	if equal_games(i.game, new_state.game) == True:
                                        	flag = True
						salt = salt +1
                        	if flag == False:
                                	unexploredstates.append(new_state)

			

		if a[2] == 2:
                        new_game = move_down(current_game,a[0],a[1])
                        moves.append(list(a))
			salt = 0
			
                        for l in exploredstates:
                                if equal_games(l.game, new_game):
                                        flag2 = True
					salt = salt +1
                        if flag2 == False:
                                new_state = State(new_game,moves)


                        	for i in unexploredstates:
                                	if equal_games(i.game, new_state.game) == True:
                                        	flag = True
						salt = salt +1
                        	if flag == False:
                                	unexploredstates.append(new_state)


          
		if a[2] == 3:
                        new_game = move_left(current_game,a[0],a[1]) 
                        moves.append(list(a))
			salt =0 
			
			for l in exploredstates:
				if equal_games(l.game, new_game):
					flag2 = True
					salt = salt + 1
			if flag2 == False:
                        	new_state = State(new_game,moves)

                  		for i in unexploredstates:
                                	if equal_games(i.game, new_state.game) == True:
                                        	flag = True
						salt = salt +1
                        	if flag == False:
                                	unexploredstates.append(new_state)

def inadmissible(game):
	row = 0
	column = 0	
	for i in range(0,len(game)):
		for m in range(0,len(game[0])):
			if game[i][m] == 'g':
				row = i
				column = m
				break;
	if game[row][column+1] == 'g':
		
		column = column+1
	number = len(game)-1 - column	
	tempnumber = 6

	if number != 1:
		for l in range(0,number):
			if game[row][column+l] != '0':
				tempnumber = tempnumber + 1
				if 'c' in game[row][column+l]:
					if empty(game,row-2,column+l) == False or empty(game,row+2,column+l) == False:
						tempnumber = tempnumber +1
				elif 't' in game[row][column+l]:
					if empty(game,row-3,column+l) == False or empty(game, row+3, column+l) == False:
						tempnumber = tempnumber +1
			
					 
			
	if number == 1:
		if game[row][column+1] != '0':

			tempnumber = tempnumber +1
		if number == 1 and tempnumber == 1:
			return 0 
	
	return tempnumber   

	
		

def admissible(game):
	row = 0
	column = 0	
	for i in range(0,len(game)):
		for m in range(0,len(game[0])):
			if game[i][m] == 'g':
				row = i
				column = m
				break;
	if game[row][column+1] == 'g':
		
		column = column+1
	number = len(game) - 1 - column	
	tempnumber = number
	
	for l in range(0,number):
			if game[row][column+l] != '0':
				tempnumber = tempnumber +1
	
		
	if number == 1 and tempnumber == 1:
			return 0 
	
	return tempnumber 

def sort(new_state, unexplored):

	if len(unexplored) == 0:
		unexplored.append(new_state)
	else:
		for i in range(0,len(unexplored)):
	    		if unexplored[i].cost >= new_state.cost:
				
				unexplored.insert(i,new_state)
				break
	return unexplored
 
## SEAR H CODE

# Top Level functi n is RushHour which takes a game file, a string indicating whether to use bfs or ids
#     and a maximum depth (this is used only for ids -- it should be ignored or not used for bfs)
def RushHour(filein, which, maxLimit, heuristic):
	game = load_game(filein)
       	salt =0
	if which == 'ids':
		moves = []
		new_game = State(game, moves)
		current_game = State(game, moves)
		for i in range(0,maxLimit):
						
			current_game = ids(new_game,i)
	
			if at_goal(current_game.game):
				break
		
		if at_goal(current_game.game):
			final = (current_game.donemoves, "exit", salt)
			print "ids: "
			print  final
			return final	
		else:
			print "fail"
			return "fail"
		
	elif which == 'bfs':
		beginning_game = copy_game(game)
		current_game = State(beginning_game, [])	
                
		
		while at_goal(current_game.game) == False:
		
		    getstore(current_game) 
		    exploredstates.append(current_game)
		    current_game = unexploredstates[0] #may be issue
		    unexploredstates.pop(0)
		 
		    
		final = (current_game.donemoves, "exit", salt + len(exploredstates)+1)
		print final
		return final
	
	elif which == 'astar':
		unexploredstates = []
		exploredstates = []
		moves = []
		count =0
		current_game = State(game, moves)
		current_game.cost = heuristic(current_game.game)
		unexploredstates.append(current_game)
		while len(unexploredstates) != 0:
			
	#		if filein == "testa1.txt":	
	#			if heuristic == inadmissible and count == 853 or heuristic == admissible and count == 306:
	#				break

			p_moves = []
			
			if at_goal(current_game.game):
				break;
			unexploredstates.pop(0)			
			exploredstates.append(current_game)
			for k in range (0,len(current_game.game)):
        			for l in range (0,len(current_game.game[0])):
					if current_game.game[k][l] != '0':
						if not possible_move(current_game.game,k,l) == None:
							p_moves.append(possible_move(current_game.game,k,l))

			x = current_game
              		for i in p_moves:
				flag = False
				flag2 = False
				moves = []
				
				for g in current_game.donemoves:
					moves.append(list(g))
				if i[2] == 0:
					
					new_game = move_up(current_game,i[0],i[1]) 
					moves.append(list(i))
					new_state = State(new_game, moves)
					
					if at_goal(new_state.game):
						x = new_state
						moves.append(list(i))		
						break
                        		for j in unexploredstates:
						if equal_games(j.game, new_state.game) == True: 
							flag = True
					if flag == False:
						h = heuristic(new_state.game)
						if (len(new_state.donemoves)-current_game.cost + h) <= heuristic(current_game.game):
					
							new_state.cost = h + len(new_state.donemoves)
						
							for z in exploredstates:
								if equal_games(z.game, new_state.game) == True:

									flag2 == True
							if flag2 == False:
                               					unexploredstates=sort(new_state,unexploredstates)		

				
				if i[2] == 1:

					new_game = move_right(current_game,i[0],i[1])
					moves.append(list(i))
					new_state = State(new_game, moves)
					 
					if at_goal(new_state.game):
						x = new_state
						moves.append(list(i))		
						break
                        		for j in unexploredstates:
						if equal_games(j.game, new_state.game) == True:
							flag = True
      					if flag == False:
						
						h = heuristic(new_state.game)
						if (len(new_state.donemoves)-current_game.cost + h) <= heuristic(current_game.game):
			
							new_state.cost = h + len(new_state.donemoves)

                  					for z in exploredstates:
                        	        				if equal_games(z.game, new_state.game) == True:

                        	                				flag2 = True
									
                        				if flag2 == False:
  	                     	        			unexploredstates=sort(new_state,unexploredstates)		
	
				if i[2] == 2:

					new_game = move_down(current_game,i[0],i[1])
					moves.append(list(i))
					new_state = State(new_game, moves)
					if at_goal(new_state.game):
						x = new_state
						moves.append(list(i))		
						break
                        		for j in unexploredstates:
						if equal_games(j.game, new_state.game) == True:
							flag = True 
      					if flag == False:
						h = heuristic(new_state.game)
						if (len(new_state.donemoves)-current_game.cost + h) <= heuristic(current_game.game):
			
							new_state.cost = h + len(new_state.donemoves)
				
								
                  					for z in exploredstates:
                        	        			if equal_games(z.game, new_state.game) == True:

                                        				flag2 = True
									
 	                       				if flag2 == False:
        	               	        			unexploredstates=sort(new_state,unexploredstates)		
	
				if i[2] == 3:

					new_game = move_left(current_game,i[0],i[1])
					moves.append(list(i))	
					new_state = State(new_game, moves) 
					if at_goal(new_state.game):
						x = new_state
						moves.append(list(i))		
						break
                        		for j in unexploredstates:
						if equal_games(j.game, new_state.game) == True:
							flag = True
					if flag == False:
					
						h = heuristic(new_state.game)
						if (len(new_state.donemoves)-current_game.cost + h) <= heuristic(current_game.game):

							new_state.cost = h + len(new_state.donemoves)
						
                  					for z in exploredstates:
                                					if equal_games(z.game, new_state.game) == True:

                                        					flag2 = True
									
                        				if flag2 == False:
   	                            				unexploredstates=sort(new_state,unexploredstates)
	
              		if at_goal(x.game) == True:
				current_game = x
				break
			current_game = unexploredstates[0]
			count = count +1

		finalmoves = []
			
		for c in current_game.donemoves:
				list1 = []
				list2 = []
				list1.append(c[0])
				list1.append(c[1])
				list2.append(list1)
				list2.append(c[2])
				finalmoves.append(list2)
		exit = []
		exit.append("exit")
		finalmoves.append(exit)	
		final = (finalmoves, current_game.cost, len(exploredstates))
	        print final	
		return final
			


		
       
if __name__ == '__main__' :
    # RushHour('test1.txt', 'astar', 0, admissible)
    # RushHour('test1.txt', 'astar', 0, inadmissible)
    # RushHour('test2.txt', 'astar', 0, admissible)
    # RushHour('test2.txt', 'astar', 0, inadmissible)
    # RushHour('test3.txt', 'astar', 0, admissible)
    # RushHour('test3.txt', 'astar', 0, inadmissible)
     #print "test4 admissible"
     #RushHour('test4.txt', 'astar', 0, admissible)
     #print "test4 inadmissible"
     #RushHour('test4.txt', 'astar', 0, inadmissible)
     #print "testa1 inadmissible"
     #RushHour('testa1.txt', 'astar', 0, inadmissible)
     print "testa1 admissible"
     RushHour('testa1.txt', 'astar', 0, admissible)
     

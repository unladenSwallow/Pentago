'''
Created on Jul 22, 2016
@author: Les
'''
import point_2D as point
import random
from copy import deepcopy as dc
import game_tree 

''' Creates a gameboard for the pentago game. Functions allow the 
ability to print the game board to the console and a file (log) as well as
game-play such as move or board rotations (Left or Right @ 90 degrees)'''
class Board:

    ''' Initializes the pentago gameboard to an empty board '''
    def __init__(self):
        self.pos_key = [point.Point(0,0), point.Point(0,1), point.Point(0,2), 
           point.Point(1,0), point.Point(1,1), point.Point(1,2),
           point.Point(2,0), point.Point(2,1), point.Point(2,2)]
        self.file = open('Output.txt', 'a')
        self.players = []
        self.block_1 = self.get_block()
        self.block_2 = self.get_block()
        self.block_3 = self.get_block()
        self.block_4 = self.get_block()
        self.blocks = {1 : self.block_1, 2: self.block_2, 
                       3: self.block_3, 4: self.block_4}
        self.DIAG_WINSblocks = [[1, 1, 2, 4, 4], [2, 2, 1, 3, 3], [1, 1, 1, 4, 4], 
                            [1, 1, 4, 4, 4], [2, 2, 2, 3, 3], [2, 2, 3, 3, 3], 
                            [1, 1, 3, 4, 4], [2, 2, 4, 3, 3]]
        self.DIAG_WINSplace = [[2, 6, 7, 2, 6], [2, 4, 9, 2, 4], [1, 5, 9, 1, 5], 
                               [5, 9, 1, 5, 9], [3, 5, 7, 3, 5], [5, 7, 3, 5, 7], 
                               [4, 8, 3, 4, 8], [6, 8, 1, 6, 8]]
        
    def getVal(self, block, position):
        point = self.pos_key[position - 1]
        return (self.blocks[block])[point.x][point.y]
    
    def testColWin(self, start):
        B = 'B'
        W = 'W'
        self.move(1, start, B)
        self.move(1, start + 3, B)
        self.move(1, start + 6, B)
        self.move(3, start, B)
        self.move(3, start + 3, B)
        self.print_board()
        self.is_goal_achieved()
        wins = self.is_goal_achieved()
        h = {'B':0, 'W':0}
        self.check_cols_heuristic(h)
        print "wins = B:", wins[B], "W:",  wins[W]
        print "H = B:", h[B], "W:", h[W]
        self.move(2, start, W)
        self.move(2, start + 3, W)
        self.move(2, start + 6, W)
        self.move(4, start, W)
        self.move(4, start + 3, W)
        self.print_board()
        wins = self.is_goal_achieved()
        self.check_cols_heuristic(h)
        print "wins = B:", wins[B], "W:",  wins[W]
        print "H = B:", h[B], "W:", h[W]
        
    def testDiagWin(self):
        token = 'B'
        for blox in range(0, len(self.DIAG_WINSblocks)):
            for spot in range(0, len(self.DIAG_WINSblocks[blox])):
                self.move(self.DIAG_WINSblocks[blox][spot], self.DIAG_WINSplace[blox][spot], token)
        self.print_board()
        wins = self.is_goal_achieved()
        h = {'B':0, 'W':0}
        self.get_diag_heuristic(h)
        print "H = B:", h['B'], "W:", h['W']
        print "Wins = B:", wins['B'], "W:", wins['W']
    
    def testRowWin(self):
        self.move(1, 1, 'B')
        self.move(1, 2, 'B')
        self.move(1, 3, 'B')
        self.move(2, 1, 'B')
        self.move(2, 2, 'B')
        self.move(1, 5, 'B')
        self.move(1, 6, 'B')
        self.move(2, 4, 'B')
        self.move(2, 5, 'B')
        self.move(2, 6, 'B')
        self.move(3, 1, 'B')
        self.move(3, 2, 'B')
        self.move(3, 3, 'B')
        self.move(4, 1, 'B')
        self.move(4, 2, 'B')
        self.move(3, 8, 'B')
        self.move(3, 9, 'B')
        self.move(4, 7, 'B')
        self.move(4, 8, 'B')
        self.move(4, 9, 'B')
        self.print_board()
        wins = self.is_goal_achieved()
        h = {'B': 0, 'W':0}
        self.check_rows_heuristic(h)
        print"H = B:", h['B'], "W:", h['W']
        print "Wins = B:", wins['B'], "W:", wins['W']
    
    ''' Returns a block for the board filled with dashes (empty)'''    
    def get_block(self):
        return [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']] 
    
    ''' prints half (top or bottom) of the gameboard to the console'''
    def print_half(self, b_1, b_2):
        print'+-------+-------+'
        for row in range(0,3):
            print '|', b_1[row][0], b_1[row][1], b_1[row][2], '|', b_2[row][0], b_2[row][1], b_2[row][2], '|'
    
    ''' prints the gameboard to the console'''       
    def print_board(self):
        self.print_half(self.block_1, self.block_2)
        self.print_half(self.block_3, self.block_4)
        print '+-------+-------+'
     
    ''' 
        Gets the heuristic for the current state
        Returns the heuristic dictionary
    '''   
    def get_heuristic(self):
        heuristic = {'B' : 0, 'W' : 0 }
        self.check_cols_heuristic(heuristic)
        self.check_rows_heuristic(heuristic)
        self.get_diag_heuristic(heuristic)
        wins = self.is_goal_achieved()
        heuristic['B'] += (wins['B'] * 100)
        heuristic['W'] += (wins['W'] * 100)
        return heuristic
    
    ''' logs the board in its current state to the output file'''   
    def log_board(self):
        self.file.write('+---+---+\n')
        for row in range(0,3):
            self.file.write('|'+ self.block_1[row][0] + self.block_1[row][1] +
                       self.block_1[row][2]+ '|' + self.block_2[row][0] + 
                       self.block_2[row][1] + self.block_2[row][2] + '|' +'\n')
        self.file.write('+---+---+\n')
        for row in range(0,3):
            self.file.write('|' + self.block_3[row][0] + self.block_3[row][1] + 
                       self.block_3[row][2] + '|' + self.block_4[row][0] + 
                       self.block_4[row][1] + self.block_4[row][2] + '|' +'\n')
        self.file.write('+---+---+\n')
        
    ''' logs the specifics of a player's move to the file'''
    def log_full_move(self, player, block_place, position, block_rot, direction):
        self.file.write("Player Name & Token:" + " " +  player.name +" - " + player.color + '\n')
        self.file.write(block_place + '/' + position +" "+ block_rot 
                        + direction + '\n')
    '''
         Implements a player's move checking for a win
         and printing the board afterward.
         Returns the boolean value true if a winner is found and false if not as
         well as the dictionary containing wins
    '''   
    def player_go(self, player, move):
        the_block = move[0]
        the_spot = move[2]
        self.move(int(the_block), int(the_spot), player.color)
        self.print_board()
        player.moves.append(move)
        wins = self.is_goal_achieved()
        won = False
        if wins['B'] > 0 or wins['W'] > 0:
            won = True
        return won, wins
    '''
         Implements a player's rotation checking for a win
         and printing the board afterward.
         Returns the boolean value true if a winner is found and false if not as
         well as the dictionary containing wins
    ''' 
    def player_rotate(self, player, rotate):
        the_block = rotate[0]
        the_direction = rotate[1]
        self.rotate(int(the_block), the_direction)
        self.print_board()
        player.moves.append(rotate)
        wins = self.is_goal_achieved()
        won = False
        if wins['B'] > 0 or wins['W'] > 0:
            won = True
        return won, wins
    
    ''' adds a player's piece to the board in the desired position'''    
    def move(self, block, position, token):
        space = self.pos_key[position - 1]
        row = space.x
        col = space.y
        (self.blocks[block])[row][col] = token    
#         self.print_board()
     
    ''' 
        Checks the block and position provided.
        Returns True if the space is available, False if it is not. 
    '''   
    def check_move(self, block, position):
        space = self.pos_key[position - 1]
        row = space.x
        col = space.y
        if (self.blocks[block])[row][col] != 'B' and (self.blocks[block])[row][col] != 'W':
            return True
        return False
        
            
     
    ''' rotates the board indicated 90 degrees in the specified direction'''   
    def rotate(self, block_num, direction):
        block = self.blocks[int(block_num)]
        row_1 = dc(block[0])
        row_2 = dc(block[1])
        row_3 = dc(block[2])
        if direction == 'L' or direction == 'l':
            for row in range(0,3):
                block[row][0] = row_1[2 - row] 
                block[row][1] = row_2[2 - row]
                block[row][2] = row_3[2 - row]
        elif direction == 'R' or direction == 'r':
            for row in range(0,3):
                block[row][0] = row_3[row] 
                block[row][1] = row_2[row]
                block[row][2] = row_1[row]
#         self.print_board()
      
    ''' Sets the players to the correct player order. '''  
    def set_players(self, p_1, p_2):
        self.players.append(p_1)
        self.players.append(p_2)
        
    ''' 
        Checks to see if any goal states have been achieved. 
        Returns the dictionary containing number of wins for each
        token.
    '''   
    def is_goal_achieved(self):
        wins = {'B': 0, 'W': 0}
        temp = self.check_colsWIN()
        wins['B'] += temp['B']
        wins['W'] += temp['W']
        temp = self.check_diagonalWIN()
        wins['B'] += temp['B']
        wins['W'] += temp['W']
        temp = self.check_rowsWIN()
        wins['B'] += temp['B']
        wins['W'] += temp['W']
        return wins
    
    ''' 
        Computes and sets the heuristic for the diagonal possibilities.
    '''
    def get_diag_heuristic(self, hval):
        blox = self.DIAG_WINSblocks
        places = self.DIAG_WINSplace
        val = self.getVal
        blocset = 0
        while blocset < len(blox):
            b = blox[blocset]
            p = places[blocset]
            if val(b[0], p[0]) != '-' and val(b[0], p[0]) == val(b[1], p[1]) and val(b[0], p[0]) == val(b[2], p[2]):
                hval[val(b[0], p[0])] += 5
                if val(b[0], p[0]) == val(b[3], p[3]):
                    hval[val(b[0], p[0])] += 10
            if val(b[1], p[1]) != '-' and val(b[1], p[1]) == val(b[2], p[2]) and val(b[1], p[1]) == val(b[3], p[3]):
                hval[val(b[1], p[1])] += 5
                if val(b[1], p[1]) == val(b[4], p[4]):
                    hval[val(b[1], p[1])] += 10
            if val(b[2], p[2]) != '-' and val(b[2], p[2]) == val(b[3], p[3]) and val(b[2], p[2]) == val(b[4], p[4]):
                hval[val(b[2], p[2])] += 5
            blocset += 1
    
    ''' 
        Checks the board's diagonals for a winner.
        Returns all wins in a dictionary mapped by token.
    '''
    def check_diagonalWIN(self):
        wins = {'B': 0, 'W': 0}
        winBlox = self.DIAG_WINSblocks
        winPlace = self.DIAG_WINSplace
        val = self.getVal
        for row in range(0, len(winBlox)):
            blox = winBlox[row]
            pos = winPlace[row]
            start = 0
            end = len(blox) - 1
            if val(blox[start], pos[start]) != '-' and val(blox[start], pos[start]) == val(blox[end], pos[end]):
                if val(blox[start], pos[start]) == val(blox[start+ 1], pos[start + 1]) and val(blox[start], pos[start]) == val(blox[end - 1], pos[end - 1]):
                    if val(blox[start], pos[start]) == val(blox[start + 2], pos[start + 2]):
                        wins[val(blox[start], pos[start])] += 1
        return wins
    
    ''' 
        Checks the columns for heuristic values, setting the h values to 
        the correct token in the dictionary.
    '''
    def check_cols_heuristic(self, h_val):
        top = 1
        bott = 3
        val = self.getVal
        for block_set in range(0,2):
            top = top + block_set
            bott = bott + block_set
            for start in range(1,4):
                if val(top, start) != '-' and val(top, start) == val(top, start + 3) and val(top, start) == val(top, start + 6):
                    h_val[val(top, start)] += 5
                    if val(top, start) == val(bott, start):
                        h_val[val(top, start)] += 10
                if val(top, start + 3) != '-' and val(top, start + 3) == val(top, start + 6) and val(top, start + 3) == val(bott, start):
                    h_val[val(top, start + 3)] += 5
                    if val(top, start + 3) == val(bott, start + 6):
                        h_val[val(top, start + 3)] += 10
                if val(top, start + 6) != '-' and val(top, start + 6) == val(bott, start) and val(top, start + 6) == val(bott, start + 3):
                    h_val[val(top, start + 6)] += 5
                    if val(top, start + 6) == val(bott, start + 6):
                        h_val[val(top, start + 6)] += 10
                if val(bott, start) != '-' and val(bott, start) == val(bott, start + 3) and val(bott, start) == val(bott, start + 6):
                    h_val[val(bott, start)] += 5
            
        
            
    ''' Checks the columns of the blocks passed as arguments for a winner.
        Returns all winning tokens in a dictionary mapped by token.
    '''
    def check_colsWIN(self):
        wins = {'B': 0, 'W': 0}
        top = 1
        bott = 3
        val = self.getVal
        for block_set in range(0,2):
            top = top + block_set
            bott = bott + block_set
            for start in range(1,4):
                if val(top, start) != '-' and val(top, start) == val(bott, start + 3):
                    if val(top, start) == val(top, start + 3) and val(top, start) == val(bott, start):
                        if val(top, start) == val(top, start + 6):
                            wins[val(top, start)] += 1
                if val(top, start + 3) != '-' and val(top, start + 3) == val(bott, start + 6):
                    if val(top, start + 3) == val(top, start + 6) and val(top, start + 3) == val(bott, start + 3):
                        if val(top, start) == val(bott, start):
                            wins[val(top, start + 3)] += 1
        return wins
    
    ''' 
        Gets the heuristic value of all rows for the current state and 
        adds them to the dictionary.
    '''
    def check_rows_heuristic(self, h_val):
        val = self.getVal
        left = 1
        right = 2
        sets = 0
        while sets < 2:
            start = 1
            end = 3
            while start < 8:
                if val(left, start) != '-' and val(left, start) == val(left, start + 1) and val(left, start + 1) == val(left, end):
                    h_val[val(left, start)] += 5
                    if val(left, end) == val(right, start):
                        h_val[val(left, start)] += 10
                if val(left, start + 1) != '-' and val(left, start + 1) == val(left, end) and val(left, start + 1) == val(right, start):
                    h_val[val(left, start + 1)] += 5
                    if val(left, start + 1) == val(right, start + 1):
                        h_val[val(left, start + 1)] += 10
                if val(left, end) != '-' and val(left, end) == val(right, start) and val(left, end) == val(right, start + 1):
                    h_val[val(left, end)] += 5
                    if val(left, end) == val(right, end):
                        h_val[val(left, end)] += 10
                if val(right, start) != '-' and val(right, start) == val(right, start + 1) and val(right, start) == val(right, end):
                    h_val[val(right, start)] += 5
                start += 3
                end += 3
            sets += 1
        
    ''' Checks the rows of the blocks passed as arguments for a winner.
        Returns:
        all winning tokens in the dictionary.
    '''
    def check_rowsWIN(self):
        wins = {'B': 0, 'W': 0}
        val = self.getVal
        left = 1
        right = 2
        sets = 0
        while sets < 2:
            start = 1
            end = 3
            while start < 8:
                if val(left, start) != '-' and val(left, start) ==  val(right, end - 1):
                    if val(left, start) == val(left, start + 1) and val(left, start) == val(right, end - 2):
                        if val(left, start) == val(left, end):
                            wins[val(left, start)] += 1
                elif val(left, start + 1) != '-' and val(left, start + 1) == val(right, end):
                    if val(left, start + 1) == val(left, end) and val(left, start + 1) == val(right, end - 1):
                        if val(left, start + 1) == val(right, start):
                            wins[val(left, start + 1)] += 1
                start += 3
                end += 3
            sets += 1
        return wins;
   
              
''' 
    Player class keeps track of the name, token color, and moves 
    for each player playing pentago
'''        
class Player:
    def __init__(self, name, color, AI_or_not):
        self.name = name
        self.color = color
        self.moves = []
        self.is_AI = AI_or_not

''' class initiates a game of Pentago between a computer (AI) and human
player '''                
class Play:
    def __init__(self):
        self.players = [] #max of 2
        self.board = Board();
        self.ai_tree = game_tree.Tree()
        self.moves_taken = 0
        
    ''' starts a game of pentago'''
    def start(self):
        self.determine_order() # get the order of play
        is_won = False
        curr_player = self.players[0]
        self.board.print_board()
        while not is_won:
            print curr_player.name,'\'s turn!'
            if curr_player.is_AI:
                move_info = {'move':0, 'twist':0, 'dir': 0}
                if self.moves_taken < 2:
                    bloc = random.randint(1, 4)
                    pos = random.randint(1, 9)
                    is_valid = self.board.check_move(bloc, pos)
                    while not is_valid:
                        bloc = random.randint(1, 4)
                        pos = random.randint(1, 9)
                    is_valid = self.board.check_move(bloc, pos)
                    twist_b = random.randint(1, 4)
                    twist_d = 'l'
                    if bloc % 2 == 0:
                        twist_d = 'r'
                    move = move_info['move'] = str(bloc) + '/' + str(pos)
                    move_info['twist'] = True
                    move_info['dir'] = str(twist_b) + twist_d
                else:
                    move_info = self.ai_tree.get_move(self.board, curr_player)
                    print 'Crtd:', self.ai_tree.num_created, 'Expd:', self.ai_tree.num_expanded
                    move = move_info['move']
                    twist = '1L'
                if move_info['twist']:
                    twist = move_info['dir']
                is_won, winners = self.board.player_go(curr_player, move_info['move'])
                self.board.print_board()
                if not is_won:
                    is_won, winners = self.board.player_rotate(curr_player, twist)
                    self.board.print_board()  
                    if move_info['twist']:
                        self.board.log_full_move(curr_player, move[0], move[2], move_info['dir'][0], move_info['dir'][1])
                    else:
                        self.board.log_full_move(curr_player, move[0], move[2], "NA", "NA")
                    self.board.log_board()
                print "Data placed their piece at block:", move[0], "position:", move[2]
                if move_info['twist']:
                    print "Data twisted block:",  move_info['dir'][0], "to the:",  move_info['dir'][1]
            else:
                move = raw_input("Enter your move w/o rotation")
                while not self.board.check_move(int(move[0]), int(move[2])):
                    print "invalid position. Try again."
                    move = raw_input("Enter your move w/o rotation")
                is_won, winners = self.board.player_go(curr_player, move)
                print "You placed your piece at block:", move[0], "position:", move[2]
                if not is_won:
                    rotate = raw_input("Enter your rotation")
                    is_won, winners = self.board.player_rotate(curr_player, rotate)
                    print "You twisted block:",  rotate[0], "to the:",  rotate[1]
                    self.board.print_board()
                    self.board.log_full_move(curr_player,move[0], move[2], rotate[0], rotate[1])
                    self.board.log_board()
                else:
                    self.board.log_full_move(curr_player, move[0], move[2], "NA", "NA")
                    self.board.log_board()
            curr_player = self.next_player(curr_player)
            self.moves_taken += 1
        if is_won:
            if winners['B'] > 0:
                if winners['W'] > 0:
                    print "Game Over. It's a TIE!"
                else:
                    if self.players[0].color == 'B':
                        print 'Game Over!', self.players[0].name, 'won!'
                    else:
                        print 'Game Over!', self.players[1].name, 'won!'
            elif winners['W'] > 0:
                if self.players[0].color == 'W':
                    print 'Game Over!', self.players[0].name, 'won!'
                else:
                    print 'Game Over!', self.players[1].name, 'won!'     
     
    ''' 
         Returns the next player in rotation.
    '''     
    def next_player(self, current):
        if current.name == self.players[0].name:
            return self.players[1]
        else:
            return self.players[0]
        
          
    ''' determines the order of play randomly and stores player info'''       
    def determine_order(self): 
        rand = random.randint(0,500)
        if rand % 2 == 0:
            color_rand = random.randint(0, 500)
            if color_rand % 2 == 0:
                print 'AI player, Data is first! Data has chosen to play (W)hite'
                self.players.append(Player('Data', 'W', True))
                name = raw_input('Player 2, enter your name here:')
                print 'hello,',  name + '! You will be playing (B)lack. Let\'s play!'
                self.players.append(Player(name, 'B', False))
                
            else:
                print 'AI player, Data is first! Data has chosen to play (B)lack'
                self.players.append(Player('Data', 'B', True))
                name = raw_input('Player 2, enter your name here:')
                print 'hello,', name + '! You will be playing (W)hite. Let\'s play!'
                self.players.append(Player(name, 'W', False))
            
        else:
            print 'You are first!'
            name = raw_input('Please enter your name here:')
            color = raw_input('Would you like to play as (B)lack or (W)hite?:')
            print name + ', meet Data, our friendly AI player and your opponent. Let\'s play!'
            if color == "W" or color == "w" or color.upper == "WHITE":
                self.players.append(Player(name, 'W', False))
                self.players.append(Player('Data', 'B', True))
            else:
                self.players.append(Player(name, 'B', False))
                self.players.append(Player('Data', 'W', True))
                
        self.board.set_players(self.players[0], self.players[1])
 
        
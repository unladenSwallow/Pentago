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
    
    ''' Returns a block for the board filled with dashes (empty)'''    
    def get_block(self):
        return [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']] 
    
    ''' prints half (top or bottom) of the gameboard to the console'''
    def print_half(self, b_1, b_2):
        print '+-------+-------+'
        for row in range(0,3):
            print '|', b_1[row][0], b_1[row][1], b_1[row][2], '|', b_2[row][0], b_2[row][1], b_2[row][2], '|'
    
    ''' prints the gameboard to the console'''       
    def print_board(self):
        self.print_half(self.block_1, self.block_2)
        self.print_half(self.block_3, self.block_4)
        print '+-------+-------+'
        
    def get_heuristic(self):
        trash_1, trash_2, h = self.is_goal_achieved()
        return h
    
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
    def log_full_move(self, block_place, position, block_rot, direction):
        self.file.write(block_place + '/' + ' ' + position + block_rot 
                        + direction + '\n')
        
    def player_go(self, player, move):
        the_block = move[0]
        the_spot = move[2]
        self.move(int(the_block), int(the_spot), player.color)
        self.print_board()
        player.moves.append(move)
        won, winners, trash = self.is_goal_achieved()
        print "B:", trash['B'], "W:", trash['W']
        return won, winners
    
    def player_rotate(self, player, rotate):
        the_block = rotate[0]
        the_direction = rotate[1]
        self.rotate(int(the_block), the_direction)
        self.print_board()
        player.moves.append(rotate)
        won, winners, trash = self.is_goal_achieved()
        print "B:", trash['B'], "W:", trash['W']
        return won, winners
    
    ''' adds a player's piece to the board in the desired position'''    
    def move(self, block, position, token):
        space = self.pos_key[position - 1]
        row = space.x
        col = space.y
        (self.blocks[block])[row][col] = token      
#         self.print_board()
        
    def check_move(self, block, position):
        space = self.pos_key[position - 1]
        row = space.x
        col = space.y
        if (self.blocks[block])[row][col] != 'B' and (self.blocks[block])[row][col] != 'W':
            return True
        return (self.blocks[block])[row][col]
        
            
     
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
        
    def set_players(self, p_1, p_2):
        self.players.append(p_1)
        self.players.append(p_2)
        
        
    def is_goal_achieved(self):   
        winners = []
        win_found = False
        h = {'B': 0, 'W': 0}
        wins = self.check_rows(self.block_1, self.block_2, h)
        if wins != False:
            for w in range(0,len(wins)):
                if wins[w] == 'B' or wins[w] == 'W':
                    winners.append(wins[w])
        wins = self.check_rows(self.block_3, self.block_4, h)
        if wins!= False:
            for w in range(0,len(wins)):
                if wins[w] == 'B' or wins[w] == 'W':
                    winners.append(wins[w])
        wins = self.check_cols(self.block_1, self.block_3, h)
        if len(wins) > 0:
            for w in range(0,len(wins)):
                if wins[w] == 'B' or wins[w] == 'W':
                    winners.append(wins[w])
        wins = self.check_cols(self.block_2, self.block_4, h)
        if len(wins) > 0:
            for w in range(0,len(wins)):
                if wins[w] == 'B' or wins[w] == 'W':
                    winners.append(wins[w])
        wins = self.check_diagonal(h)
        if len(wins) > 0:
            for w in range(0,len(wins)):
                if wins[w] == 'B' or wins[w] == 'W':
                    winners.append(wins[w])
        for w in range(0, len(winners)):
            print winners[w]
            if winners[w] == 'B' or winners[w] == 'W':
                win_found = True
        return win_found, winners, h
    
    ''' 
        Checks the board's diagonals for a winner
    '''
    def check_diagonal(self, h):
        winners = []
        b1 = self.block_1
        b2 = self.block_2
        b3 = self.block_3
        b4 = self.block_4
        if b1[2][2] == b4[0][0] and b4[0][0] != '-':
            if b1[1][1] == b4[0][0] and b4[0][0] == b4[1][1]:
                h[b1[1][1]] += 10 
                if b1[0][0] == b4[0][0] or b4[2][2] == b4[0][0]:
                    winners.append(b4[0][0]);
                    h[b4[0][0]] += 100
            if b1[1][1] == b4[0][0]  and b1[0][0] == b4[0][0]:
                h[b1[1][1]] += 10
            if b4[1][1] == b4[0][0] and b4[2][2] == b4[1][1]: 
                h[b4[1][1]] += 10
        if b1[1][2] == b2[2][0] and b2[2][0] == b4[0][1] and b4[0][1] != '-':
            if b1[0][1] == b4[0][1] and b4[0][1] == b4[1][2]:
                winners.append(b4[0][1] )
                h[b4[0][1]] += 100
            if b1[0][1] == b4[0][1]: 
                h[b1[0][1]] += 10
            if b4[0][1] == b4[1][2]:
                h[b4[0][1]] += 10
        if b1[2][1] == b3[0][2] and b4[1][0] == b3[0][2]  and b3[0][2]  != '-':
            if b1[2][1] == b1[1][0] and b1[2][1]  == b4[2][1]:
                winners.append(b1[2][1])
                h[b1[2][1]] += 100
            if b1[2][1] == b1[1][0]:
                h[b1[2][1]] += 10
            if b1[2][1] == b4[2][1]:
                h[b1[2][1]] += 10
        if b2[2][0] == b3[0][2] and b3[0][2] != '-':
            if b2[1][1] == b3[0][2] and b3[1][1] == b3[0][2]:
                h[b2[1][1]] += 10
                if b2[0][2] == b3[0][2] or b3[0][2] == b3[2][0]:
                    winners.append(b3[0][2])
                    h[b3[0][2]] += 100
            if b2[1][1] == b3[0][2] and b2[0][0] == b2[1][1]:
                h[b2[1][1]] += 10
            if b3[1][1] == b3[0][2] and b3[1][1] == b3[2][0]: 
                h[b3[1][1]] += 10
            if b2[1][1] == b3[0][2] and b2[0][2] == b3[0][2]:
                h[b2[1][1]] += 10
        if b2[1][0] == b1[2][2] and b2[1][0] == b3[0][1] and b3[0][1] != '-':
            if b2[0][1] == b2[1][0] and b2[0][1] == b3[1][0]:
                winners.append(b2[0][1])
                h[b2[0][1]] += 100
            if b2[0][1] == b2[1][0] and b2[0][1] != '-':
                h[b2[0][1]] += 10
            if b2[0][1] == b3[1][0] and b2[0][1] != '-':
                h[b3[1][0]] += 10
        if b2[2][1] == b4[0][0] and b4[0][0] == b3[1][2] and b4[0][0] != '-':
            if b2[1][2] == b4[0][0] and b4[0][0] == b3[2][1]:       
                winners.append(b4[0][0])
                h[b3[0][0]] += 100
            if b2[1][2] == b4[0][0]:
                h[b2[1][2]] += 10
            if b3[2][1] == b4[0][0]:
                h[b4[0][0]] += 10
        return winners
    
    ''' Checks the columns of the blocks passed as arguments for a winner
        Args:
        blk_1 - the first block from the board to check
        blk_2 - the second block from the board to check
        Returns:
        all winning tokens
    '''
    def check_cols(self, blk_1, blk_2, h):
        winners = []
        for col in range(0, 3):
            row_1 = 0
            row_2 = 1
            if blk_1[row_1][col] == blk_2[row_2][col] and blk_2[row_2][col] != '-':
                old = row_1
                row_1 += 1
                row_2 -= 1
                if blk_1[row_1][col] == blk_2[row_2][col] and blk_1[row_1][col] == blk_1[old][col]:
                    row_1 +=1
                    if blk_1[row_1][col] == blk_2[row_2][col]:
                        if blk_1[row_1][col]:
                            winners.append(blk_1[row_1][col])
                            h[blk_1[old][col]] += 100
            if blk_1[0][col] == blk_1[1][col] and blk_1[1][col] == blk_1[2][col] and blk_1[2][col] == blk_2[0][col] and blk_2[0][col] != '-':
                h[blk_1[0][col]] += 10
            if blk_1[1][col] == blk_1[2][col] and blk_1[1][col] == blk_2[0][col] and blk_2[1][col] == blk_2[0][col] and blk_2[0][col] != '-':
                h[blk_1[1][col]] += 10
            if blk_1[2][col] == blk_2[0][col] and blk_2[0][col] == blk_2[1][col] and blk_2[1][col] == blk_2[2][col] and blk_2[2][col] != '-':
                h[blk_1[2][col]] += 10 
            row_1 = 1
            row_2 = 2
            if blk_1[row_1][col] == blk_2[row_2][col] and blk_2[row_2][col] != '-':
                old = row_1
                row_1 += 1
                row_2 -= 1
                if blk_1[row_1][col] == blk_2[row_2][col] and blk_1[row_1][col] == blk_1[old][col]:
                    row_2 -=1
                    if blk_1[row_1][col] == blk_2[row_2][col]:
                        if blk_2[row_2][col] != '-':
                            winners.append(blk_2[row_1][col])
                            h[blk_1[old][col]] += 100
        return winners
        
    ''' Checks the rows of the blocks passed as arguments for a winner
        Args:
        blk_1 the first block from the board
        blk_2 the second block from the board
        Returns:
        all winning tokens
    '''
    def check_rows(self, blk_1, blk_2, h):
        winners = []
        for row in range(0, 3):
            win = self.check_left(blk_1[row], blk_2[row], h)
            if win != False:
                winners.append(win)
            win = self.check_right(blk_1[row], blk_2[row], h)      
            if win != False:
                winners.append(win)
        return winners
              
    ''' Checks the rows of the boards starting at the left for a winner
        Args: 
        left - the left block of the board to check
        right - the right block of the board to check
        Returns:
        the winner's token if a winner is found, False otherwise
    '''          
    def check_left(self, left, right, h):
        i = 0
        j = i + 1
        if left[i] == right[j] and left[i] != '-':
            old = i
            i += 1
            j -= 1
            if left[i] == right[j] and right[j] == left[old]:
                i += 1
                h[right[j]] += 10
                if left[i] == right[j]:
                    h[left[i]] += 100
                    return left[i]
        elif left[1] == left[2] and left[2]== right[0] and right[0] == right[1] and left[1] != '-':
            h[left[1]] += 10
        elif left[2] == right[0] and right[1] == right[0] and right[2] == right[1] and right[1] != '-':
            h[left[2]] += 10
        return False
    
    ''' Checks the rows of the boards starting at the right for a winner
        Args: 
        left - the left block of the board to check
        right - the right block of the board to check
        Returns:
        the winner's token if a winner is found, False otherwise
    '''   
    def check_right(self, left, right, h):
        i = 1
        j = 2
        if left[i] == right[j] and left[i] != '-':
            old = i
            i += 1
            j -= 1
            if left[i] == right[j] and right[j] == left[old] :
                h[right[j]] += 10
                i = j
                j -= 1
                if right[i] == right[j]:
                    h[right[i]] += 100
                    return right[i]
        elif left[0] == left[1] and left[1]== left[2] and right[0] == left[2] and left[1] != '-':
            h[left[1]] += 10
        elif left[2] == right[0] and right[1] == right[0] and right[2] == right[1] and right[1] != '-':
            h[left[2]] += 10
        return False        
              
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
        
    ''' starts a game of pentago'''
    def start(self):
        self.determine_order() # get the order of play
        is_won = False
        curr_player = self.players[0]
        self.board.print_board()
        while not is_won:
            print curr_player.name,'\'s turn!'
            if curr_player.is_AI:
                move_info = self.ai_tree.get_move(self.board, curr_player)
                move = move_info['move']
                dir = '1L'
                if move_info['twist']:
                    dir = move_info['dir']
                is_won, winners = self.board.player_go(curr_player, move)
                self.board.print_board()
                if not is_won:
                    is_won, winners = self.board.player_rotate(curr_player, dir)
                    self.board.print_board()
                    
            else:
                move = raw_input("Enter your move w/o rotation")
                while not self.board.check_move(int(move[0]), int(move[2])):
                    print "invalid position. Try again."
                    move = raw_input("Enter your move w/o rotation")
                is_won, winners = self.board.player_go(curr_player, move)
                if not is_won:
                    rotate = raw_input("Enter your rotation")
                    is_won, winners = self.board.player_rotate(curr_player, rotate)
                    self.board.print_board()
            print is_won
            curr_player = self.next_player(curr_player)
        win_1 = False
        win_2 = False
        for w in winners:
            if w == 'B':
                if self.players[0].color == 'B':
                    win_1 = True
                else:
                    win_2 = True
            if w == 'W':
                if self.players[0].color == 'W':
                    win_1 = True
                else:
                    win_2 = True
            
        if win_1 and win_2:
            print "It's a tie!"
        elif win_1:
            print "Player one,", self.players[0].name, "won the game!" 
        elif win_2:  
            print "Player two,", self.players[1].name, "won the game!" 
                
          
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
                print 'hello,' + name + '! You will be playing (B)lack. Let\'s play!'
                self.players.append(Player(name, 'B', False))
                
            else:
                print 'AI player, Data is first! Data has chosen to play (B)lack'
                self.players.append(Player('Data', 'B', True))
                name = raw_input('Player 2, enter your name here:')
                print 'hello,' + name + '! You will be playing (W)hite. Let\'s play!'
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
  
    
                
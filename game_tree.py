'''
Created on Aug 1, 2016
@author: Les
'''

from copy import deepcopy as dc
import pentago
import queues

''' Node class creates a node for the search tree '''
class Node:
    def __init__(self, game_board, node):
        # The cost by which to sort this node (varies by algorithm)
        self.total_cost = 0
        # The total cost to this state in the path
        self.pathlength = 0
        # The gameboard corresponding to this state
        self.state = game_board
        #The heuristic cost for the node
        self.h = 0
        # The tracker (node connected to this one in a path)
        self.tracker = node
        # The depth at which this node resides, -1 indicates no place in graph/tree
        self.depth = -1
    
    ''' Compares two board states, returning True if they are the same, else False.'''    
    def compare_states(self, other):
        my_blocks = [self.game_board.block_1, self.game_board.block_2, 
                     self.game_board.block_3, self.game_board.block_4]
        their_blocks = [other.game_board.block_1, other.game_board.block_2, 
                        other.game_board.block_3, other.game_board.block_4]
        for i in range(0,4):
            mine = my_blocks[i]
            theirs = their_blocks[i]
            for row in range(0,3):
                for col in range(0,3):
                    if mine[row][col] != theirs[row][col]:
                        return False
        return True
    
''' Class that creates the search tree or graph and implements the search.'''
class Tree:
    def __init__(self):
        self.root = Node(0, 0)
        self.root.depth = 0
        self.num_expanded = 0
        self.num_created = 0
        self.max_fringe = 0
        self.board_blocks = ['1', '2', '3', '4']
        self.twists = ['1L', '1R', '2L', '2R', '3L', '3R', '4L', '4R']
        
    ''' Uses the alpha beta pruning method with minimax to find the next move for Data-- AI.
        Returns the heuristic for the current best state'''
    def alpha_beta_minimax(self, node, is_max, depth, max_color, min_color, alpha, beta):
        if depth == 0:
            h = node.state.get_heuristic()
            return h[max_color] - h[min_color]
        moves = []
        self.get_available_moves(node.state, moves)
        self.num_expanded += 1
        for b in range(0, 4):
            for space in range(0, len(moves[b])):
                if is_max:
                    child = Node(dc(node.state), node)
                    child.state.move(b+1, space, max_color)
                    self.num_created += 1
                    v1 = self.alpha_beta_minimax(child, False, depth-1, max_color, min_color, alpha, beta)
                    alpha = max(alpha, v1)
                    if beta <= alpha:
                        break
                else:
                    child = Node(dc(node.state), node)
                    self.num_created += 1
                    child.state.move(b+1, space, min_color)
                    v1 = self.alpha_beta_minimax(child, True, depth-1, max_color, min_color, alpha, beta)
                    beta = min(beta, v1)
                    if beta <= alpha:
                        break 
        return v1                 
                
    ''' Uses the minimax algorithm to find the next move for Data-- AI.
        Returns the heuristic for the current best state'''
    def minimax(self, node, is_max, depth, max_color, min_color):
        if depth == 0:
            h = node.state.get_heuristic()
            return h[max_color] - h[min_color]
        h_val = 0
        moves = []
        self.get_available_moves(node.state, moves)
        self.num_expanded += 1
        for b in range(0, 4):
            for space in range(0, len(moves[b])):
                if is_max:
                    h_val = -32000
                    child = Node(dc(node.state), node)
                    child.state.move(b+1, space, max_color)
                    self.num_created += 1
                    v1 = self.minimax(child, False, depth-1, max_color, min_color)
                    h_val = max(h_val, v1)
                else:
                    h_val = 32000
                    child = Node(dc(node.state), node)
                    self.num_created += 1
                    child.state.move(b+1, space, min_color)
                    v1 = self.minimax(child, True, depth-1, max_color, min_color)
                    h_val = min(h_val, v1)
        return v1         
        
    ''' Get the next move for the AI player. Returns a dictionary containing
    the move the AI should take with keys:
     'move' a string that contains the next token placement
     'twist' a boolean that tells us if a twist is required or not
      and 'dir' a string indicating which block to rotate and what direction to 
      rotate it.'''
    def get_move(self, state, player):
        self.num_expanded = 0
        self.num_created = 0
        self.root = Node(dc(state), 0) # deep copy of the board for tree generation
        self.root.depth = 3
        self.num_created += 1
        best_h = -32000
        if player.color == 'B':
            enemy = 'W'
        else:
            enemy = 'B'
        moves = []
        self.get_available_moves(self.root.state, moves)
        plan = {'move': moves[0], 'twist':False, 'dir':0}
        for b in range(0, 4):
            for space in range(0, len(moves[b])):
                child = Node(dc(self.root.state), self.root)
                self.num_created += 1
                child.state.move(b + 1, space, player.color)
                child.depth = 1
                v1 = self.minimax(child, False, 2, player.color, enemy)
                # v1 = self.alpha_beta_minimax(child, False, 3, player.color, enemy, -32000, 32000)
                if v1 > best_h:
                    best_h = v1
                    plan['move'] =  str(b + 1) + '/' + str(moves[b][space])
                    plan['twist'] = False
                    temp = dc(child)
                for t in self.twists:
                    temp.state.rotate(t[0], t[1])
                    v2 = self.minimax(temp, False, 2, player.color, enemy)
                    # v2 = self.alpha_beta_minimax(child, False, 3, player.color, enemy, -32000, 32000)
                    if v2 > best_h:
                        best_h = v2
                        plan['move'] =  str(b + 1) + '/' + str(moves[b][space])
                        plan['twist'] = True
                        plan['dir'] = str
        return plan
    ''' Checks the board to see what moves are available. Returns
    a 2D array where the first index is the board chosen and 
    the second index contains the corresponding move.'''   
    def get_available_moves(self, state, moves): 
        block = state.block_1
        block_num = 1
        while block_num < 5:
            block_moves = []
            if block_num == 2:
                block = state.block_2 
            elif block_num == 3:
                block = state.block_3
            elif block_num == 4:
                block = state.block_4
            space = 1
            for row in range(0,3):
                for col in range(0,3):
                    if block[row][col] == '-':
                        block_moves.append(space)
                    space += 1       
            block_num += 1 
            moves.append(block_moves) 
            
     
        ''' Finds all tokens for the player on the board and returns
        a dictionary of block numbers mapped to the 
        tokens' positions'''
    def find_all_tokens(self, board, player, blox):
        all_moves = {1: [], 2: [], 3: [], 4: []}
        for bloc in range(1,5):
            for position in range(1,10):
                t = board.getVal(bloc, position)
                # get the piece above this (-3), below this (+3), and beside(+/- 1) if avail
                if t == player:
                    if position > 3:
                        temp = board.getVal(position - 3) 
                        if temp == '-':
                            all_moves[bloc].append(position - 3)
                    if position < 7:
                        temp = board.getVal(position + 3) 
                        if temp == '-':
                            all_moves[bloc].append(position + 3)
                    if position == 1 or position == 4 or position == 7:
                        temp = board.getVal(position + 1) 
                        if temp == '-':
                            all_moves[bloc].append(position + 1)
                    elif position == 3 or position == 6 or position ==  9:
                        temp = board.getVal(position - 1) 
                        if temp == '-':
                            all_moves[bloc].append(position - 1)
                    else:
                        temp = board.getVal(position + 1) 
                        if temp == '-':
                            all_moves[bloc].append(position + 1)
                        temp = board.getVal(position - 1)
                        if temp == '-':
                            all_moves[bloc].append(position + 1)
        return all_moves
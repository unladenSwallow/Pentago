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
    
class Tree:
    def __init__(self):
        self.root = Node(0, 0)
        self.root.depth = 0
        self.num_expanded = 0
        self.num_created = 0
        self.max_fringe = 0
        self.board_blocks = ['1', '2', '3', '4']
        self.twists = ['1L', '1R', '2L', '2R', '3L', '3R', '4L', '4R']
        
    def minimax(self, node, is_max, depth, max_color, min_color):
        self.num_expanded += 1
        if depth == 0:
            h = node.state.get_heuristic()
            return h[max_color] - h[min_color]
        alpha = None
        beta = None
        moves = []
        self.get_available_moves(node.state, moves)
#         for block in range(0, 4):
#             for space in range(0, len(moves[block])):
#                 print 'block = ', block + 1, 'space = ', moves[block][space]
        for b in range(0, 4):
            for space in range(0, len(moves[b])):
                if is_max:
                    alpha = -32000
                    for str in self.twists:
                        child = Node(dc(node.state), node)
                        child.state.move(b+1, space, max_color)
                        self.num_created += 1
                        v1 = self.minimax(child, False, depth-1, max_color, min_color)
                        child.state.rotate(str[0], str[1])
                        self.num_created += 1
                        v2 = self.minimax(child, False, depth-1, max_color, min_color)
                        alpha = max(alpha, v1, v2)
                else:
                    alpha = 32000
                    for t in self.twists:
                        child = Node(dc(node.state), node)
                        self.num_created += 1
                        child.state.move(b+1, space, min_color)
                        v1 = self.minimax(child, True, depth-1, max_color, min_color)
                        child.state.rotate(t[0], t[1])
                        self.num_created += 1
                        v2 = self.minimax(child, True, depth-1, max_color, min_color)
                        alpha = min(alpha, v1, v2)
        return alpha                
        
    def get_move(self, state, player):
        self.root = Node(dc(state), 0) # deep copy of the board for tree generation
        self.root.depth = 2
        self.num_created += 1
        best_h = -32000
        if player.color == 'B':
            enemy = 'W'
        else:
            enemy = 'B'
        moves = []
        self.get_available_moves(self.root.state, moves)
    #         for block in range(0, 4):
    #             for space in range(0, len(moves[block])):
    #                 print 'block = ', block + 1, 'space = ', moves[block][space]
    
        plan = {'move':moves[0], 'twist':False, 'dir':0}
        for b in range(0, 4):
            for space in range(0, len(moves[b])):
                for t in self.twists:
                    child = Node(dc(self.root.state), self.root)
                    child.state.move(b + 1, space, player.color)
                    child.depth = 1
                    v1 = self.minimax(child, False, 1, player.color, enemy)
                    if v1 > best_h:
                        best_h = v1
                        plan['move'] = moves[b]
                        plan['twist'] = False
                    child.state.rotate(t[0], t[1])
                    v2 = self.minimax(child, False, 1, player.color, enemy)
                    if v2 > v1 or v2 > best_h:
                        best_h = v2
                        plan['move'] = moves[b]
                        plan['twist'] = True
                        plan['dir'] = str
        return plan
       
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
    
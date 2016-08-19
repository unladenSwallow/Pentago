'''
Created on Jul 22, 2016
@author: Les
'''
import pentago

def main():
#     board = pentago.Board()
#     board.move(1, 1, 'B')
#     print 'going left:'
#     board.rotate(1, 'L')
#     print 'back to norm:'
#     board.rotate(1, 'R')
#     print 'going right:'
#     board.rotate(1, 'R')
#     print 'back to norm:'
#     board.rotate(1, 'L')
    game = pentago.Play()
    game.start()
    game.board.file.close()
    
    
main()
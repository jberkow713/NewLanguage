import pygame as p
import random
import sys
from pygame.constants import MOUSEBUTTONDOWN
import copy
p.init()

Width, Height = 1024, 1024
Max_FPS = 15

class Game:
    def __init__(self, size):
        self.size = size
        self.pieces = ['kn', 'r', 'b', 'q', 'k', 'p']
        self.screen = p.display.set_mode((Width, Height))   
        self.board = self.create_board()
        self.Sq_sz = int(Width/self.size)
        self.IMAGES = {}
        self.load_images()
       
    def create_board(self):
        
        Board = []
        top_row = []
        bottom_row = []
        
        for _ in range(self.size):
            piece = self.pieces[random.randint(0,3)]
            top_row.append('w' + piece)
            bottom_row.append('b' + piece)
        top_row[int(self.size/2)] = 'wk'
        bottom_row[int(self.size/2)]='bk'
        
        white_pawns = ['wp' for _ in range(self.size)]
        black_pawns = ['bp' for _ in range(self.size)]
        
        Board.append(top_row)
        Board.append(white_pawns)
        for _ in range(self.size-4):
            Board.append(['-' for _ in range(self.size)])
        Board.append(black_pawns)
        Board.append(bottom_row)
        return Board
        
    def load_images(self):

        pieces = ['br', 'bkn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wkn', 'wb', 'wq', 'wk', 'wp']
        for piece in pieces:
            self.IMAGES[piece]= p.transform.scale(p.image.load(piece+'.png'), (self.Sq_sz, self.Sq_sz))
    
    def drawBoard(self):

        colors = [p.Color('white'), p.Color('gray')]
        for r in range(self.size):
            for c in range(self.size):
                color = colors[((r+c)%2)]
                p.draw.rect(self.screen, color, p.Rect(c*self.Sq_sz, r*self.Sq_sz, self.Sq_sz, self.Sq_sz))
        return self.screen

    def draw_pieces(self):
    
        for r in range(self.size):
            for c in range(self.size):
                piece = self.board[r][c]
                if piece != '-':
                    self.screen.blit(self.IMAGES[piece], p.Rect(c*self.Sq_sz, r*self.Sq_sz, self.Sq_sz, self.Sq_sz))
class Comp:
    def __init__(self, color, Game):
        self.color = color
        self.board = Game.board
        if self.color == 'white':
            self.pieces = ['wr', 'wkn', 'wb', 'wq', 'wk', 'wp']
        if self.color =='black':
            self.pieces = ['br', 'bkn', 'bb', 'bq', 'bk', 'bp']
        self.moves = {}
        self.movable_keys = []
        self.can_move = False    
    
    def random_choice(self, list):
        return list[random.randint(0,len(list)-1)]

    def create_positions(self):
        moves = {}
        ROW = 0
        for row in self.board:
            COLUMN = 0
            for piece in row:
                if piece in self.pieces:
                    moves[(ROW,COLUMN)]=piece 
                COLUMN +=1
            ROW +=1

        self.moves = moves
        self.movable_keys = [x for x in moves.keys()]

    def find_pieces_moves(self, piece_position, piece_type):
        # piece position is tuple, col, row in self.board
        # Find piece type, and return a list of movable spots for that piece
        # If list returned >0:
        # set self.can_move = True
        
        # PlaceHolder, showing how it works
        return [(5,7), (10,6)]
        

    def random_move(self):
        # Move piece on the grid, there are no coordinates here, the game draw_pieces will do the rest
        # set Games board equal to this board, this will update the main board, before it is drawn
        self.can_move == False
        self.create_positions()
        while self.can_move == False:

            rand_grid = self.random_choice(self.movable_keys)
            rand_piece = self.moves[rand_grid]
            # Random selection from pieces, need to test if it can move
            print(rand_piece, rand_grid)
            moves = self.find_pieces_moves(rand_grid, rand_piece)
            if len(moves)>0:
                move = self.random_choice(moves)
                row = move[0]
                col = move[1]
                self.board[rand_grid[0]][rand_grid[1]]= '-'
                self.board[row][col] = rand_piece
                self.can_move = True

        Game.board = self.board        
       
    
def main():
    
    G = Game(32)
    C = Comp('white', G)
    clock = p.time.Clock()
    count = 0
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                sys.exit()
    
        G.screen.fill(p.Color('white'))
        G.drawBoard()
        G.draw_pieces()
        
        if count ==0:

            C.random_move()
            count +=1
        # This will update the game board so that next iteration of loop, game draws piece that has moved


        clock.tick(Max_FPS)
        p.display.flip()

main()            
        
            

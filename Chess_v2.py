import pygame as p
import random
from pygame.constants import MOUSEBUTTONDOWN
p.init()

Width, Height = 1024, 1024
Dimensions = 16
Sq_Size = int(Width/Dimensions)
Max_FPS = 15
IMAGES = {}

def load_images():

    pieces = ['br', 'bkn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wkn', 'wb', 'wq', 'wk', 'wp']
    for piece in pieces:
        IMAGES[piece]= p.transform.scale(p.image.load(piece+'.png'), (Sq_Size, Sq_Size))

class Game:
    def __init__(self, size):
        self.size = size
        self.pieces = ['kn', 'r', 'b', 'q', 'k', 'p']
        self.board = self.create_board()
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
        black_panws = ['bp' for _ in range(self.size)]
        empty_row = ['-' for _ in range(self.size)]
        Board.append(top_row)
        Board.append(white_pawns)
        for _ in range(self.size-4):
            Board.append(empty_row)
        Board.append(black_panws)
        Board.append(bottom_row)
        return Board

G = Game(10)
print(G.board)            
        
            

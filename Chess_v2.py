import pygame as p
import random
import sys
from pygame.constants import MOUSEBUTTONDOWN
p.init()

Width, Height = 1024, 1024
Max_FPS = 15




class Game:
    def __init__(self, size):
        self.size = size
        self.pieces = ['kn', 'r', 'b', 'q', 'k', 'p']
        self.board = self.create_board()
        self.screen = p.display.set_mode((Width, Height))
        self.Sq_sz = int(Width/self.size)
        self.IMAGES = {}
    
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
    
    def drawBoard(self):
        colors = [p.Color('white'), p.Color('gray')]
        for r in range(self.size):
            for c in range(self.size):
                color = colors[((r+c)%2)]
                p.draw.rect(self.screen, color, p.Rect(c*self.Sq_sz, r*self.Sq_sz, self.Sq_sz, self.Sq_sz))

    def load_images(self):

        pieces = ['br', 'bkn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wkn', 'wb', 'wq', 'wk', 'wp']
        for piece in pieces:
            self.IMAGES[piece]= p.transform.scale(p.image.load(piece+'.png'), (self.Sq_sz, self.Sq_sz))



def main():
    
    G = Game(16)
    clock = p.time.Clock()
    
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                sys.exit()
    
        G.screen.fill(p.Color('white'))
        G.drawBoard()
        clock.tick(Max_FPS)
        p.display.flip()   


main()            
        
            
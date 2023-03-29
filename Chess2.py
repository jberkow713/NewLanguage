import pygame as p
import random
import sys
from pygame.constants import MOUSEBUTTONDOWN
import copy
'''
This is a customizable chess game. You can play against a computer on whatever size board you want,
and the pieces are randomized. The AI for computer logic is still being created, but the functionality
allows for human-comp gaming.
'''

p.init()
Width, Height = 1024, 1024
Max_FPS = 15
clock = p.time.Clock()

class Game:
    def __init__(self, size):
        self.size = size
        self.pieces = ['kn', 'r', 'b', 'q']
        self.screen = p.display.set_mode((Width, Height))   
        self.board = self.create_board()
        self.Sq_sz = int(Width/self.size)
        self.IMAGES = {}
        self.load_images()
        self.Piece_Locations = {}
               
    def create_board(self):
        #Creates an in order list of chess board from top to bottom 
        Board = []
        top_row = []
        bottom_row = []        
        for _ in range(self.size):
            piece = self.pieces[random.randint(0,3)]
            top_row.append('w' + piece)
            bottom_row.append('b' + piece)
        # Setting Kings in Middle
        top_row[int(self.size/2)] = 'wk'
        bottom_row[int(self.size/2)]='bk'
        # Setting the Pawns
        white_pawns = ['wp' for _ in range(self.size)]
        black_pawns = ['bp' for _ in range(self.size)]
        # Start with bottom row
        Board.append(bottom_row)
        Board.append(black_pawns)
        # Middle Rows of empty squares
        for _ in range(2,self.size-2):
            Board.append(['-' for _ in range(self.size)])
        # Bottom Rows
        Board.append(white_pawns)
        Board.append(top_row)
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
        square = 0
        for r in range(self.size):
            for c in range(self.size):
                piece = self.board[r][c]
                # Mapping coordinates of pieces as they are drawn to self.Piece_Locations to be used for movement
                if piece != '-':
                    x_val = c * self.Sq_sz
                    y_val = r * self.Sq_sz
                    self.Piece_Locations[square]=(piece,x_val,y_val,x_val+self.Sq_sz,y_val+self.Sq_sz)
                    self.screen.blit(self.IMAGES[piece], p.Rect(x_val, y_val, self.Sq_sz, self.Sq_sz))
                    square+=1
                else:
                    x_val = c * self.Sq_sz
                    y_val = r * self.Sq_sz
                    self.Piece_Locations[square]=('-',x_val,y_val,x_val+self.Sq_sz, y_val+self.Sq_sz)
                    square +=1

class Player:
    def __init__(self, color, Game):
        self.color = color
        self.Game = Game
        self.board = Game.board
        self.dim = Game.size
        self.current_piece = None
        self.current_square = None
        self.time_flag = 0
        self.increment = None        
    
    def Increment(self):
        self.time_flag+=1
        if self.time_flag >= 10:
            self.time_flag=10
            self.increment = None
    
    def decrease_timer(self):
        self.time_flag-=1
        if self.time_flag <= 0:
            self.time_flag=0
            self.increment = None
    
    def move(self):
        
        if e.type == p.MOUSEBUTTONDOWN:            
            mouse_loc = p.mouse.get_pos()
            for square, info in self.Game.Piece_Locations.items():
                # Collision Detection
                if mouse_loc[0]>info[1] and mouse_loc[0]<info[3]:
                    if mouse_loc[1]>info[2] and mouse_loc[1]<info[4]:
                        if self.current_piece == None and self.time_flag==0:
                            if info[0]!='-':
                                self.current_piece = info[0]
                                self.current_square = square
                                self.increment = True
                                return
                            
                        elif self.current_piece!=None:
                            if self.time_flag>=5:

                                starting_piece = self.current_piece
                                ending_piece = info[0]
                                # Finding Grid Position
                                starting_col = self.current_square % self.dim
                                starting_row = self.current_square // self.dim
                                ending_col = square % self.dim
                                ending_row = square // self.dim                            
                                # Setting board for drawing
                                self.board[starting_row][starting_col] = ending_piece
                                self.board[ending_row][ending_col] = starting_piece
                                # Taking focus off clicked piece
                                self.current_piece = None
                                self.increment = False
                                return       

            

G = Game(20)
P = Player('black', G)

while True:
    for e in p.event.get():
        if e.type == p.QUIT:
            sys.exit()
    clock.tick(Max_FPS)
    G.screen.fill(p.Color('white'))
    G.drawBoard()
    G.draw_pieces()
    P.move()
    if P.increment==True:
        P.Increment()
    if P.increment==False:
        P.decrease_timer()
    
    
    p.display.flip()
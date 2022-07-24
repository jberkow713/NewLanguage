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
        
        Board.append(bottom_row)
        Board.append(black_pawns)
        for _ in range(self.size-4):
            Board.append(['-' for _ in range(self.size)])
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
        for r in range(self.size):
            for c in range(self.size):
                piece = self.board[r][c]
                if piece != '-':
                    self.screen.blit(self.IMAGES[piece], p.Rect(c*self.Sq_sz, r*self.Sq_sz, self.Sq_sz, self.Sq_sz))
class Comp:
    def __init__(self, color, Game):
        self.color = color
        self.Game = Game
        self.board = Game.board
        if self.color == 'white':
            self.pieces = ['wr', 'wkn', 'wb', 'wq', 'wk', 'wp']
            self.enemy_pieces = ['br', 'bkn', 'bb', 'bq', 'bk', 'bp']
        if self.color =='black':
            self.pieces = ['br', 'bkn', 'bb', 'bq', 'bk', 'bp']
            self.enemy_pieces = ['wr', 'wkn', 'wb', 'wq', 'wk', 'wp']
        self.moves = {}
        self.movable_keys = []
        self.enemy_moves = {}
        self.enemy_movable_keys = []
        self.can_move = False
        self.game_over = False    
    
    def random_choice(self, list):
        return list[random.randint(0,len(list)-1)]
    
    def on_board(self, val):
        if val[0]>=0 and val[0]<=self.Game.size-1:
            if val[1]>=0 and val[1]<=self.Game.size-1:
                return True
        return False         

    def create_positions(self):
        moves = {}
        enemy_moves = {}
        ROW = 0
        for row in self.board:
            COLUMN = 0
            for piece in row:
                if piece in self.pieces:
                    moves[(ROW,COLUMN)]=piece
                if piece in self.enemy_pieces:
                    enemy_moves[(ROW,COLUMN)] = piece     
                COLUMN +=1
            ROW +=1

        self.moves = moves
        self.movable_keys = [x for x in moves.keys()]
        self.enemy_moves = enemy_moves
        self.enemy_movable_keys =  [x for x in enemy_moves.keys()]

    def find_path(self, piece_position, piece):
        # Find limitations of movement based on the pieces position, piece type, and board size,
        # Returns a list of possible moves for that piece, or an empty list if no moves available 
        Usable_Moves = []
        Final_Moves = []       
        
        if piece == 'wr' or piece == 'br' or piece == 'wq' or piece == 'bq':
            Usable_Moves.append(self.move_left(piece_position))
            Usable_Moves.append(self.move_right(piece_position))
            Usable_Moves.append(self.move_up(piece_position))
            Usable_Moves.append(self.move_down(piece_position))
        if piece == 'wb' or piece =='bb' or piece =='wq' or piece =='bq':
            Usable_Moves.append(self.diag_left_down(piece_position))
            Usable_Moves.append(self.diag_left_up(piece_position))
            Usable_Moves.append(self.diag_r_down(piece_position))
            Usable_Moves.append(self.diag_r_up(piece_position))
        if piece == 'wkn' or piece =='bkn':
            Usable_Moves.append(self.knight_moves(piece_position))
        if piece == 'wk' or piece =='bk':
            Usable_Moves.append(self.king_moves(piece_position))
        if piece =='bp' or piece =='wp':
            Usable_Moves.append(self.pawn_moves(piece_position, piece))

        for x in Usable_Moves:
            for y in x:
                Final_Moves.append(y)
        Final_Enemy_Moves = [x for x in Usable_Moves if x in self.enemy_movable_keys]
        return Final_Moves, Final_Enemy_Moves
                
    def pawn_moves(self, piece_position, piece):
        movable_spots = []
        row = piece_position[0]
        col = piece_position[1]

        if piece =='wp':
            pos = row-1, col
            if self.on_board(pos)==True:
                if pos not in self.movable_keys and pos not in self.enemy_movable_keys:
                    movable_spots.append(pos) 
                left_diag = row-1,col-1
                if left_diag in self.enemy_movable_keys:
                    movable_spots.append(left_diag)
                right_diag = row-1, col+1
                if right_diag in self.enemy_movable_keys:
                    movable_spots.append(right_diag)
        if piece =='bp':
            pos = row+1, col
            if self.on_board(pos)==True:
                if pos not in self.movable_keys and pos not in self.enemy_movable_keys:
                    movable_spots.append(pos) 
                left_diag = row+1,col-1
                if left_diag in self.enemy_movable_keys:
                    movable_spots.append(left_diag)
                right_diag = row+1, col+1
                if right_diag in self.enemy_movable_keys:
                    movable_spots.append(right_diag)
        return movable_spots

    def king_moves(self, piece_position):
        movable_spots = []
        row = piece_position[0]
        col = piece_position[1]
        positions = [(row+1,col), (row-1,col), (row, col-1), (row,col+1),\
            (row-1,col-1), (row-1,col+1), (row+1,col-1), (row+1, col+1)]
        for x in positions:
            if self.on_board(x)==True:
                if x not in self.movable_keys:
                    movable_spots.append(x)
        return movable_spots    

    def knight_moves(self, piece_position):
        movable_spots = []
        row = piece_position[0]
        col = piece_position[1]
        positions = [(row-2,col+1), (row-2, col-1), (row+2, col+1), (row+2, col-1), \
            (row-1, col+2), (row+1, col+2), (row-1, col-2), (row+1, col-2)]
        for x in positions:
            if self.on_board(x)==True:
                if x not in self.movable_keys:
                    movable_spots.append(x)
        return movable_spots

    def move_left(self, piece_position):
        movable_spots = []        
        left = True
        curr_row = piece_position[0]
        curr_col = piece_position[1]  
        while left == True:            
            Next = curr_row, curr_col-1
            if self.on_board(Next)==False or Next in self.movable_keys:
                left = False  
                break            
            if Next in self.enemy_movable_keys:
                movable_spots.append(Next)
                left = False 
                break
            movable_spots.append(Next)
            curr_col -=1        
        return movable_spots

    def move_right(self,piece_position):
        movable_spots = []        
        right = True
        curr_row = piece_position[0]
        curr_col = piece_position[1] 
        while right == True:            
            Next = curr_row, curr_col+1
            if self.on_board(Next)==False or Next in self.movable_keys:
                right = False  
                break 
            if Next in self.enemy_movable_keys:
                movable_spots.append(Next)
                right = False 
                break
            movable_spots.append(Next)
            curr_col +=1        
        return movable_spots
    
    def move_up(self,piece_position):        
        movable_spots = []        
        up = True
        curr_row = piece_position[0]
        curr_col = piece_position[1]  
        while up == True:            
            Next = curr_row-1, curr_col
            if self.on_board(Next)==False or Next in self.movable_keys:
                up = False  
                break            
            if Next in self.enemy_movable_keys:
                movable_spots.append(Next)
                up = False 
                break
            movable_spots.append(Next)
            curr_row -=1        
        return movable_spots
    
    def move_down(self,piece_position):        
        movable_spots = []        
        down = True
        curr_row = piece_position[0]
        curr_col = piece_position[1]  
        while down == True:            
            Next = curr_row+1, curr_col
            if self.on_board(Next)==False or Next in self.movable_keys:
                down = False  
                break            
            if Next in self.enemy_movable_keys:
                movable_spots.append(Next)
                down = False 
                break
            movable_spots.append(Next)
            curr_row +=1        
        return movable_spots        
    
    def diag_r_down(self,piece_position):        
        movable_spots = []        
        drd= True
        curr_row = piece_position[0]
        curr_col = piece_position[1]   
        while drd == True:            
            Next = curr_row+1, curr_col+1
            if self.on_board(Next)==False or Next in self.movable_keys:
                drd = False  
                break            
            if Next in self.enemy_movable_keys:
                movable_spots.append(Next)
                drd = False 
                break
            movable_spots.append(Next)
            curr_row +=1
            curr_col +=1
        return movable_spots
    
    def diag_r_up(self,piece_position):        
        movable_spots = []        
        dru= True
        curr_row = piece_position[0]
        curr_col = piece_position[1]  
        while dru == True:            
            Next = curr_row-1, curr_col+1
            if self.on_board(Next)==False or Next in self.movable_keys:
                dru = False  
                break            
            if Next in self.enemy_movable_keys:
                movable_spots.append(Next)
                dru = False 
                break
            movable_spots.append(Next)
            curr_row -=1
            curr_col +=1
        return movable_spots      
    
    def diag_left_up(self,piece_position):        
        movable_spots = []        
        dlu= True
        curr_row = piece_position[0]
        curr_col = piece_position[1]  
        while dlu == True:            
            Next = curr_row-1, curr_col-1
            if self.on_board(Next)==False or Next in self.movable_keys:
                dlu = False  
                break            
            if Next in self.enemy_movable_keys:
                movable_spots.append(Next)
                dlu = False 
                break
            movable_spots.append(Next)
            curr_row -=1
            curr_col -=1
        return movable_spots
    
    def diag_left_down(self,piece_position):        
        movable_spots = []        
        dld= True
        curr_row = piece_position[0]
        curr_col = piece_position[1]  
        while dld == True:            
            Next = curr_row+1, curr_col-1
            if self.on_board(Next)==False or Next in self.movable_keys:
                dld = False  
                break            
            if Next in self.enemy_movable_keys:
                movable_spots.append(Next)
                dld = False 
                break
            movable_spots.append(Next)
            curr_row +=1
            curr_col -=1
        return movable_spots    

    def random_move(self):
        # Move piece on the grid, there are no coordinates here, the game draw_pieces will do the rest
        # set Games board equal to this board, this will update the main board, before it is drawn
        
        self.create_positions()
        if len(self.movable_keys)==0 or len(self.enemy_movable_keys)==0:
            self.game_over = True
            return
        
        while self.can_move == False:
            
            rand_grid = self.random_choice(self.movable_keys)
            rand_piece = self.moves[rand_grid]
            # Random selection from pieces, need to test if it can move
            # print(rand_piece, rand_grid)
            # moves actually is two lists, for testing just made it non conquerable moves
            all_moves = self.find_path(rand_grid, rand_piece)
            open_moves = all_moves[0]
            enemy_moves = all_moves[1]
            if len(open_moves)>0 and len(enemy_moves)>0:
                choice = random.randint(0,1)
                if choice ==0:
                    move = self.random_choice(open_moves)
                    row = move[0]
                    col = move[1]
                    self.board[rand_grid[0]][rand_grid[1]]= '-'
                    self.board[row][col] = rand_piece
                    self.can_move = True
                    break
                elif choice ==1:
                    move = self.random_choice(enemy_moves)
                    row = move[0]
                    col = move[1]
                    self.board[rand_grid[0]][rand_grid[1]]= '-'
                    self.board[row][col] = rand_piece
                    self.can_move = True
                    break            
            if len(open_moves)>0 and len(enemy_moves)==0:
                move = self.random_choice(open_moves)
                # print(move)
                row = move[0]
                col = move[1]
                self.board[rand_grid[0]][rand_grid[1]]= '-'
                self.board[row][col] = rand_piece
                self.can_move = True
                break
            if len(open_moves)==0 and len(enemy_moves)>0:
                move = self.random_choice(enemy_moves)
                row = move[0]
                col = move[1]
                self.board[rand_grid[0]][rand_grid[1]]= '-'
                self.board[row][col] = rand_piece
                self.can_move = True
                break
            else:
                if len(self.movable_keys)==1:
                    self.can_move==True
                    break 
                else:
                    self.movable_keys.remove(rand_grid)
                
                    

        self.Game.board = self.board
        self.can_move = False        
       
    
def main():
    
    G = Game(32)
    C = Comp('white', G)
    C2 = Comp('black', G)
    clock = p.time.Clock()
    
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                sys.exit()    
        G.screen.fill(p.Color('white'))
        G.drawBoard()
        G.draw_pieces()

        if C.game_over==True or C2.game_over==True:
            print('Game is over')
            sys.exit()
        C.random_move()
        C2.random_move()
        
        
        
        # This will update the game board so that next iteration of loop, game draws piece that has moved
        clock.tick(Max_FPS)
        p.display.flip()

main()            
        
            

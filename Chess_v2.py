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
def on_board(val, Dimensions):
    if val[0]>=0 and val[0]<=Dimensions-1:
        if val[1]>=0 and val[1]<=Dimensions-1:
            return True
    return False

def create_positions(board, pieces, enemy_pieces):
    moves = {}
    enemy_moves = {}
    ROW = 0
    for row in board:
        COLUMN = 0
        for piece in row:
            if piece in pieces:
                moves[(ROW,COLUMN)]=piece
            if piece in enemy_pieces:
                enemy_moves[(ROW,COLUMN)] = piece     
            COLUMN +=1
        ROW +=1
        
    movable_keys = [x for x in moves.keys()]
    enemy_movable_keys =  [x for x in enemy_moves.keys()]
    enemy_king_position = []
    for pos, piece in enemy_moves.items():
        if piece == 'wk' or piece =='bk':
            enemy_king_position.append(pos)
    your_king_position = []
    for pos, piece in moves.items():
        if piece == 'wk' or piece =='bk':
            your_king_position.append(pos)

    return moves, movable_keys, enemy_moves, enemy_movable_keys, enemy_king_position[0], your_king_position[0]

def pawn_moves(piece_position, piece, Dimensions, movable_keys, enemy_movable_keys):
    movable_spots = []
    row = piece_position[0]
    col = piece_position[1]

    if piece =='wp':
        pos = row-1, col
        if on_board(pos, Dimensions)==True:
            if pos not in movable_keys and pos not in enemy_movable_keys:
                movable_spots.append(pos) 
            left_diag = row-1,col-1
            if left_diag in enemy_movable_keys:
                movable_spots.append(left_diag)
            right_diag = row-1, col+1
            if right_diag in enemy_movable_keys:
                movable_spots.append(right_diag)
    if piece =='bp':
        pos = row+1, col
        if on_board(pos, Dimensions)==True:
            if pos not in movable_keys and pos not in enemy_movable_keys:
                movable_spots.append(pos) 
            left_diag = row+1,col-1
            if left_diag in enemy_movable_keys:
                movable_spots.append(left_diag)
            right_diag = row+1, col+1
            if right_diag in enemy_movable_keys:
                movable_spots.append(right_diag)
    return movable_spots

def king_moves(piece_position, Dimensions, movable_keys):
    movable_spots = []
    row = piece_position[0]
    col = piece_position[1]
    positions = [(row+1,col), (row-1,col), (row, col-1), (row,col+1),\
        (row-1,col-1), (row-1,col+1), (row+1,col-1), (row+1, col+1)]
    for x in positions:
        if on_board(x, Dimensions)==True:
            if x not in movable_keys:
                movable_spots.append(x)
    return movable_spots      

def knight_moves(piece_position, Dimensions, movable_keys):
    movable_spots = []
    row = piece_position[0]
    col = piece_position[1]
    positions = [(row-2,col+1), (row-2, col-1), (row+2, col+1), (row+2, col-1), \
        (row-1, col+2), (row+1, col+2), (row-1, col-2), (row+1, col-2)]
    for x in positions:
        if on_board(x, Dimensions)==True:
            if x not in movable_keys:
                movable_spots.append(x)
    return movable_spots

def move_left(piece_position, Dimensions, movable_keys, enemy_movable_keys):
    movable_spots = []        
    left = True
    curr_row = piece_position[0]
    curr_col = piece_position[1]  
    while left == True:            
        Next = curr_row, curr_col-1
        if on_board(Next, Dimensions)==False or Next in movable_keys:
            left = False  
            break            
        if Next in enemy_movable_keys:
            movable_spots.append(Next)
            left = False 
            break
        movable_spots.append(Next)
        curr_col -=1        
    return movable_spots

def move_right(piece_position, Dimensions, movable_keys, enemy_movable_keys):
    movable_spots = []        
    right = True
    curr_row = piece_position[0]
    curr_col = piece_position[1] 
    while right == True:            
        Next = curr_row, curr_col+1
        if on_board(Next, Dimensions)==False or Next in movable_keys:
            right = False  
            break 
        if Next in enemy_movable_keys:
            movable_spots.append(Next)
            right = False 
            break
        movable_spots.append(Next)
        curr_col +=1        
    return movable_spots

def move_up(piece_position, Dimensions, movable_keys, enemy_movable_keys):        
    movable_spots = []        
    up = True
    curr_row = piece_position[0]
    curr_col = piece_position[1]  
    while up == True:            
        Next = curr_row-1, curr_col
        if on_board(Next, Dimensions)==False or Next in movable_keys:
            up = False  
            break            
        if Next in enemy_movable_keys:
            movable_spots.append(Next)
            up = False 
            break
        movable_spots.append(Next)
        curr_row -=1        
    return movable_spots

def move_down(piece_position, Dimensions, movable_keys, enemy_movable_keys):        
    movable_spots = []        
    down = True
    curr_row = piece_position[0]
    curr_col = piece_position[1]  
    while down == True:            
        Next = curr_row+1, curr_col
        if on_board(Next, Dimensions)==False or Next in movable_keys:
            down = False  
            break            
        if Next in enemy_movable_keys:
            movable_spots.append(Next)
            down = False 
            break
        movable_spots.append(Next)
        curr_row +=1        
    return movable_spots        

def diag_r_down(piece_position, Dimensions, movable_keys, enemy_movable_keys):        
    movable_spots = []        
    drd= True
    curr_row = piece_position[0]
    curr_col = piece_position[1]   
    while drd == True:            
        Next = curr_row+1, curr_col+1
        if on_board(Next, Dimensions)==False or Next in movable_keys:
            drd = False  
            break            
        if Next in enemy_movable_keys:
            movable_spots.append(Next)
            drd = False 
            break
        movable_spots.append(Next)
        curr_row +=1
        curr_col +=1
    return movable_spots

def diag_r_up(piece_position, Dimensions, movable_keys, enemy_movable_keys):        
    movable_spots = []        
    dru= True
    curr_row = piece_position[0]
    curr_col = piece_position[1]  
    while dru == True:            
        Next = curr_row-1, curr_col+1
        if on_board(Next, Dimensions)==False or Next in movable_keys:
            dru = False  
            break            
        if Next in enemy_movable_keys:
            movable_spots.append(Next)
            dru = False 
            break
        movable_spots.append(Next)
        curr_row -=1
        curr_col +=1
    return movable_spots      

def diag_left_up(piece_position, Dimensions, movable_keys, enemy_movable_keys):        
    movable_spots = []        
    dlu= True
    curr_row = piece_position[0]
    curr_col = piece_position[1]  
    while dlu == True:            
        Next = curr_row-1, curr_col-1
        if on_board(Next, Dimensions)==False or Next in movable_keys:
            dlu = False  
            break            
        if Next in enemy_movable_keys:
            movable_spots.append(Next)
            dlu = False 
            break
        movable_spots.append(Next)
        curr_row -=1
        curr_col -=1
    return movable_spots

def diag_left_down(piece_position, Dimensions, movable_keys, enemy_movable_keys):        
    movable_spots = []        
    dld= True
    curr_row = piece_position[0]
    curr_col = piece_position[1]  
    while dld == True:            
        Next = curr_row+1, curr_col-1
        if on_board(Next, Dimensions)==False or Next in movable_keys:
            dld = False  
            break            
        if Next in enemy_movable_keys:
            movable_spots.append(Next)
            dld = False 
            break
        movable_spots.append(Next)
        curr_row +=1
        curr_col -=1
    return movable_spots

class Human:
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
        self.curr_loc = None
        self.piece_type = None
        self.curr_moves = []
        self.curr_enemy_moves = []        
        self.moved = False
        self.enemy_king = None
        self.king = None

    def find_square(self, mouse_pos):
        Positions = create_positions(self.board, self.pieces, self.enemy_pieces)
        self.moves = Positions[0]
        self.movable_keys = Positions[1]
        self.enemy_moves = Positions[2]
        self.enemy_movable_keys = Positions[3]
        self.enemy_king = Positions[4]
        self.king = Positions[5]        
        
        col = mouse_pos[0]//self.Game.Sq_sz
        row = mouse_pos[1]//self.Game.Sq_sz
        piece_position = row,col
        return piece_position
    def reset(self):
        self.curr_moves.clear()
        self.curr_enemy_moves.clear()
        self.curr_loc = None
        self.piece_type = None 
    
    def update_board(self, pos):
        
        self.board[self.curr_loc[0]][self.curr_loc[1]] = '-'
        self.board[pos[0]][pos[1]] = self.piece_type          
            
    def find_moves(self, location):
        piece_position = self.find_square(location)

        if piece_position in self.movable_keys:
            # Classifying piece for grid search
            piece = self.moves[(piece_position[0], piece_position[1])]

            Usable_Moves = []                
            
            if piece == 'wr' or piece == 'br' or piece == 'wq' or piece == 'bq':
                Usable_Moves.append(move_left(piece_position,self.Game.size, self.movable_keys, self.enemy_movable_keys))
                Usable_Moves.append(move_right(piece_position,self.Game.size, self.movable_keys, self.enemy_movable_keys))
                Usable_Moves.append(move_up(piece_position,self.Game.size, self.movable_keys, self.enemy_movable_keys))
                Usable_Moves.append(move_down(piece_position,self.Game.size, self.movable_keys, self.enemy_movable_keys))
            if piece == 'wb' or piece =='bb' or piece =='wq' or piece =='bq':
                Usable_Moves.append(diag_left_down(piece_position,self.Game.size, self.movable_keys, self.enemy_movable_keys))
                Usable_Moves.append(diag_left_up(piece_position,self.Game.size, self.movable_keys, self.enemy_movable_keys))
                Usable_Moves.append(diag_r_down(piece_position,self.Game.size, self.movable_keys, self.enemy_movable_keys))
                Usable_Moves.append(diag_r_up(piece_position,self.Game.size, self.movable_keys, self.enemy_movable_keys))
            if piece == 'wkn' or piece =='bkn':
                Usable_Moves.append(knight_moves(piece_position, self.Game.size, self.movable_keys))
            if piece == 'wk' or piece =='bk':
                Usable_Moves.append(king_moves(piece_position, self.Game.size, self.movable_keys))
            if piece =='bp' or piece =='wp':
                Usable_Moves.append(pawn_moves(piece_position, piece, self.Game.size, self.movable_keys, self.enemy_movable_keys))

            Final_Moves = [] 
            for x in Usable_Moves:
                for y in x:
                    Final_Moves.append(y)

            Final_Enemy_Moves = [x for x in Usable_Moves if x in self.enemy_movable_keys]
            self.curr_moves = Final_Moves
            self.curr_enemy_moves = Final_Enemy_Moves
            self.curr_loc = piece_position
            self.piece_type = piece
            return    

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
        self.all_moves = None
        self.all_enemy_moves = None
        self.can_move = False
        self.game_over = False
        self.enemy_king = None
        self.king = None
        self.check_info = None
        self.attackers = []     
    
    def in_check(self):
        # Determines if king is in check
        # If the king is in check, returns a list of lists, for each piece checking king, a list of spots
        # that can be blocked, to be used in getting out of check function, for the knight, more information given
        # including the knight's path  
        if self.color =='white':
            King = 'wk'
        elif self.color =='black':
            King = 'bk'    

        King_Attacks = []
        King_Attacks.append(move_left(self.king,self.Game.size, self.movable_keys, self.enemy_movable_keys))
        King_Attacks.append(move_right(self.king,self.Game.size, self.movable_keys, self.enemy_movable_keys))
        King_Attacks.append(move_up(self.king,self.Game.size, self.movable_keys, self.enemy_movable_keys))
        King_Attacks.append(move_down(self.king,self.Game.size, self.movable_keys, self.enemy_movable_keys))
        King_Attacks.append(diag_left_down(self.king,self.Game.size, self.movable_keys, self.enemy_movable_keys))
        King_Attacks.append(diag_left_up(self.king,self.Game.size, self.movable_keys, self.enemy_movable_keys))
        King_Attacks.append(diag_r_down(self.king,self.Game.size, self.movable_keys, self.enemy_movable_keys))
        King_Attacks.append(diag_r_up(self.king,self.Game.size, self.movable_keys, self.enemy_movable_keys))
        King_Attacks.append(knight_moves(self.king,self.Game.size, self.movable_keys))

        # List of all spots that can see the king, from perspective of the king if looking out on the board
        All_Moves = []
        for x in King_Attacks:
            for y in x:
                All_Moves.append(y)              
        
        Checks = []

        for check in All_Moves:
            for move, Piece in self.enemy_moves.items():
                if move ==check:
                    
                    attacking_path = self.find_path(move, Piece, enemy=True)
                    # If the piece which is in the king's vision has access to the king:
                    if self.king in attacking_path[0]:
                        if Piece == 'wkn' or Piece =='bkn':
                            self.attackers.append(self.find_path(move, Piece, enemy=True)[0])
                        else:
                            # This represents blocks that other pieces can make 
                            block = attacking_path[1]
                            block.remove(self.king)
                            # king can also move to this last spot, conquering the piece
                            block.append(move)
                            Checks.append(block)

                           
                            # Need to temporarily replace the king's key with nothing, and then add it back in
                            self.movable_keys.remove(self.king)
                            attacking_path_1 = self.find_path(move, Piece, enemy=True)
                            self.attackers.append(attacking_path_1[0])                                              
                            self.movable_keys.append(self.king)                            
        # Set class variable for later use
        self.check_info = Checks                    
        if len(Checks)>0:
            return Checks                           
        return False           
    
    def random_choice(self, list):
        return list[random.randint(0,len(list)-1)]
    
    def find_all_paths(self):
        # Finds path of all its own pieces, stores in class Dict
        if len(self.moves)==0:
            return
        move_dict = {}
        for pos,piece in self.moves.items():
            move_dict[(pos,piece)]= self.find_path(pos,piece)
        self.all_moves = move_dict
        return     
    
    def find_all_enemy_paths(self):
        # Finds Path of all enemies, stores in class Dict
        if len(self.enemy_moves)==0:
            return
        move_dict = {}
        for pos,piece in self.enemy_moves.items():
            move_dict[(pos,piece)]= self.find_path(pos,piece,enemy=True)
        self.all_enemy_moves = move_dict
        return  
    
    # added to commit
    def block_check(self):
        blocks = []
        for x in self.check_info:
            for y in x:
                blocks.append(y)        
        
        self.find_all_paths()
        
        blockers = []

        for block in blocks:
            for piece, moves in self.all_moves.items():            
                for list in moves:
                    for move in list:
                        if move == block:
                            if (piece,block) not in blockers:
                                if 'bk' not in piece:
                                    if 'wk' not in piece:
                                        blockers.append((piece, block))
                
        # TODO, add functionality to check if knight is checking king, to kill knight
        # Figure out way to deal with multiple checks at once, rare, but important
        
        return blockers

    def king_escapes(self):
               
        if self.color =='white':
            Piece = 'wk'
        else:
            Piece = 'bk'    
        
        attacks = []
        for x in self.attackers:
            for y in x:
                attacks.append(y)
        escapes = self.find_path(self.king, Piece)[0]
        valid_escapes =[]
        for move in escapes:
            if move not in attacks:
                if move not in self.check_info:
                    valid_escapes.append((Piece,move))
        return valid_escapes        

    def out_of_check(self):
        
        Escapes = []
        
        for Escape in self.block_check():
            Escapes.append(Escape)
        for escape in self.king_escapes():
            if escape not in Escapes:
                Escapes.append(escape)

        self.attackers.clear()
        return Escapes              

    def find_path(self, piece_position, piece, enemy=False):
        # Find limitations of movement based on the pieces position, piece type, and board size,
        # Returns a list of possible moves for that piece, or an empty list if no moves available 
        Usable_Moves = []
        Final_Moves = []     
        
        if enemy==False:
            keys = self.movable_keys
            enemy_keys = self.enemy_movable_keys
        elif enemy==True:
            keys = self.enemy_movable_keys
            enemy_keys = self.movable_keys

        if piece == 'wr' or piece == 'br' or piece == 'wq' or piece == 'bq':
            Usable_Moves.append(move_left(piece_position,self.Game.size, keys, enemy_keys))
            Usable_Moves.append(move_right(piece_position,self.Game.size, keys, enemy_keys))
            Usable_Moves.append(move_up(piece_position,self.Game.size, keys, enemy_keys))
            Usable_Moves.append(move_down(piece_position,self.Game.size, keys, enemy_keys))
        if piece == 'wb' or piece =='bb' or piece =='wq' or piece =='bq':
            Usable_Moves.append(diag_left_down(piece_position,self.Game.size, keys, enemy_keys))
            Usable_Moves.append(diag_left_up(piece_position,self.Game.size, keys, enemy_keys))
            Usable_Moves.append(diag_r_down(piece_position,self.Game.size, keys, enemy_keys))
            Usable_Moves.append(diag_r_up(piece_position,self.Game.size, keys, enemy_keys))
        if piece == 'wkn' or piece =='bkn':
            Usable_Moves.append(knight_moves(piece_position, self.Game.size, keys))
        if piece == 'wk' or piece =='bk':
            Usable_Moves.append(king_moves(piece_position, self.Game.size, keys))
        if piece =='bp' or piece =='wp':
            Usable_Moves.append(pawn_moves(piece_position, piece, self.Game.size, keys, enemy_keys))
        
        Blocks = []
        for x in Usable_Moves:
            if self.king in x:
                Blocks = x
            for y in x:
                Final_Moves.append(y)
               
        if enemy ==False:
            Final_Enemy_Moves = [x for x in Final_Moves if x in self.enemy_movable_keys]        
            return Final_Moves, Final_Enemy_Moves

        elif enemy ==True:
                           
            return Final_Moves,Blocks

    def smart_move(self):

        #Finds all moves for all pieces first, stores in self.all_moves 
        self.find_all_paths()
        self.find_all_enemy_paths()
        # for pos, 
        # TODO create intelligent design for smart interactive moves
        pass

    def random_move(self):
        # Move piece on the grid, there are no coordinates here, the game draw_pieces will do the rest
        # set Games board equal to this board, this will update the main board, before it is drawn
        
        Positions = create_positions(self.board, self.pieces, self.enemy_pieces)
        self.moves = Positions[0]
        self.movable_keys = Positions[1]
        self.enemy_moves = Positions[2]
        self.enemy_movable_keys = Positions[3]
        self.enemy_king = Positions[4]
        self.king = Positions[5]            
        
        if len(self.movable_keys)==0 or len(self.enemy_movable_keys)==0:
            self.game_over = True
            return

        # Premove, determine if king is in check        
        self.in_check()                       
        

        if self.check_info!=[]:
            
            Escapes = self.out_of_check()
            # [(((0, 9), 'br'), (2, 9)), (((1, 8), 'bp'), (2, 9)), ('bk', (0, 10)), ('bk', (1, 11)), ('bk', (2, 9))]
            rand_move = self.random_choice(Escapes)
            if rand_move[0] =='bk' or rand_move[0]=='wk':
                moved_from = self.king
                piece = rand_move[0]
            else:
                moved_from = rand_move[0][0]
                piece = rand_move[0][1]
            moved_to = rand_move[1]
            
            self.board[moved_from[0]][moved_from[1]]= '-'
            self.board[moved_to[0]][moved_to[1]] = piece            

            row = moved_from[0]
            col = moved_from[1]
            rand_piece=piece
        # Possible_Moves = self.out_of_check()
        # And then randomly select one move, and run something similar to the below loop
        # Run the other loop below

        elif self.check_info==[]:
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
                    # If only one key removes and it can not be moved
                    if len(self.movable_keys)==1:
                        self.can_move==True
                        break 
                    else:
                        self.movable_keys.remove(rand_grid)                    
    
        # Pawn upgrades after the move has been made
        white_upgrades = ['wkn', 'wq', 'wb', 'wr']
        black_upgrades =['bkn', 'bq', 'bb', 'br']

        if rand_piece == 'wp':
            if row == 0:
                upgrade = self.random_choice(white_upgrades)
                self.board[row][col] = upgrade
        if rand_piece == 'bp':
            if row == self.Game.size-1:
                upgrade = self.random_choice(black_upgrades)
                self.board[row][col] = upgrade

        self.Game.board = self.board
        self.can_move = False      
    
def main():    

    G = Game(20)
    H = Human('white', G)
    C = Comp('black', G)
    
    clock = p.time.Clock()
            
    while True:        

        for e in p.event.get():
            if e.type == p.QUIT:
                sys.exit()

        G.screen.fill(p.Color('white'))
        G.drawBoard()
        G.draw_pieces()

        if C.game_over==True:
            print('Game is over')
            sys.exit()        

        if e.type == p.MOUSEBUTTONDOWN:
            loc = p.mouse.get_pos()            
            H.find_moves(loc)
                        
            if len(H.curr_moves)>0 or len(H.curr_enemy_moves)>0:
                # (7, 3), Curr
                
                Curr = H.find_square(loc)
                # If you press the same piece, it resets the loop
                if Curr == H.curr_loc:
                    H.update_board(Curr)
                    H.reset()
                                    
                elif Curr!= H.curr_loc:                            
                    if Curr in H.curr_moves or Curr in H.curr_enemy_moves:
                        H.update_board(Curr)
                        H.Game.board = H.board
                        C.random_move()
                        H.reset()
                        
                    else:
                        H.reset()

                    #Once this click is made, meaning you didn't reclick, and you clicked a spot that could be made,
                    # The board needs to update, and then the computer needs to make a move           

            H.find_moves(loc)
                
        clock.tick(Max_FPS)
        p.display.flip()

main()            
        
            

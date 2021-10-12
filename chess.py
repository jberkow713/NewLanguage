import pygame as p
from pygame.constants import MOUSEBUTTONDOWN
p.init()

Width, Height = 1024, 1024
Dimensions = 16
Sq_Size = int(Width/Dimensions)
Max_FPS = 15
IMAGES = {}
def board_check(coord, Boardsize):
    
    if coord[0]>=0 and coord[0]<Boardsize:
        if coord[1]>=0 and coord[1]<Boardsize:
            return True        

def while_loop(condition, board, row, col, row_val, col_val, list,opp_list, final_list):
    
    while condition:
        if board[row+row_val][col+col_val] == '-':
            final_list.append((row+row_val,col+col_val))
        
        elif board[row+row_val][col+col_val] in opp_list:
            final_list.append((row+row_val,col+col_val))
            return

        elif board[row+row_val][col+col_val] in list:
            return
            
        row += row_val
        col += col_val
    
def create_moves(position, board, Boardsize, piece_type, piece_list, opposite_piece_list):
    possible_spots = []
    row_pos = position[0]
    col_pos = position[1]

    if piece_type == 'rook':
        temp_row = row_pos
        temp_col = col_pos 
        
        while temp_row>0:

            if board[temp_row-1][temp_col] == '-':
                possible_spots.append((temp_row-1,temp_col))

            elif board[temp_row-1][temp_col] in opposite_piece_list:
                possible_spots.append((temp_row-1,temp_col))
                break

            elif board[temp_row-1][temp_col] in piece_list:
                break

            temp_row-=1    
        
        temp_row = row_pos
        temp_col = col_pos                 
        
        while temp_row < Boardsize-1:
            if board[temp_row+1][temp_col] == '-':
                possible_spots.append((temp_row+1,temp_col))                
            
            elif board[temp_row+1][temp_col] in opposite_piece_list:
                possible_spots.append((temp_row+1,temp_col))
                break

            elif board[temp_row+1][temp_col] in piece_list:
                break
            
            temp_row+=1    
        
        temp_row = row_pos
        temp_col = col_pos 
        
        while temp_col>0:
            if board[temp_row][temp_col-1] == '-':
                possible_spots.append((temp_row,temp_col-1))
            
            elif board[temp_row][temp_col-1] in opposite_piece_list:
                possible_spots.append((temp_row,temp_col-1))
                break

            elif board[temp_row][temp_col-1] in piece_list:
                break
           
            temp_col-=1    
        
        temp_row = row_pos
        temp_col = col_pos 
        
        while temp_col < Boardsize-1:
            if board[temp_row][temp_col+1] == '-':
                possible_spots.append((temp_row,temp_col+1))

            elif board[temp_row][temp_col+1] in opposite_piece_list:
                possible_spots.append((temp_row,temp_col+1))
                break

            elif board[temp_row][temp_col+1] in piece_list:
                break

            temp_col+=1
               
        return possible_spots
    
    if piece_type == 'bishop':
        temp_row = row_pos
        temp_col = col_pos

        while temp_row>0 and temp_col>0:

            if board[temp_row-1][temp_col-1] == '-':
                possible_spots.append((temp_row-1,temp_col-1))

            elif board[temp_row-1][temp_col-1] in opposite_piece_list:
                possible_spots.append((temp_row-1,temp_col-1))
                break

            elif board[temp_row-1][temp_col-1] in piece_list:
                break

            temp_row-=1
            temp_col-=1
        
        temp_row = row_pos
        temp_col = col_pos

        while temp_row<Boardsize-1 and temp_col<Boardsize-1:

            if board[temp_row+1][temp_col+1] == '-':
                possible_spots.append((temp_row+1,temp_col+1))

            elif board[temp_row+1][temp_col+1] in opposite_piece_list:
                possible_spots.append((temp_row+1,temp_col+1))
                break

            elif board[temp_row+1][temp_col+1] in piece_list:
                break

            temp_row+=1
            temp_col+=1

        temp_row = row_pos
        temp_col = col_pos

        while temp_row>0 and temp_col<Boardsize-1:

            if board[temp_row-1][temp_col+1] == '-':
                possible_spots.append((temp_row-1,temp_col+1))

            elif board[temp_row-1][temp_col+1] in opposite_piece_list:
                possible_spots.append((temp_row-1,temp_col+1))
                break

            elif board[temp_row-1][temp_col+1] in piece_list:
                break

            temp_row-=1
            temp_col+=1

        temp_row = row_pos
        temp_col = col_pos

        while temp_row<Boardsize-1 and temp_col>0:

            if board[temp_row+1][temp_col-1] == '-':
                possible_spots.append((temp_row+1,temp_col-1))

            elif board[temp_row+1][temp_col-1] in opposite_piece_list:
                possible_spots.append((temp_row+1,temp_col-1))
                break

            elif board[temp_row+1][temp_col-1] in piece_list:
                break

            temp_row+=1
            temp_col-=1
        return possible_spots    
    
    if piece_type == 'queen':
        
        temp_row = row_pos
        temp_col = col_pos 
        
        while temp_row>0:

            if board[temp_row-1][temp_col] == '-':
                possible_spots.append((temp_row-1,temp_col))

            elif board[temp_row-1][temp_col] in opposite_piece_list:
                possible_spots.append((temp_row-1,temp_col))
                break

            elif board[temp_row-1][temp_col] in piece_list:
                break

            temp_row-=1    
        
        temp_row = row_pos
        temp_col = col_pos                 
        
        while temp_row < Boardsize-1:
            if board[temp_row+1][temp_col] == '-':
                possible_spots.append((temp_row+1,temp_col))                
            
            elif board[temp_row+1][temp_col] in opposite_piece_list:
                possible_spots.append((temp_row+1,temp_col))
                break

            elif board[temp_row+1][temp_col] in piece_list:
                break
            
            temp_row+=1    
        
        temp_row = row_pos
        temp_col = col_pos 
        
        while temp_col>0:
            if board[temp_row][temp_col-1] == '-':
                possible_spots.append((temp_row,temp_col-1))
            
            elif board[temp_row][temp_col-1] in opposite_piece_list:
                possible_spots.append((temp_row,temp_col-1))
                break

            elif board[temp_row][temp_col-1] in piece_list:
                break
           
            temp_col-=1    
        
        temp_row = row_pos
        temp_col = col_pos 
        
        while temp_col < Boardsize-1:
            if board[temp_row][temp_col+1] == '-':
                possible_spots.append((temp_row,temp_col+1))

            elif board[temp_row][temp_col+1] in opposite_piece_list:
                possible_spots.append((temp_row,temp_col+1))
                break

            elif board[temp_row][temp_col+1] in piece_list:
                break

            temp_col+=1
        temp_row = row_pos
        temp_col = col_pos

        while temp_row>0 and temp_col>0:

            if board[temp_row-1][temp_col-1] == '-':
                possible_spots.append((temp_row-1,temp_col-1))

            elif board[temp_row-1][temp_col-1] in opposite_piece_list:
                possible_spots.append((temp_row-1,temp_col-1))
                break

            elif board[temp_row-1][temp_col-1] in piece_list:
                break

            temp_row-=1
            temp_col-=1
        
        temp_row = row_pos
        temp_col = col_pos

        while temp_row<Boardsize-1 and temp_col<Boardsize-1:

            if board[temp_row+1][temp_col+1] == '-':
                possible_spots.append((temp_row+1,temp_col+1))

            elif board[temp_row+1][temp_col+1] in opposite_piece_list:
                possible_spots.append((temp_row+1,temp_col+1))
                break

            elif board[temp_row+1][temp_col+1] in piece_list:
                break

            temp_row+=1
            temp_col+=1

        temp_row = row_pos
        temp_col = col_pos

        while temp_row>0 and temp_col<Boardsize-1:

            if board[temp_row-1][temp_col+1] == '-':
                possible_spots.append((temp_row-1,temp_col+1))

            elif board[temp_row-1][temp_col+1] in opposite_piece_list:
                possible_spots.append((temp_row-1,temp_col+1))
                break

            elif board[temp_row-1][temp_col+1] in piece_list:
                break

            temp_row-=1
            temp_col+=1

        temp_row = row_pos
        temp_col = col_pos

        while temp_row<Boardsize-1 and temp_col>0:

            if board[temp_row+1][temp_col-1] == '-':
                possible_spots.append((temp_row+1,temp_col-1))

            elif board[temp_row+1][temp_col-1] in opposite_piece_list:
                possible_spots.append((temp_row+1,temp_col-1))
                break

            elif board[temp_row+1][temp_col-1] in piece_list:
                break

            temp_row+=1
            temp_col-=1
        return possible_spots   
    #return a list of possible moves based on the input that user can move to

class Gamestate():
    def __init__(self):
        self.board = [
            ['br','bkn',  'bkn','bkn', 'bb','bb', 'bq','bq', 'bk','bb', 'bb', 'bb', 'bkn','bkn', 'bkn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr','wkn',  'wkn','wkn', 'wb','wb', 'wq','wq', 'wk','wb', 'wb', 'wb', 'wkn','wkn', 'wkn', 'wr'],
            

                    ]
        self.turn = 'White'
        self.white_moves = ['wp', 'wr', 'wkn', 'wb', 'wq', 'wk']
        self.black_moves = ['bp', 'br', 'bkn', 'bb', 'bq', 'bk']
        self.move_log = []
        self.white_in_check = False
        self.black_in_check = False  
        self.initial_move_log = self.check_initial_movement()

    def check_initial_movement(self):
        d = {}
        list_to_check = ['br', 'bk', 'bp', 'wr', 'wk', 'wp']
        for x in range(Dimensions):
            for y in range(Dimensions):
                piece = self.board[x][y]
                if piece in list_to_check:
                    d[(x,y)]='False'
        return d   

    def in_check(self):
        pos = []
        if self.turn == 'White':
            #check knight position
            opposite_piece_list = ['bp', 'br','bkn', 'bb', 'bq', 'bk']
            piece_list =   ['wp', 'wr', 'wkn', 'wb', 'wq', 'wk']
            narrowed_list = ['br', 'bb', 'bq']  
            for x in range(Dimensions):
                for y in range(Dimensions):
                    piece = self.board[x][y]
                    if piece == 'wk':
                        X,Y = x,y
                        
            possible= [(X+2, Y+1), (X+2, Y-1),(X-2, Y+1), (X-2, Y-1),\
                (X+1, Y+2), (X+1, Y-2), (X-1, Y+2),(X-1, Y-2)]
            for i in possible:
                if board_check(i, Dimensions)==True:
                    if self.board[i[0]][i[1]]=='bkn':
                        return True
            possible_pawn = [(X-1, Y+1),(X-1, Y-1) ]
            
            for i in possible_pawn:
                if board_check(i, Dimensions)==True:
                    if self.board[i[0]][i[1]]=='bp':
                        return True                 

        if self.turn == 'Black':
            #check knight position
            piece_list = ['bp', 'br','bkn', 'bb', 'bq', 'bk']
            opposite_piece_list =   ['wp', 'wr', 'wkn', 'wb', 'wq', 'wk']
            narrowed_list = ['wr', 'wb', 'wq']  
            for x in range(Dimensions):
                for y in range(Dimensions):
                    piece = self.board[x][y]
                    if piece == 'bk':
                        X,Y = x,y
                        
            possible= [(X+2, Y+1), (X+2, Y-1),(X-2, Y+1), (X-2, Y-1),\
                (X+1, Y+2), (X+1, Y-2), (X-1, Y+2),(X-1, Y-2)]
            for i in possible:
                if board_check(i, Dimensions)==True:
                    if self.board[i[0]][i[1]]=='wkn':
                        return True
            possible_pawn = [(X+1, Y+1),(X+1, Y-1) ]
            
            for i in possible_pawn:
                if board_check(i, Dimensions)==True:
                    if self.board[i[0]][i[1]]=='wp':
                        return True                             
        
        surroundings = [(X, Y-1), (X,Y+1), (X+1, Y-1), (X+1, Y+1), (X-1, Y-1), (X+1,Y), (X-1,Y)]
        if self.turn =='White':
            for i in surroundings:
                if board_check(i, Dimensions)==True:
                    if self.board[i[0]][i[1]]=='bk':
                        
                        return True
        elif self.turn == 'Black':
            for i in surroundings:
                if board_check(i, Dimensions)==True:
                    if self.board[i[0]][i[1]]=='wk':
                        
                        return True

        Boardsize = Dimensions
        temp_row, temp_col = X,Y
        possible_spots = []
        board = self.board 

        while temp_row>0:

            if board[temp_row-1][temp_col] in opposite_piece_list:
                if board[temp_row-1][temp_col] in narrowed_list:

                    possible_spots.append((temp_row-1,temp_col))
                break
            
            elif board[temp_row-1][temp_col] in piece_list:
                break
            temp_row-=1    
        
        temp_row = X
        temp_col = Y                 
        
        while temp_row < Boardsize-1:                        
            
            if board[temp_row+1][temp_col] in opposite_piece_list:
                if board[temp_row+1][temp_col] in narrowed_list:
                    possible_spots.append((temp_row+1,temp_col))
                break

            elif board[temp_row+1][temp_col] in piece_list:
                break
            
            temp_row+=1    
        
        temp_row = X
        temp_col = Y  
        
        while temp_col>0:            
            
            if board[temp_row][temp_col-1] in opposite_piece_list:
                if board[temp_row][temp_col-1] in narrowed_list:
                    possible_spots.append((temp_row,temp_col-1))
                break

            elif board[temp_row][temp_col-1] in piece_list:
                break
           
            temp_col-=1    
        
        temp_row = X
        temp_col = Y  
        
        while temp_col < Boardsize-1:
            
            if board[temp_row][temp_col+1] in opposite_piece_list:
                if board[temp_row][temp_col+1] in narrowed_list:
                    possible_spots.append((temp_row,temp_col+1))
                break

            elif board[temp_row][temp_col+1] in piece_list:
                break            
            temp_col+=1

        temp_row = X
        temp_col = Y 

        while temp_row>0 and temp_col>0:
            
            if board[temp_row-1][temp_col-1] in opposite_piece_list:
                if board[temp_row-1][temp_col-1] in narrowed_list:
                    possible_spots.append((temp_row-1,temp_col-1))
                break

            elif board[temp_row-1][temp_col-1] in piece_list:
                break

            temp_row-=1
            temp_col-=1
        
        temp_row = X
        temp_col = Y 

        while temp_row<Boardsize-1 and temp_col<Boardsize-1:
           
            if board[temp_row+1][temp_col+1] in opposite_piece_list:
                if board[temp_row+1][temp_col+1] in narrowed_list:
                    possible_spots.append((temp_row+1,temp_col+1))
                break

            elif board[temp_row+1][temp_col+1] in piece_list:
                break

            temp_row+=1
            temp_col+=1

        temp_row = X
        temp_col = Y 

        while temp_row>0 and temp_col<Boardsize-1:           

            if board[temp_row-1][temp_col+1] in opposite_piece_list:
                if board[temp_row-1][temp_col+1] in narrowed_list:
                    possible_spots.append((temp_row-1,temp_col+1))
                break

            elif board[temp_row-1][temp_col+1] in piece_list:
                break

            temp_row-=1
            temp_col+=1

        temp_row = X
        temp_col = Y 

        while temp_row<Boardsize-1 and temp_col>0:
            
            if board[temp_row+1][temp_col-1] in opposite_piece_list:
                if board[temp_row+1][temp_col-1] in narrowed_list:
                    possible_spots.append((temp_row+1,temp_col-1))
                break

            elif board[temp_row+1][temp_col-1] in piece_list:
                break

            temp_row+=1
            temp_col-=1
        #Checking to see if pieces in kings line of sight can actually attack the king, putting him in check
        if self.turn == 'White':
            pce_list = ['bp', 'bkn', 'br', 'bq', 'bk', 'bb']
            opp_piece_list = ['wp', 'wkn', 'wr', 'wq', 'wk', 'wb']
        if self.turn == 'Black':
            pce_list =  ['wp', 'wkn', 'wr', 'wq', 'wk', 'wb']
            opp_piece_list =  ['bp', 'bkn', 'br', 'bq', 'bk', 'bb']  
                
        for x in possible_spots:
            Boardsize = Dimensions
            piece = board[x[0]][x[1]]
            if piece == 'wq' or piece == 'bq':
                return True 

            if piece == 'bb' or piece == 'wb':
                piece_type = 'bishop'
                opposing_pieces = create_moves(x, board, Boardsize, piece_type, pce_list, opp_piece_list)
                
                for x in opposing_pieces:
                    piece = board[x[0]][x[1]]
                    if piece == 'wk' or piece == 'bk':
                        return True 
                    
            if piece == 'br' or piece == 'wr':
                piece_type = 'rook'
                opposing_pieces = create_moves(x, board, Boardsize, piece_type, pce_list, opp_piece_list)
                for x in opposing_pieces:
                    piece = board[x[0]][x[1]]
                    if piece == 'wk' or piece == 'bk':
                        return True 
                    
        return False           

    def check_move(self, starting_position, ending_position):
        #starting and ending positions are going to be grid locations on the game grid
        
        piece_type = self.board[starting_position[0]][starting_position[1]]
        
        possible_pieces = ['wp', 'bp', 'wkn', 'bkn', 'wr', 'br', 'wq', 'bq', 'wk', 'bk', 'wb', 'bb']
        black_pieces = ['bp', 'bkn', 'br', 'bq', 'bk', 'bb']
        white_pieces = ['wp', 'wkn', 'wr', 'wq', 'wk', 'wb']
        movable_spots = []        

        if piece_type == 'wp':                       

            a = starting_position[0]
            b = starting_position[1]
            
            if b <Dimensions-1:
                conquerable = [(a-1, b-1), (a-1, b+1)]
            else:
                conquerable = [(a-1, b-1)]

            for x in conquerable:
                if self.board[x[0]][x[1]] in possible_pieces:
                    movable_spots.append(x)                 

            movable = (a-1,b)

            if self.board[movable[0]][movable[1]] == '-':
                movable_spots.append(movable)


            for k,v in self.initial_move_log.items():
                if starting_position == k:
                                    
                    if v == 'False':                                           

                        movable = [(a-1,b),(a-2,b)]
                        
                        for x in movable:
                            
                            if self.board[x[0]][x[1]] == '-':
                                                                
                                movable_spots.append(x)

                        self.initial_move_log[starting_position]='True'             

        if piece_type == 'bp':           

            a = starting_position[0]
            b = starting_position[1]

            if b < Dimensions-1:
                conquerable = [(a+1, b-1), (a+1, b+1)]
            else:
                conquerable = [(a+1, b-1)]    

            for x in conquerable:
                if self.board[x[0]][x[1]] in possible_pieces:
                    movable_spots.append(x)                 

            movable = (a+1,b)

            if self.board[movable[0]][movable[1]] == '-':
                movable_spots.append(movable)

            for k,v in self.initial_move_log.items():
                if starting_position == k:
                                    
                    if v == 'False':                                           

                        movable = [(a+1,b),(a+2,b)]
                        
                        for x in movable:                            
                            
                            if self.board[x[0]][x[1]] == '-':
                                                                
                                movable_spots.append(x)
                        
                        self.initial_move_log[starting_position]='True'

        if piece_type == 'wkn' or piece_type == 'bkn':
            
            possible_spots = [(starting_position[0]+2, starting_position[1]+1), (starting_position[0]+2, starting_position[1]-1),\
                (starting_position[0]-2, starting_position[1]+1), (starting_position[0]-2, starting_position[1]-1),\
                    (starting_position[0]+1, starting_position[1]+2), (starting_position[0]+1, starting_position[1]-2),\
                        (starting_position[0]-1, starting_position[1]+2),(starting_position[0]-1, starting_position[1]-2)]                
            
            for x in possible_spots:
                if board_check(x, Dimensions)==True:

                    if piece_type == 'wkn':
                        
                        if self.board[x[0]][x[1]] in black_pieces or self.board[x[0]][x[1]]== '-':
                            movable_spots.append(x)
                            
                    if piece_type == 'bkn':
                        if self.board[x[0]][x[1]] in white_pieces or self.board[x[0]][x[1]]== '-':
                            movable_spots.append(x)
            
        if piece_type == 'wk' or piece_type == 'bk':
            possible_spots = [(starting_position[0], starting_position[1]+1), (starting_position[0], starting_position[1]-1),\
                (starting_position[0]+1, starting_position[1]), (starting_position[0]-1, starting_position[1]),\
                    (starting_position[0]+1, starting_position[1]+1),(starting_position[0]+1, starting_position[1]-1),\
                        (starting_position[0]-1, starting_position[1]+1),(starting_position[0]-1, starting_position[1]-1)
                    ]
            for x in possible_spots:
                if board_check(x, Dimensions)==True:
                    
                    if piece_type == 'wk':
                        if self.board[x[0]][x[1]] in black_pieces or self.board[x[0]][x[1]]== '-':
                            movable_spots.append(x)
                    if piece_type == 'bk':
                        if self.board[x[0]][x[1]] in white_pieces or self.board[x[0]][x[1]]== '-':
                            movable_spots.append(x)

        if piece_type == 'wr':
            Position = (starting_position[0], starting_position[1])
            movable_spots= create_moves(Position, self.board, Dimensions, 'rook', white_pieces, black_pieces)

        if piece_type =='br':
            Position = (starting_position[0], starting_position[1])
            movable_spots= create_moves(Position, self.board, Dimensions, 'rook', black_pieces, white_pieces)

        if piece_type == 'wb':
            Position = (starting_position[0], starting_position[1])
            movable_spots= create_moves(Position, self.board, Dimensions, 'bishop', white_pieces, black_pieces)

        if piece_type =='bb':
            Position = (starting_position[0], starting_position[1])
            movable_spots= create_moves(Position, self.board, Dimensions, 'bishop', black_pieces, white_pieces)    

        if piece_type == 'wq':
            Position = (starting_position[0], starting_position[1])
            movable_spots= create_moves(Position, self.board, Dimensions, 'queen', white_pieces, black_pieces)
        if piece_type == 'bq':
            Position = (starting_position[0], starting_position[1])
            movable_spots= create_moves(Position, self.board, Dimensions, 'queen', black_pieces, white_pieces)       
        
        if ending_position in movable_spots:
            if self.in_check()==False:
                
                self.board[starting_position[0]][starting_position[1]]='-'
                self.board[ending_position[0]][ending_position[1]] = piece_type

                if self.in_check()==True:

                    self.board[starting_position[0]][starting_position[1]]=piece_type
                    self.board[ending_position[0]][ending_position[1]] = '-'
                    
                    return False

                return True
            
            if self.in_check()==True:    

                self.board[starting_position[0]][starting_position[1]]='-'
                self.board[ending_position[0]][ending_position[1]] = piece_type

                if self.in_check()==True:
                    self.board[starting_position[0]][starting_position[1]]=piece_type
                    self.board[ending_position[0]][ending_position[1]] = '-'
                
                    return False

                return True
        
        else:
            return False       

def load_images():

    pieces = ['br', 'bkn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wkn', 'wb', 'wq', 'wk', 'wp']
    for piece in pieces:
        IMAGES[piece]= p.transform.scale(p.image.load(piece+'.png'), (Sq_Size, Sq_Size))

def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(Dimensions):
        for c in range(Dimensions):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*Sq_Size, r*Sq_Size, Sq_Size, Sq_Size))

def draw_pieces(screen, board):
    
    for r in range(Dimensions):
        for c in range(Dimensions):
            piece = board[r][c]
            if piece != '-':
                screen.blit(IMAGES[piece], p.Rect(c*Sq_Size, r*Sq_Size, Sq_Size, Sq_Size))

def main():
    screen = p.display.set_mode((Width, Height))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = Gamestate()
    load_images()
    
    can_move = False
    pieces = []
    locations = []

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                turn = gs.turn                                     
                
                if can_move == True and gs.turn == 'White':
                                        
                    location = p.mouse.get_pos()
                    col = location[0]//Sq_Size
                    row = location[1]//Sq_Size
                    
                    if gs.board[row][col] not in gs.white_moves:
                        
                        moved_row = locations[-1][0]
                        moved_col = locations[-1][1]

                        starting_position = moved_row,moved_col
                        ending_position = row,col
                        
                        if gs.check_move(starting_position, ending_position)==True:
                                   
                            gs.board[moved_row][moved_col]= '-'      
                            gs.board[row][col]= pieces[-1]
                            
                            can_move = False  
                            gs.turn = 'Black'
                            break  
                        
                        elif gs.check_move(starting_position, ending_position)==False:
                            break              
                                         
                if can_move == True and gs.turn == 'Black':
                                        
                    location = p.mouse.get_pos()
                    col = location[0]//Sq_Size
                    row = location[1]//Sq_Size                                       
                    
                    if gs.board[row][col] not in gs.black_moves:
                        #set empty piece you click to be equal to last piece clicked by black
                        # gs.board[row][col]= pieces[-1]
                        #the last piece in locations will represent the spot on the grid that you want
                        #to move from
                        moved_row = locations[-1][0]
                        moved_col = locations[-1][1]
                        #set the last position that was moved from to an empty spot
                        
                        #Evaluate here, whether or not gs.board[row][col] is a legal move.
                        # given the piece that is actually being moved:  pieces[-1] is the piece type,
                        #evaluate if this piece type from it's current location can move to the location
                        #the player has just clicked on

                        starting_position = moved_row,moved_col
                        ending_position = row,col
                        
                        if gs.check_move(starting_position, ending_position)==True:

                            gs.board[moved_row][moved_col]= '-'
                            gs.board[row][col]= pieces[-1]      
                            
                            can_move = False  
                            gs.turn = 'White'
                            break  
                        
                        elif gs.check_move(starting_position, ending_position)==False:
                            break          

                if turn == 'White':
                    
                    location = p.mouse.get_pos()
                    col = location[0]//Sq_Size
                    row = location[1]//Sq_Size

                    locations.append((row, col))

                    if gs.board[row][col] in gs.white_moves:
                        piece = gs.board[row][col]
                        pieces.append(piece)
                        
                        #until you click on an empty spot, or a non white spot during white's turn,
                        #you append the piece you click on to pieces, and the last piece you clicked on
                        #will be used for reference once it is time to move the piece
                        
                        can_move = True

                if turn == 'Black' :
                    
                    location = p.mouse.get_pos()
                    col = location[0]//Sq_Size
                    row = location[1]//Sq_Size

                    locations.append((row, col))

                    if gs.board[row][col] in gs.black_moves:
                        piece = gs.board[row][col]
                        pieces.append(piece)
                        
                        can_move = True  

        drawBoard(screen)
        draw_pieces(screen, gs.board)        
        
        clock.tick(Max_FPS)
        p.display.flip()       

main() 







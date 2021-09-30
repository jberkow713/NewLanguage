import pygame as p
from pygame.constants import MOUSEBUTTONDOWN
p.init()

Width, Height = 1024, 1024
Dimensions = 16
Sq_Size = int(Width/Dimensions)
Max_FPS = 15
IMAGES = {}



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
        
    def check_move(self, starting_position, ending_position):
        #starting and ending positions are going to be grid locations on the game grid

        possible_moves = []

        piece_type = self.board[starting_position[0]][starting_position[1]]
        
        possible_pieces = ['wp', 'bp', 'wkn', 'bkn', 'wr', 'br', 'wq', 'bq', 'wk', 'bk', 'wb', 'bb']
        
        movable_spots = []

        if piece_type == 'wp':           

            a = starting_position[0]
            b = starting_position[1]

            conquerable = [(a-1, b-1), (a-1, b+1)]

            for x in conquerable:
                if self.board[x[0]][x[1]] in possible_pieces:
                    movable_spots.append(x)                 


            for k,v in self.initial_move_log.items():
                if starting_position == k:
                                      
                    if v == 'False':                                           

                        movable = [(a-1,b),(a-2,b)]
                           
                        for x in movable:
                            
                            print(self.board[x[0]][x[1]])
                            if self.board[x[0]][x[1]] == '-':
                                                                
                                movable_spots.append(x)
                        self.initial_move_log[starting_position]='True'
                    else:
                        movable = (a-1,b)
                        if self.board[movable[0]][movable[1]] not in possible_pieces:
                            movable_spots.append(movable) 
        if piece_type == 'bp':           

            a = starting_position[0]
            b = starting_position[1]

            conquerable = [(a+1, b-1), (a+1, b+1)]

            for x in conquerable:
                if self.board[x[0]][x[1]] in possible_pieces:
                    movable_spots.append(x)                 


            for k,v in self.initial_move_log.items():
                if starting_position == k:
                                      
                    if v == 'False':                                           

                        movable = [(a+1,b),(a+2,b)]
                           
                        for x in movable:
                            
                            print(self.board[x[0]][x[1]])
                            if self.board[x[0]][x[1]] == '-':
                                                                
                                movable_spots.append(x)
                        self.initial_move_log[starting_position]='True'
                else:
                    movable = (a+1,b)
                    if self.board[movable[0]][movable[1]] not in possible_pieces:
                        movable_spots.append(movable)            

        if ending_position in movable_spots:
            return True
        else:
            return False     

                        








                        





        #need to take the piece type, piece position, and determine where it can move

        #going to use current board state to determine moving

        
     

        

        

        #for pawns initially, if their current row is their starting row, they are allowed
        # to move 2 spots forward...we can do this by adding a has_moved variable to each pawn,
        # so once it has initially moved, it can no longer move 2 spots

        #need to check if pawns, king, or rooks have moved, use self.initial_move_log dictionary for this


# g = Gamestate()
# print(g.board[0][0])

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
    print(gs.initial_move_log)
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

                # print(gs.turn)
                # print(can_move)                       
                
                if can_move == True and gs.turn == 'White':
                                        
                    location = p.mouse.get_pos()
                    col = location[0]//Sq_Size
                    row = location[1]//Sq_Size
                    
                    if gs.board[row][col] not in gs.white_moves:
                        # gs.board[row][col]= pieces[-1]

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






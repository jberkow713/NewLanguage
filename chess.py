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

        #eventually want to highlight all possible moves you can make with a piece

        #check if piece being moved from starting position, can move to the ending position
        #this means we need to get all possible moves for the piece being moved at the starting position
        #check if the ending position is one of these spots

        #7 types of pieces, bp, wp, (wr,br), (wq, bq), (wk, bk), (wb, bb), (wkn, bkn)
        #pawns go in different directions, every other piece can move wherever based on its type
        #need functions to check possible moves of each type based on their type

        #first we want to check in general all the moves it could go to
        #then we want to check if one of its own pieces is either in the way of its path, or the 
        #ending of its path
        #if that is not the case, we want to check if opponent's piece is in the path...at which point
        #it can also not move to the spot by going through opponents piece...with the exception of the knight

        #basically if spots are being blocked in the path, then all possible spots it could have moved to
        #beyond that point, will not exist...aside from the knight

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

                print(gs.turn)
                print(can_move)                       
                
                if can_move == True and gs.turn == 'White':
                                        
                    location = p.mouse.get_pos()
                    col = location[0]//Sq_Size
                    row = location[1]//Sq_Size
                    
                    if gs.board[row][col] not in gs.white_moves:
                        gs.board[row][col]= pieces[-1]
                        moved_row = locations[-1][0]
                        moved_col = locations[-1][1]

                        starting_position = gs.board[moved_row][moved_col]
                        ending_position = gs.board[row][col]
                        
                        if gs.check_move(starting_position, ending_position)==True:

                            gs.board[moved_row][moved_col]= '-'      

                            
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
                        gs.board[row][col]= pieces[-1]
                        #the last piece in locations will represent the spot on the grid that you want
                        #to move from
                        moved_row = locations[-1][0]
                        moved_col = locations[-1][1]
                        #set the last position that was moved from to an empty spot
                        
                        #Evaluate here, whether or not gs.board[row][col] is a legal move.
                        # given the piece that is actually being moved:  pieces[-1] is the piece type,
                        #evaluate if this piece type from it's current location can move to the location
                        #the player has just clicked on

                        starting_position = gs.board[moved_row][moved_col]
                        ending_position = gs.board[row][col]
                        
                        if gs.check_move(starting_position, ending_position)==True:

                            gs.board[moved_row][moved_col]= '-'      

                            
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






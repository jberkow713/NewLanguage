import pygame as p
from pygame.constants import MOUSEBUTTONDOWN
p.init()

class Gamestate():
    def __init__(self):
        self.board = [
            ['br','br',  'bkn','bkn', 'bb','bb', 'bq','bq', 'bk','bk', 'bb', 'bb', 'bkn','bkn', 'br', 'br'],
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
            ['wr','wr',  'wkn','wkn', 'wb','wb', 'wq','wq', 'wk','wk', 'wb', 'wb', 'wkn','wkn', 'wr', 'wr'],
            

                    ]
        self.turn = 'White'
        self.white_moves = ['wp', 'wr', 'wkn', 'wb', 'wq', 'wk']
        self.black_moves = ['bp', 'br', 'bkn', 'bb', 'bq', 'bk']
        self.move_log = []            

# g = Gamestate()
# print(g.board[0][0])

Width, Height = 1024, 1024
Dimensions = 16
Sq_Size = int(Width/Dimensions)
Max_FPS = 15
IMAGES = {}



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
                        gs.board[moved_row][moved_col]= '-'                              

                        
                        can_move = False  
                        gs.turn = 'Black'
                        break     
                                         
                if can_move == True and gs.turn == 'Black':
                                        
                    location = p.mouse.get_pos()
                    col = location[0]//Sq_Size
                    row = location[1]//Sq_Size
                    #Evaluate here, whether or not gs.board[row][col] is a legal move, given the 
                    #piece that is actually being moved:  pieces[-1] is the piece type,
                    #evaluate if this piece type from it's current location can move to the location
                    #the player has just clicked on
                    
                    if gs.board[row][col] not in gs.black_moves:
                        #set empty piece you click to be equal to last piece clicked by black
                        gs.board[row][col]= pieces[-1]
                        #the last piece in locations will represent the spot on the grid that you want
                        #to move from
                        moved_row = locations[-1][0]
                        moved_col = locations[-1][1]
                        #set the last position that was moved from to an empty spot
                        gs.board[moved_row][moved_col]= '-'                              

                        
                        can_move = False  
                        gs.turn = 'White'
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






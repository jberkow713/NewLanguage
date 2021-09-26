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
                        gs.board[row][col]= current 
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
                    
                    if gs.board[row][col] not in gs.black_moves:
                        gs.board[row][col]= current 
                        moved_row = locations[-1][0]
                        moved_col = locations[-1][1]
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
                        current = pieces[-1]
                        can_move = True

                if turn == 'Black' :
                    
                    location = p.mouse.get_pos()
                    col = location[0]//Sq_Size
                    row = location[1]//Sq_Size

                    locations.append((row, col))

                    if gs.board[row][col] in gs.black_moves:
                        piece = gs.board[row][col]
                        pieces.append(piece)
                        current = pieces[-1]
                        can_move = True        
               
                


        drawBoard(screen)
        draw_pieces(screen, gs.board)        
        
        clock.tick(Max_FPS)
        p.display.flip()         

main() 






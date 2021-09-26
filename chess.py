import pygame as p
p.init()

class Gamestate():
    def __init__(self):
        self.board = [
            ['br', 'bkn', 'bb', 'bq', 'bk', 'bb', 'bkn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['wr', 'wkn', 'wb', 'wq', 'wk', 'wb', 'wkn', 'wr'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],

                    ]
        self.turn = 'White'
        self.move_log = []            

# g = Gamestate()
# print(g.board[0][0])

Width, Height = 1024, 1024
Dimensions = 8
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
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawBoard(screen)
        draw_pieces(screen, gs.board)        
        
        clock.tick(Max_FPS)
        p.display.flip()         

main() 






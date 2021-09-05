import pygame
import random
import sys
import math
from pygame.locals import(
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_ESCAPE, KEYDOWN, QUIT, K_RETURN
)

width = 1200
height = 800
origin = 0
margin = 25
top_left = origin+margin, origin+margin
top_right = width-margin, origin+margin
bottom_left = origin+margin, height-margin
bottom_right = width-margin, height-margin
 

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
screen.fill(WHITE)
pygame.draw.lines(screen, BLACK, False, [(top_left), (top_right), (bottom_right), (bottom_left), (top_left)], 4)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    pygame.display.flip()
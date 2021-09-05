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
 
FPS =60
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
pygame.display.set_caption("Wallsmash")

#Need 3 classes:
#Class for the movable rectangle
#Class for the ball
#Class for the rectangle that will be smashed

class mover:
    def __init__(self):
        self.x = width/2
        self.y = 733
        self.speed = 10
        pygame.draw.rect(screen,BLUE,(self.x,self.y,100,5)) 
    
    def update(self):
        
        keys = pygame.key.get_pressed()        

        if keys[pygame.K_RIGHT]:
            pygame.draw.rect(screen,WHITE,(self.x,self.y,100,5)) 
            self.new_x = self.x + self.speed 
            if self.new_x >25 and self.new_x < 1075:
                self.x =self.new_x             

        elif keys[pygame.K_LEFT]:
            pygame.draw.rect(screen,WHITE,(self.x,self.y,100,5)) 
            self.new_x = self.x - self.speed
            if self.new_x >25 and self.new_x < 1075:
                self.x =self.new_x            
        
        pygame.draw.rect(screen,BLUE,(self.x,self.y,100,5))     
        
Mover = mover()

running = True
while running:
    
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if event.type == pygame.KEYDOWN:
                        
        Mover.update()          
    pygame.display.flip()
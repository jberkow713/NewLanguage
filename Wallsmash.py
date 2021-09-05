import pygame
import random
import sys
import math
from pygame.locals import(
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_ESCAPE, KEYDOWN, QUIT, K_RETURN
)
pygame.init()

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

class Ball():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        pygame.draw.circle(screen,self.color,(self.x,self.y),15)     
    
    def move(self):
        speed = 5
        pygame.draw.circle(screen,WHITE,(self.x,self.y),15)
        
        self.y +=speed
        
        pygame.draw.circle(screen,self.color,(self.x,self.y),15)
  
        

class Rectangles():
    def __init__(self):
        self.positions = []
        self.draw()
    def draw(self):
        
        x = 100
        y = 100
        length = 75
        width = 25
        colors = [RED, GREEN, BLUE, PURPLE]
        index = 0

        while y <=201:
            #tuple of tuples, representing the drawing coordinates, then the xrange, and yrange of rectangles
            #appended to the positions list, to be referenced for when the ball hits the rectangles
            a = round(x,2)
            b = round(y,2)
            c = a+length
            d = b+width
            self.positions.append(((a,b),(a,c),(b,d))) 
            pygame.draw.rect(screen,colors[index],(a,b,length,width))

            x +=length+.05
            index +=1
            if index >3:
                index = 0
            if x >=1050:
                y+=width+.2
                x = 100

#TODO create ball class, movement of ball, bounce off Mover, hit rectangles, update rectangles, etc
#can now reference the rectangle positions within the ball class to update rectangles
#can now reference the mover position to check how and where ball bounces

Rectangle = Rectangles()
print(Rectangle.positions)
Ball = Ball(width/2, height/2, BLACK)
Mover = mover()


running = True
while running:
    
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if event.type == pygame.KEYDOWN:
                        
        Mover.update()
    
    Ball.move()
       
    

    pygame.display.flip()
import pygame 
import random
from enum import Enum
from collections import namedtuple
from time import sleep 

pygame.init()
font = pygame.font.Font('./arial.ttf' , 20)

class directions(Enum):
    RIGHT = 1
    LEFT = 2 
    UP = 3 
    DOWN = 4

point = namedtuple('point' , 'x , y')

WHITE = (255, 255, 255)
BLUE1 = (0,0,225)
BLUE2 = (0,100,225)
RED2 = (200, 0, 0)
RED1 = (200, 100, 20)
GREEN = (50,100,50)

BLOCK_SIZE = 25
SPEED = 5


class Snakgame:
    
    def __init__(self,h=800,w=700):
        self.w = w 
        self.h = h
        
        #display
        self.display = pygame.display.set_mode((self.h , self.w))
        pygame.display.set_caption('snak_game')
        self.clock = pygame.time.Clock()
        
        #game state 
        self.direction = directions.RIGHT
        self.head = point(self.w/2 , self.h/2)
        self.snak = [self.head , point(self.head.x-BLOCK_SIZE,self.head.y),
                    point(self.head.x-(2*BLOCK_SIZE),self.head.y) ]
        
        self.score = 0 
        self.food = None
        self.place_food()  
    def place_food(self):
        x = random.randint(0 , 800-25) //25 *25
        y = random.randint(0 ,700-25)  //25 * 25
        self.food = point(x, y)
        if self.snak in self.food:
            self.place_food()
            
    def play_step(self):
        #user input 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = directions.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = directions.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = directions.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = directions.DOWN   
                         
        #move 
        self.move(self.direction)
        self.snak.insert(0, self.head)
        
        #check the game over 
        game_over = False
        if self._is_collection():
            game_over = True
            return game_over, self.score
        
        #place new food 
        if self.head == self.food:
            self.score += 1
            self.place_food()
            self.sp_plus(1)
           
        else:
            self.snak.pop()
        
            
        #update ui and clock
        self.clock.tick(SPEED)    
        self._ui_update()        
        
        
           
        # return game over and score
        return game_over, self.score
        
    
    def sp_plus(self, x):
        yield  x + SPEED   
        print(SPEED)
    
#    def plus(self):
#        while True:
#            self.sp_plus = SPEED + 1 
#            print (SPEED)
#            while True:
#                sleep(5)
#                return self.sp_plus
          
                        
    def _is_collection(self):
        
        #if it hiys the border 
        if self.head.x > self.w + 3*(BLOCK_SIZE) or self.head.x < 0 or self.head.y > self.h - 5*(BLOCK_SIZE) or self.head.y < 0:
            return True
        
        #if it hits it self
        if self.head in self.snak[1:]:
            return True
    
        return False
        
    
    def _ui_update(self):
        self.display.fill(GREEN)
        
        for pt in self.snak:
            pygame.draw.rect(self.display, RED1 ,pygame.Rect(pt.x , pt.y , BLOCK_SIZE , BLOCK_SIZE))
            pygame.draw.rect(self.display, RED2 ,pygame.Rect(pt.x+5 , pt.y+5 , 15 , 15))
        
            pygame.draw.rect(self.display, BLUE1 ,pygame.Rect(self.food.x , self.food.y , BLOCK_SIZE , BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2 ,pygame.Rect(self.food.x+5 , self.food.y+5 , 15 , 15))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text , [0 , 0])
        pygame.display.flip()
        
    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == directions.RIGHT:
            x += BLOCK_SIZE
        elif direction == directions.LEFT:
            x -= BLOCK_SIZE
        elif direction == directions.DOWN:
            y += BLOCK_SIZE
        elif direction == directions.UP:
            y -= BLOCK_SIZE  
            
        self.head = point(x, y)
              
        
if __name__ == '__main__':
    game = Snakgame()   
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        
    #brake if game over 
        if game_over == True:
            break
print('final score:', score)
        
pygame.quit()        

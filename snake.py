from helpers import *
import time
import renderer
import random

BG_COLOR = WHITE
SNAKE_COLOR = DARK_GREEN
APPLE_COLOR = RED
SNAKE_HEAD = MOSS

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

class snakeBoard:
    def __init__(self, boardSize = 10, scale = 2):
        self.boardSize = boardSize
        self.scale = scale
        self.snake = [(0,0)]
        self.apple = (4,0)
        self.display = renderer.Display(scale=self.scale)
        self.lastTickTime = time.perf_counter()
        self.tickDelay = 200 #in milliseconds
        self.nextDir = RIGHT
        self.dir = RIGHT
        
        self.extend = False
        self.directionDict = {
            UP:(0,-1),
            DOWN:(0,1),
            RIGHT:(1,0),
            LEFT:(-1,0)
        }
        
    def randomizeApple(self):
        while True:
            newX = random.randint(0, self.boardSize - 1)
            newY = random.randint(0, self.boardSize - 1)
            if (newX, newY) not in self.snake:
                self.apple = (newX, newY)
                break
    
    def render(self):
        for i, snakePos in enumerate(self.snake):
            if i == (len(self.snake) - 1):   
                self.display.draw(SNAKE_HEAD, snakePos)
            else:
                self.display.draw(SNAKE_COLOR, snakePos)
        self.display.draw(APPLE_COLOR, self.apple)
    
    def update(self):
        dx, dy = self.directionDict[self.nextDir]
        self.dir = self.nextDir
        
        x, y = self.snake[-1]
        newPos = (x + dx, y + dy)
        print(newPos)
        
        self.snake.append(newPos)
        if newPos == self.apple:
            self.extend = True
            self.randomizeApple()
        
        if not self.extend:
            del self.snake[0]
        else:
            self.extend = False
    
    def runGame(self):
        self.display.init()
        while True:
            timePassed = time.perf_counter() - self.lastTickTime
            if timePassed >= (self.tickDelay/1000):
                self.update()
                self.lastTickTime = time.perf_counter()
                self.display.fill(BG_COLOR)
                self.render()
                self.display.render()
            
            keys = self.display.getKeys()
            if "q" in keys:
                break
            
            direction = -1
            if "w" in keys:
                direction = UP
            if "a" in keys:
                direction = LEFT
            if "s" in keys:
                direction = DOWN
            if "d" in keys:
                direction = RIGHT
            
            if direction != -1:
                if ((direction + 2) % 4) != self.dir:
                    self.nextDir = direction
            
        self.display.closeDisplay()
                
                
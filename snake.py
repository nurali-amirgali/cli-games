from helpers import *
import time
import renderer

BG_COLOR = WHITE
SNAKE_COLOR = GREEN
APPLE_COLOR = RED

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

class snakeBoard:
    def __init__(self, boardSize = 10):
        self.boardSize = boardSize
        self.scale = 2
        self.snake = [(0,0)]
        self.apple = (4,0)
        self.display = renderer.Display()
        self.lastTickTime = time.perf_counter()
        self.tickDelay = 400 #in milliseconds
        self.nextDir = RIGHT
        self.dir = RIGHT
        
        self.extend = False
        self.directionDict = {
            UP:(0,-1),
            DOWN:(0,1),
            RIGHT:(1,0),
            LEFT:(-1,0)
        }
    
    def render(self):
        for snakePos in self.snake:
            self.display.draw(SNAKE_COLOR, snakePos)
        self.display.draw(APPLE_COLOR, self.apple)
    
    def update(self):
        dx, dy = self.directionDict[self.nextDir]
        x, y = self.snake[-1]
        print(x, y)
        self.snake.append((x + dx, y + dy))
        if not self.extend:
            del self.snake[0]
    
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
                if ((direction + 2) % 3) != self.dir:
                    self.nextDir = direction
            
        self.display.closeDisplay()
                
                
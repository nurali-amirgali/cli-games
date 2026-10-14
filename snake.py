from helpers import *
import time
import renderer

BG_COLOR = WHITE
SNAKE_COLOR = GREEN
APPLE_COLOR = RED

class snakeBoard:
    def __init__(self, boardSize = 10):
        self.boardSize = boardSize
        self.scale = 2
        self.snake = [(0,0)]
        self.apple = (4,0)
        self.display = renderer.Display()
        self.lastTickTime = time.perf_counter()
        self.tickDelay = 400 #in milliseconds
    
    def render(self):
        for snakePos in self.snake:
            self.display.draw(SNAKE_COLOR, snakePos)
        self.display.draw(APPLE_COLOR, self.apple)
    
    def runGame(self):
        self.display.init()
        while True:
            timePassed = time.perf_counter() - self.lastTickTime
            if timePassed >= (self.tickDelay/1000):
                self.lastTickTime = time.perf_counter()
                self.display.fill(BG_COLOR)
                self.render()
                self.display.render()
            
            keys = self.display.getKeys()
            if "q" in keys:
                break
        self.display.closeDisplay()
                
                
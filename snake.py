from helpers import *

BG_COLOR = WHITE
SNAKE_COLOR = GREEN
APPLE_COLOR = RED

class snakeBoard:
    def __init__(self, display, boardSize = 10):
        self.boardSize = boardSize
        self.scale = 2
        self.snake = [(0,0)]
        self.apple = (4,0)
        self.display = display
    
    def render(self):
        for snakePos in self.snake:
            self.display.draw(SNAKE_COLOR, snakePos)
        self.display.draw(APPLE_COLOR, self.apple)
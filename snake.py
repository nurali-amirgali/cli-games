from helpers import *

BG_COLOR = WHITE_BG
SNAKE_COLOR = GREEN_BG
APPLE_COLOR = RED_BG

class snakeBoard:
    def __init__(self, boardSize = 10):
        self.boardSize = boardSize
        self.scale = 2
        self.snake = [(0,0)]
        self.apple = (4,0)
    
    def render(self):
        for row in range(self.boardSize):
            for _ in range(self.scale):
                for col in range(self.boardSize):
                    for _ in range(self.scale * 2):
                        if (col, row) in self.snake:
                            color = SNAKE_COLOR
                        elif (col, row) == self.apple:
                            color = APPLE_COLOR
                        else:
                            color = BG_COLOR
                        print(f"{color} ", end='')
                print(RESET)
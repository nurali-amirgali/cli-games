from helpers import *

class snakeBoard:
    def __init__(self, boardSize = 10):
        self.boardSize = boardSize
        self.tiles = [[0] * 10 for i in range(10)]
        self.tiles[4][4] = 1
        self.scale = 1 #this means that
    
    def render(self):
        for row in range(self.boardSize):
            for _ in range(self.scale):
                for col in range(self.boardSize):
                    for _ in range(self.scale * 2):
                        value = self.tiles[row][col]
                        if value == 0:
                            print(f"{RED}█", end='')
                        else:
                            print(f"{GREEN}█", end='')
                print()
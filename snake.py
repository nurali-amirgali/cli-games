from helpers import *
import time
import renderer
import random
import math

BG_COLOR = WHITE
SNAKE_COLOR = DARK_GREEN
APPLE_COLOR = RED
SNAKE_HEAD = MOSS
TOP_BAR_BG = BLACK
TOP_BAR_TEXT = WHITE_TEXT

DEATH_TOP_BG = "\033[48;5;160m"
DEATH_TOP_TEXT = WHITE_TEXT
DEATH_BG_COLOR = "\033[48;5;252m"
DEATH_SNAKE_COLOR = "\033[48;5;243m"
DEATH_APPLE_COLOR = "\033[48;5;248m"
DEATH_SNAKE_HEAD = "\033[48;5;236m"

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

class snakeBoard:
    def __init__(self, boardSize = 10, scale = 1):
        self.boardSize = boardSize
        self.scale = scale
        self.snake = [(0,0)]
        self.apple = (4,0)
        self.display = renderer.Display(scale = self.scale, y = 1)
        self.lastTickTime = time.perf_counter()
        self.tickDelay = 200 #in milliseconds
        self.nextDir = RIGHT
        self.dir = RIGHT
        
        self.isImprovement = False
        self.score = 0
        self.bestScore = 0
        self.gameOver = False
        self.extend = False
        self.startScreen = True
        self.directionDict = {
            UP:(0,-1),
            DOWN:(0,1),
            RIGHT:(1,0),
            LEFT:(-1,0)
        }
    
    def renderScore(self):
        self.display.cursorHome()
        if self.gameOver:
            scoreText = "GAME OVER"
        elif self.startScreen:
            scoreText = "PRESS TO START"
        else:
            scoreText = f"Score: {self.score}"
        textLen = max((self.boardSize * self.scale * 2) - len(scoreText), 0)
        text = (" " * math.floor(textLen/2)) + scoreText + (" " * math.ceil(textLen/2))
        
        bg = (TOP_BAR_BG if not self.gameOver else DEATH_TOP_BG)
        textColor = (TOP_BAR_TEXT if not self.gameOver else DEATH_TOP_TEXT)
        textColors = bg + BOLD_TEXT + textColor
        print(textColors + text + RESET, end='')
            
        
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
                self.display.draw(SNAKE_HEAD if not self.gameOver else DEATH_SNAKE_HEAD, snakePos)
            else:
                self.display.draw(SNAKE_COLOR if not self.gameOver else DEATH_SNAKE_COLOR, snakePos)
        self.display.draw(APPLE_COLOR if not self.gameOver else DEATH_APPLE_COLOR, self.apple)
    
    def printLabel(self, text, color, bgColor, width):
        textLen = max(width - len(text), 0)
        text = (" " * math.floor(textLen/2)) + text + (" " * math.ceil(textLen/2))
        
        textColors = bgColor + BOLD_TEXT + color
        print(textColors + text + RESET)
    
    def update(self):
        dx, dy = self.directionDict[self.nextDir]
        self.dir = self.nextDir
        
        x, y = self.snake[-1]
        newPos = (x + dx, y + dy)
        
        if newPos[0] < 0 or newPos[0] > (self.boardSize - 1) or newPos[1] < 0 or newPos[1] > (self.boardSize - 1):
            self.gameOver = True
            return
        
        if newPos in self.snake:
            self.gameOver = True
            return
        
        self.snake.append(newPos)
        if newPos == self.apple:
            self.extend = True
            self.randomizeApple()
            self.score += 1
        
        if not self.extend:
            del self.snake[0]
        else:
            self.extend = False
    
    def reset(self):
        self.snake = [(0,0)]
        self.apple = (4,0)
        self.lastTickTime = time.perf_counter()
        self.tickDelay = 200 #in milliseconds
        self.nextDir = RIGHT
        self.dir = RIGHT
        self.isImprovement = False
        
        self.score = 0
        self.gameOver = False
        self.extend = False
        self.startScreen = True
        
    def runGame(self):
        self.display.init()
        while True:
            timePassed = time.perf_counter() - self.lastTickTime
            if timePassed >= (self.tickDelay/1000):
                if not self.gameOver and not self.startScreen:
                    self.update()
                self.lastTickTime = time.perf_counter()
                self.display.fill(BG_COLOR if not self.gameOver else DEATH_BG_COLOR)
                self.renderScore()
                self.render()
                self.display.render()
                
                if self.gameOver:
                    if self.score > self.bestScore:
                        self.bestScore = self.score
                        self.isImprovement = True
                    
                    scoreColor = GREEN_TEXT if self.isImprovement else RED_TEXT
                    self.printLabel(f"SCORE: {self.score}", scoreColor, BLACK, (self.boardSize * self.scale * 2))
                    self.printLabel(f"BEST: {self.bestScore}", CYAN_TEXT, BLACK, (self.boardSize * self.scale * 2))
                    print(f"press anything to restart\nor press Q to exit")
                else:
                    print("\033[J", end="", flush=True)
            
            keys = self.display.getKeys()
            if "q" in keys:
                break
            
            if keys:
                if self.gameOver:
                    self.reset()
                    continue
                elif self.startScreen:
                    self.startScreen = False
            
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
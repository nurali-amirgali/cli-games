from helpers import *
import time
import renderer
import random
import math

BG_COLOR = WHITE


class paddleBoard:
    def __init__(self, boardWidth = 40, boardHeight = 20, scale = 1):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.scale = scale
        self.display = renderer.Display(boardHeight = boardHeight, boardWidth = boardWidth, scale = self.scale, y = 1)
        self.lastTickTime = time.perf_counter()
        self.tickDelay = 10 #in milliseconds
        
        self.paddleHeight = 7
        self.paddleWidth = 1
        
        self.paddleUserY = 10
        self.paddleBotY = 10
        self.paddleOffsetX = 2
        
        self.ballPos = (round(boardWidth/2), round(boardHeight/2))
        self.ballVelocity = (1, 0)
    
    def renderPaddle(self):
        for x in range(self.paddleWidth):
            for y in range(self.paddleHeight):
                drawPos = (x + self.paddleOffsetX, y + self.paddleUserY)
                self.display.draw(BLACK, drawPos)
    
    def renderBall(self):
        pass
    
    def render(self):
        self.renderPaddle()
    
    def update(self):
        pass
    
    def reset(self):
        pass
        
    def runGame(self):
        self.display.init()
        while True:
            timePassed = time.perf_counter() - self.lastTickTime
            if timePassed >= (self.tickDelay/1000):
                self.display.fill(BG_COLOR)
                
                self.render()
                
                self.display.render()
            
            keys = self.display.getKeys()
            if "q" in keys:
                break
        
        self.display.closeDisplay()     
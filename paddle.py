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
        
        self.lastKeyTime = time.perf_counter()
        self.currentMovement = 0 # 1 is up and -1 is down
        self.holdTime = 200 #in milliseconds
        self.repeatTime = 100
        self.continueHold = False
        self.nextRepeat = 0
        
        self.paddleHeight = 7
        self.paddleWidth = 1
        
        self.paddleUserY = 10
        self.paddleBotY = 10
        self.paddleOffsetX = 2
        self.paddleSpeed = 0.1
        
        self.ballPos = (round(boardWidth/2), round(boardHeight/2))
        self.ballVelocity = (0.01, 0.01)
        self.ballSpeed = 0.01
        
        self.randomizeBallVelocity()
    
    def randomizeBallVelocity(self):
        angle = random.uniform(0, 2 * math.pi)

        dx = math.cos(angle) * self.ballSpeed
        dy = math.sin(angle) * self.ballSpeed
        
        self.ballVelocity = (dx, dy)
    
    def renderPaddle(self):
        for x in range(self.paddleWidth):
            for y in range(self.paddleHeight):
                drawPos = (round(x + self.paddleOffsetX), round(y + self.paddleUserY))
                self.display.draw(MOSS, drawPos)
    
    def renderBall(self):
        drawPos = (round(self.ballPos[0]), round(self.ballPos[1]))
        self.display.draw(RED, drawPos)
    
    def render(self):
        self.renderPaddle()
        self.renderBall()
        
    def updateBall(self):
        x, y = self.ballPos
        dx, dy = self.ballVelocity
        self.ballPos = (x + dx, y + dy)
    
    def update(self):
        pass
    
    def reset(self):
        pass
        
    def runGame(self):
        self.display.init()
        while True:
            timePassed = time.perf_counter() - self.lastTickTime
            if timePassed >= (self.tickDelay/1000):
                self.updateBall()
                
                if self.currentMovement == 1:
                    self.paddleUserY =  max(self.paddleUserY - self.paddleSpeed, 0)
                elif self.currentMovement == -1:
                    self.paddleUserY =  min(self.paddleUserY + self.paddleSpeed, (self.boardHeight - self.paddleHeight))
                
                self.display.fill(BG_COLOR)
                                
                self.render()
                
                self.display.render()
            
            keys = self.display.getKeys()
            if "q" in keys:
                break
            
            if "w" in keys or "UP" in keys:
                self.lastKeyTime = time.perf_counter()
                if not self.continueHold:
                    self.continueHold = True
                    self.nextRepeat = self.holdTime
                else:
                    if self.currentMovement == 1:
                        self.nextRepeat = self.repeatTime
                    else:
                        self.nextRepeat = self.holdTime
                self.currentMovement = 1
            if "s" in keys or "DOWN" in keys:
                self.lastKeyTime = time.perf_counter()
                if not self.continueHold:
                    self.continueHold = True
                    self.nextRepeat = self.holdTime
                else:
                    if self.currentMovement == -1:
                        self.nextRepeat = self.repeatTime
                    else:
                        self.nextRepeat = self.holdTime
                self.currentMovement = -1
            
            if self.continueHold:
                timePassed = time.perf_counter() - self.lastKeyTime
                if timePassed >= (self.nextRepeat/1000):
                    self.continueHold = False
                    self.currentMovement = 0
                    self.nextRepeat = 0
        
        self.display.closeDisplay()     
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
        self.currentMovement = 0 # 1 is up and -1 is down
        self.speedIncrease = 1.05
        
        self.restartDelay = 2 #in seconds
        self.restartTimer = time.perf_counter()
        self.controlsLock = False
        
        self.paddleHeight = 6
        self.paddleWidth = 1
        
        self.paddleUserY = (self.boardHeight/2) - round(self.paddleHeight/2)
        self.paddleBotY = (self.boardHeight/2) - round(self.paddleHeight/2)
        self.paddleOffsetX = 2
        self.paddleSpeed = 0.2
        
        self.ballPos = (round(boardWidth/2), round(boardHeight/2))
        self.ballVelocity = (0.01, 0.01)
        self.ballSpeed = 0.3
        
        self.userPaddleTiles = []
        self.botPaddleTiles = []
        
        self.lives = (3,3)
        self.showBall = True
        
        self.waitForInput = True
        self.gameOver = False
        self.sideLost = 0
                
        self.randomizeBallVelocity()
    
    def randomizeBallVelocity(self):
        angle = random.uniform(-30, 30)

        if random.randint(0, 1) == 0:
            angle += 180

        angleRad = math.radians(angle)

        dx = math.cos(angleRad) * self.ballSpeed
        dy = math.sin(angleRad) * self.ballSpeed
        
        self.ballVelocity = (dx, dy)
    
    def drawPaddle(self, x, y):
        tiles = []
        for posX in range(self.paddleWidth):
            for posY in range(self.paddleHeight):
                drawX = posX + x
                drawY = posY + y
                drawPos = (round(drawX), round(drawY))
                tiles.append(drawPos)
        return tiles
    
    def printLabel(self, text, color, bgColor, width):
        self.display.cursorGoToY(0)
        textLen = max(width - len(text), 0)
        text = (" " * math.floor(textLen/2)) + text + (" " * math.ceil(textLen/2))
        
        textColors = bgColor + BOLD_TEXT + color
        print(textColors + text + RESET)
    
    def renderHealth(self):
        self.display.cursorGoToY(0)
        
        padLen = ((self.boardWidth * 2) - 17)/2
        HealthUserLen = (3 - self.lives[0]) * 2
        HealthBotLen = (3 - self.lives[1]) * 2
        
        healthBarUser = BLACK + (HealthUserLen * " ") + RED + ((self.lives[0] * 2) * " ")
        healthBarBot = RED + ((self.lives[1] * 2) * " ") + BLACK + (HealthBotLen * " ")
        centerBar = f"{WHITE_TEXT}{BLACK} {self.lives[0]}-{self.lives[1]} "
        
        text = (BRIGHT_BLACK + " " * math.floor(padLen)) + (healthBarUser + centerBar + healthBarBot) + (BRIGHT_BLACK + " " * math.ceil(padLen))
        print(text + RESET)
        
    def renderPaddles(self):
        self.userPaddleTiles = self.drawPaddle(self.paddleOffsetX, self.paddleUserY)
        self.botPaddleTiles = self.drawPaddle(self.boardWidth - self.paddleOffsetX - self.paddleWidth, self.paddleBotY)
        for tile in self.userPaddleTiles:
            self.display.draw(RED if self.sideLost == -1 else MOSS, tile)

        for tile in self.botPaddleTiles:
            self.display.draw(RED if self.sideLost == 1 else MOSS, tile)
        
    def renderBall(self):
        drawPos = (round(self.ballPos[0]), round(self.ballPos[1]))
        self.display.draw(RED, drawPos)
    
    def render(self):
        if self.gameOver:
            wonName = "BOT" if self.lives[0] == 0 else "YOU"
            self.printLabel(f"{wonName} WON! press to restart", WHITE_TEXT, RED, self.boardWidth * 2)
        else:
            self.renderHealth()
        self.renderPaddles()
        if self.showBall:
            self.renderBall()
    
    def isTouchingPaddle(self, x, y):
        tile = (round(x), round(y))
        return tile in self.userPaddleTiles or tile in self.botPaddleTiles
        
    def updateBall(self):
        x, y = self.ballPos
        dx, dy = self.ballVelocity
        
        newX = x + dx
        if self.isTouchingPaddle(newX, y):
            dx = -dx * self.speedIncrease
            newX = x + dx
        
        newY = y + dy
        if self.isTouchingPaddle(x, newY):
            dy = -dy * self.speedIncrease
            newY = y + dy
        
        if newX < 0:
            newX, dx = 0, abs(dx)
            self.showBall = False
            self.controlsLock = True
            self.sideLost = -1
            self.lives = (self.lives[0] - 1, self.lives[1] )
            self.restartTimer = time.perf_counter()
            
        elif newX > self.boardWidth - 1:
            newX, dx = self.boardWidth - 1, -abs(dx)
            self.showBall = False
            self.controlsLock = True
            self.sideLost = 1
            self.lives = (self.lives[0], self.lives[1] - 1)
            self.restartTimer = time.perf_counter()
            
        if newY < 0:
            newY, dy = 0, abs(dy)
        elif newY > self.boardHeight - 1:
            newY, dy = self.boardHeight - 1, -abs(dy)

        self.ballPos = (newX, newY)
        self.ballVelocity = (dx, dy)
    
    def updateGameState(self):
        if self.sideLost != 0 and not self.gameOver:
            if (time.perf_counter() - self.restartTimer) >= self.restartDelay:
                self.reset()
                self.waitForInput = True
                self.controlsLock = False
        if 0 in self.lives:
            self.gameOver = True
            self.controlsLock = True
            self.waitForInput = True
    
    def updateBot(self):
        if self.ballVelocity[0] > 0:
            target = self.ballPos[1]
        else:
            target = round(self.boardHeight/2)
        delta = (self.paddleBotY - target) + round(self.paddleHeight/2)
        if self.ballVelocity[0] < 0:
            return
        if delta > 0:
            self.paddleBotY =  max(self.paddleBotY - (self.paddleSpeed * 0.8), 0) #up
        else:
            self.paddleBotY =  min(self.paddleBotY + (self.paddleSpeed * 0.8), (self.boardHeight - self.paddleHeight)) #down
    
    def reset(self):
        self.currentMovement = 0
        
        self.paddleUserY = (self.boardHeight/2) - round(self.paddleHeight/2)
        self.paddleBotY = (self.boardHeight/2) - round(self.paddleHeight/2)
        self.paddleOffsetX = 2
        self.paddleSpeed = 0.2
        
        self.ballPos = (round(self.boardWidth/2), round(self.boardHeight/2))
        
        self.userPaddleTiles = []
        self.botPaddleTiles = []
        
        self.showBall = True
        self.gameOver = False
        self.sideLost = 0
        
        self.randomizeBallVelocity()
        
    def runGame(self):
        self.display.init()
        while True:
            timePassed = time.perf_counter() - self.lastTickTime
            if timePassed >= (self.tickDelay/1000):
                if self.showBall and not self.sideLost and not self.waitForInput:
                    self.updateBall()
                self.updateGameState()
                
                if not self.waitForInput and self.sideLost == 0:
                    self.updateBot()
                    if self.currentMovement == 1:
                        self.paddleUserY =  max(self.paddleUserY - self.paddleSpeed, 0)
                    elif self.currentMovement == -1:
                        self.paddleUserY =  min(self.paddleUserY + self.paddleSpeed, (self.boardHeight - self.paddleHeight))
                    
                    if self.paddleUserY == (self.boardHeight - self.paddleHeight) or self.paddleUserY == 0:
                        self.currentMovement = 0
                self.display.fill(BG_COLOR)
                                
                self.render()
                
                self.display.render()
                self.lastTickTime = time.perf_counter()
            
            keys = self.display.getKeys()
            if "q" in keys:
                break
            
            if keys:
                if self.gameOver:
                    self.reset()
                    self.gameOver = False
                    self.lives = (3,3)
                    self.controlsLock = False
                elif self.waitForInput and not self.controlsLock:
                    self.waitForInput = False
            
            if self.controlsLock: continue
            
            if "w" in keys or "up" in keys:
                self.currentMovement = 1
            if "s" in keys or "down" in keys:
                self.currentMovement = -1
            if " " in keys:
                self.currentMovement = 0
        
        self.display.closeDisplay()     
import sys, os, select, tty, termios, re, time
from helpers import *

KEY_PATTERN = re.compile(r"\x1b\[[ABCD]|.", re.DOTALL)
ARROWS = {"\x1b[A": "up", "\x1b[B": "down", "\x1b[C": "right", "\x1b[D": "left"}

class Display:
    def __init__(self, boardWidth = 10, boardHeight = 10, scale = 1, y = 0):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.scale = scale
        self._savedSettings = None
        self.tiles = [[WHITE] * boardWidth for _ in range(boardHeight)]
        self.y = y
        
        self.fd = sys.stdin.fileno()
    
    def init(self):
        self._savedSettings = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)
        #print("\033[2J\033[H\033[?25l", end="", flush=True)
        print("\033[?1049h\033[2J\033[H\033[?25l", end="", flush=True)
        
    def closeDisplay(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self._savedSettings)
        #print("\033[?25h", end="", flush=True)
        print("\033[?25h\033[?1049l", end="", flush=True)
        
    def hideCursor(self):
        print("\033[?25l", end="", flush=True)
    
    def showCursor(self):
        print("\033[?25h", end="", flush=True)
        
    def cursorGoToY(self, y):
        print(f"\033[{y + 1};1H", end="", flush=True)
        
    def cursorHome(self):
        print("\033[H", end="", flush=True)
        
    def getKeys(self):
        if not select.select([self.fd], [], [], 0)[0]:
            return []
        data = os.read(self.fd, 1024).decode(errors="ignore")
        return [ARROWS.get(k, k) for k in KEY_PATTERN.findall(data)]
    
    def draw(self, color, pos):
        x, y = pos
        try:
            self.tiles[y][x] = color
        except Exception:
            return
    
    def fill(self, color):
        self.tiles = [[color] * self.boardWidth for _ in range(self.boardHeight)]
    
    def render(self):
        self.cursorGoToY(self.y)
        for row in range(self.boardHeight):
            for _ in range(self.scale):
                for col in range(self.boardWidth):
                    for _ in range(self.scale * 2):
                        color = self.tiles[row][col]
                        print(f"{color} ", end='')
                print(RESET)
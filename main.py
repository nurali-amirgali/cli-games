import os
import renderer
from helpers import *
from snake import snakeBoard

display = renderer.Display()
display.init()

Snake = snakeBoard(display)

while True:
    display.fill(WHITE)
    Snake.render()
    display.render()
    keys = display.get_keys()
    if "q" in keys:
        break

display.closeDisplay()
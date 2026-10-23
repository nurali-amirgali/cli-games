from helpers import *
from snake import snakeBoard
from paddle import paddleBoard
import questionary

while True:
    print(f"{CYAN_TEXT}TIP: in the game press Q at anytime to go back to the main menu{RESET}")
    choice = questionary.select(
        "What would you like to play?",
        choices=["snake", "paddle", "quit"]
    ).ask()

    if choice == "snake":
        Snake = snakeBoard()
        Snake.runGame()
    elif choice == "paddle":
        Paddle = paddleBoard()
        Paddle.runGame()
    elif choice == "quit":
        break
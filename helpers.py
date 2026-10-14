RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
BOLD   = "\033[1m"
WHITE  = "\033[0m"

try:
    import msvcrt
    def key_pressed():
        return msvcrt.kbhit()
except ImportError:
    import sys, select
    def key_pressed():
        return select.select([sys.stdin], [], [], 0)[0] != []
    
def resetCursor():
    print("\033[H", end="")
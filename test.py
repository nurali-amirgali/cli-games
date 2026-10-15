UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

currentDir = RIGHT

for i in range(4):
    print("---------",i)
    print(((i + 2) % 4) != currentDir)
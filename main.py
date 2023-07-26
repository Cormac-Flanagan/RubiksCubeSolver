import matplotlib.pyplot as plt
from rubiksCube import Rubik
import pygame
import sys
from pygame.locals import *

pygame.init()
# Set the dimensions of the display window
window_size = (1200, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Rubik's Cube Solver")


def main():
    cube = Rubik(screen)
    # Use a breakpoint in the code line below to debug your script.
    moves = cube.shuffle_cube(2000)
    x = range(len(moves))
    y = []
    y2 = []
    while moves:

        # Clear the screen
        move = moves.pop(-1)
        cube.rotate(move[0], -move[1])
        y.append(cube.how_close())
        y2.append(len(moves)/(cube.how_close()+1))
        cube.update()

    plt.plot(x, y, y2, marker='o', linestyle='-')
    plt.xlabel('Move')
    plt.ylabel('How Close to Solved')
    plt.title('Rubik\'s Cube Solver')
    plt.grid(True)
    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import random

import matplotlib.pyplot as plt
from rubiksCube import Rubik
import pygame
import sys
from pygame.locals import *
from copy import deepcopy

pygame.init()
# Set the dimensions of the display window
window_size = (1200, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Rubik's Cube Solver")

def decision_tree(cube: Rubik, sides: list[str], counter=0, offset=3) -> list[tuple[str, int]]:
    visited = []
    result = []
    goat = (cube.how_close(), (None, None), cube.state_id())
    while True:
        options = []

        for side in sides:
            for direction in (-1, 1):
                cube.rotate(side, direction)
                # print(cube.how_close())
                options.append((cube.how_close(), (side, direction), cube.state_id()))
                cube.rotate(side, -direction)

        options.sort(key=lambda x: x[0])

        if new_places := [
            option for option in options if option[-1] not in visited
        ]:
            best = new_places[0]
            # if best[0] > goat[0]+offset:
            #     goat_pos = options.index(goat)
            #     result = result[:goat_pos]
            #     cube.reform(goat[-1])
            #     print(f'{counter}: Jump back to {goat}')


            cube.rotate(best[1][0], best[1][1])
            print(f'{counter}: {best}')
            if best[0] == 0:
                result.append(best[1])
                break

            visited.append(best[-1])
            result.append(best)

        if best[0] < goat[0]:
            goat: tuple[int, tuple[str, int], str] = min(options, key=lambda x: x[0])
        counter += 1

    return result




def main():
    cube = Rubik(screen)
    # Use a breakpoint in the code line below to debug your script.
    cube.update()
    moves = cube.shuffle_cube(100)
    moves.reverse()

    move_num = range(len(moves))
    value = []
    y2 = []

    moves = decision_tree(cube, ["Left", "Bottom", "Back"])

    for move in moves:
        cube.rotate(move[0], move[1])
        value.append(cube.how_close())
        cube.update()
    cube.update()

    plt.plot(move_num, value, y2, marker='o', linestyle='-')
    plt.xlabel('Move')
    plt.ylabel('How Close to Solved')
    plt.title('Rubik\'s Cube Solver')
    plt.grid(True)
    plt.show()
    print(sum(value) / len(value))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

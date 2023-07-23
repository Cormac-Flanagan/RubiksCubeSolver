import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import random

axes = [3, 3, 3]

class Rubik:
    def __init__(self):
        self.Top = np.array(3*[3*['R']])
        self.Bottom = np.array(3*[3*['O']])
        self.Front = np.array(3*[3*['W']])
        self.Right = np.array(3*[3*['Y']])
        self.Left = np.array(3*[3*['B']])
        self.Back = np.array(3*[3*['G']])
        self.cube = [[self.Top, self.Bottom, self.Front, self.Right, self.Left, self.Back]]

    def rotate(self, side, direction):
        if side == 'Top':
            self.Top = np.rot90(self.Top, direction)
            buffer = np.concatenate([self.Front[:, 0], self.Right[:, 0], self.Back[:, 2], self.Left[:, 2]])
            moved = buffer = np.roll(buffer, 3*direction)

            self.Front[:, 0], self.Right[:, 0], self.Back[:, 2], self.Left[:, 2] = [i for i in np.split(moved, 4)]
        elif side == 'Bottom':
            self.Bottom = np.rot90(self.Bottom, direction)
            buffer = np.concatenate((self.Front[:, 2], self.Right[:, 2], self.Back[:, 0], self.Left[:, 0]))
            buffer = np.roll(buffer, 3*direction)
            self.Front[:, 2], self.Right[:, 2], self.Back[:, 0], self.Left[:, 0] = np.split(buffer, 4)

        elif side == 'Front':
            self.Front = np.rot90(self.Front, direction)
            buffer = np.concatenate((self.Top[:, 0], self.Left[2, :], self.Bottom[:, 2], self.Right[0, :]))
            buffer = np.roll(buffer, 3*direction)
            self.Top[:, 0], self.Left[2, :], self.Bottom[:, 2], self.Right[0, :] = np.split(buffer, 4)

        elif side == 'Right':
            self.Right = np.rot90(self.Right, direction)
            buffer = np.concatenate((self.Top[2, :], self.Front[2, :], self.Bottom[0, :], self.Back[0, :]))
            buffer = np.roll(buffer, 3*direction)
            self.Top[2, :], self.Front[2, :], self.Bottom[0, :], self.Back[0, :] = np.split(buffer, 4)

        elif side == 'Left':
            self.Left = np.rot90(self.Left, direction)
            buffer = np.concatenate((self.Top[0, :], self.Back[2, :], self.Bottom[2, :], self.Front[0, :]))
            buffer = np.roll(buffer, 3*direction)
            self.Top[0, :], self.Back[2, :], self.Bottom[2, :], self.Front[0, :] = np.split(buffer, 4)

        elif side == 'Back':
            self.Back = np.rot90(self.Back, direction)
            buffer = np.concatenate((self.Top[:, 2], self.Right[2, :], self.Bottom[:, 0], self.Left[0, :]))
            buffer = np.roll(buffer, 3*direction)
            self.Top[:, 2], self.Right[2, :], self.Bottom[:, 0], self.Left[0, :] = np.split(buffer, 4)

        else:
            print("Invalid side")

    def shuffle_cube(self):
        moves = []
        for i in range(random.randint(10, 100000)):
            move = (random.choice(['Top', 'Bottom', 'Front', 'Right', 'Left', 'Back']), random.choice([1, -1]))
            self.rotate(move[0], move[1])
            moves.append(move)
        return moves

    def update(self):
        for (x, y), col in np.ndenumerate(self.Front):
            draw_front((x*100, y*100), col)

        for (x, y), col in np.ndenumerate(self.Top):
            draw_top((x*100+50*y, -y*50), col)


        for (x, y), col in np.ndenumerate(self.Right):
            draw_side((x*50, +y*100-50*x), col)

        for (x, y), col in np.ndenumerate(self.Back):
            draw_front((x*100, y*100), col, 600)

        for (x, y), col in np.ndenumerate(self.Bottom):
            draw_top((x*100+50*y, -y*50), col, 600)


        for (x, y), col in np.ndenumerate(self.Left):
            draw_side((x*50, +y*100-50*x), col, 600)


import pygame
import sys
from pygame.locals import *

pygame.init()

# Set the dimensions of the display window
window_size = (1200, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Rubik's Cube Solver")


colors_dict = {
    'W': (255, 255, 255),
    'Y': (255, 255, 0),
    'B': (0, 0, 255),
    'G': (0, 255, 0),
    'R': (255, 0, 0),
    'O': (255, 165, 0),
    'K': (0, 0, 0)
}




def draw_front(pos, color, shift = 0):
    # Draw the front face of the cube
    pygame.draw.rect(screen, colors_dict[color],
                      np.add((100+shift, 250, 100, 100), pos+(0,0)))
    # Add other faces of the cube here...

def draw_side(pos, color, shift = 0):
    pygame.draw.polygon(screen, colors_dict[color],
                        np.add(((400+shift, 350), (450+shift, 300), (450+shift, 200), (400+shift, 250)), pos))

def draw_top(pos, color, shift = 0):
    pygame.draw.polygon(screen, colors_dict[color],
                        np.add(((250+shift, 200), (150+shift, 200), (100+shift, 250), (200+shift, 250)), pos))



def main():
    cube = Rubik()

    # Use a breakpoint in the code line below to debug your script.
    moves = cube.shuffle_cube()
    while moves:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(colors_dict['K'])

        move = moves.pop(-1)
        cube.rotate(move[0], -move[1])
        cube.update()
        # Draw the Rubik's Cube
        # Update the display
        pygame.display.update()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

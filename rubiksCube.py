import numpy as np
import copy
import pygame
import random

class Rubik:
    def __init__(self, screen : pygame.Surface | None):
        self.Top: "Top is Red" = np.array(3*[3*['R']])
        self.Bottom: "Bottom is Orange" = np.array(3*[3*['O']])
        self.Front: "Front Is White" = np.array(3*[3*['W']])
        self.Right: 'Right is Yellow' = np.array(3 * [3 * ['Y']])
        self.Left: "Left is Blue" = np.array(3*[3*['B']])
        self.Back: "Back is Green" = np.array(3*[3*['G']])
        self.cube = [[self.Top, self.Bottom, self.Front, self.Right, self.Left, self.Back]]
        self._screen = screen
        self._solved = copy.deepcopy(self.cube)
        self._colors_dict = {
            'W': (255, 255, 255),
            'Y': (255, 255, 0),
            'B': (0, 0, 255),
            'G': (0, 255, 0),
            'R': (255, 0, 0),
            'O': (255, 165, 0),
            'K': (0, 0, 40)
        }


    def rotate(self, side, direction):
        if side == 'Top':
            self.Top = np.rot90(self.Top, direction)
            buffer = np.concatenate([self.Front[:, 0], self.Right[:, 0], self.Back[:, 2], self.Left[:, 2]])
            moved = buffer = np.roll(buffer, 3*direction)
            (
                self.Front[:, 0],
                self.Right[:, 0],
                self.Back[:, 2],
                self.Left[:, 2],
            ) = list(np.split(moved, 4))

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

    def shuffle_cube(self, num_times):
        moves = []
        for _ in range(num_times):
            move = (random.choice(['Top', 'Bottom', 'Front', 'Right', 'Left', 'Back']), random.choice([1, -1]))
            self.rotate(move[0], move[1])
            moves.append(move)
        return moves

    def draw_front(self, pos, color, shift=0):
        # Draw the front face of the cube
        pygame.draw.rect(self._screen, self._colors_dict[color],
                         np.add((100 + shift, 250, 100, 100), pos + (0, 0)))
        # Add other faces of the cube here...

    def draw_side(self, pos, color, shift=0):
        pygame.draw.polygon(self._screen, self._colors_dict[color],
                            np.add(((400 + shift, 350), (450 + shift, 300), (450 + shift, 200), (400 + shift, 250)),
                                   pos))

    def draw_top(self, pos, color, shift=0):
        pygame.draw.polygon(self._screen, self._colors_dict[color],
                            np.add(((250 + shift, 200), (150 + shift, 200), (100 + shift, 250), (200 + shift, 250)),
                                   pos))

    def update(self):
        self._screen.fill((0, 50, 0))

        for (x, y), col in np.ndenumerate(self.Front):
            self.draw_front((x*100, y*100), col)

        for (x, y), col in np.ndenumerate(self.Top):
            self.draw_top((x * 100 + 50 * y, -y * 50), col)

        for (x, y), col in np.ndenumerate(self.Right):
            self.draw_side((x * 50, +y * 100 - 50 * x), col)

        for (x, y), col in np.ndenumerate(self.Back):
            self.draw_front((x * 100, y * 100), col, 600)

        for (x, y), col in np.ndenumerate(self.Bottom):
            self.draw_top((x * 100 + 50 * y, -y * 50), col, 600)

        for (x, y), col in np.ndenumerate(self.Left):
            self.draw_side((x * 50, +y * 100 - 50 * x), col, 600)
        pygame.display.update()
    def how_close(self):
        return np.sum(np.equal(self.cube[0], self._solved[0]))


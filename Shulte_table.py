import sys
import time
import pygame
import random
from pygame.locals import *


WIDTH = 640
HEIGHT = 510

FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CELL_COLOR = (200, 200, 200)
BACKGROUND_COLOR = (232, 176, 210)


class Cell:
    count = 1
    width = WIDTH // 10
    height = min(width, HEIGHT // 10)

    def __init__(self, number, col, row):
        self.number = number
        self.col = col
        self.row = row

    def draw(self, surface, color=CELL_COLOR):
        r = Rect(self.col * Cell.width + 2, self.row * Cell.height + 2, Cell.width - 4, Cell.height - 4)
        t = FONT.render(str(self.number), True, BLACK)

        pygame.draw.rect(surface, color, r)

        adjusted_center = list(r.center)
        adjusted_center[0] -= Cell.width // 8
        adjusted_center[1] -= Cell.height // 4

        surface.blit(t, adjusted_center)
        pygame.display.update()

    def blit_color(self, surface, color):
        self.draw(surface, color)
        time.sleep(0.2)
        self.draw(surface)

    def check_hit(self, click_coords):
        if self.col * Cell.width <= click_coords[0] <= (self.col + 1) * Cell.width \
          and self.row * Cell.height <= click_coords[1] <= (self.row + 1) * Cell.height:
            return True
        return False


def main():
    global FONT

    pygame.init()

    FONT = pygame.font.SysFont('arial', WIDTH // 15)

    DISPLAY_SURF = pygame.display.set_mode((WIDTH, HEIGHT))
    new_game(DISPLAY_SURF)


def new_game(screen):
    width = 5
    height = 5
    board = create_random_board(width, height)
    # screen.fill(BACKGROUND_COLOR)
    screen.fill(WHITE)
    draw_cells(board, screen)

    pygame.display.update()

    run_game(screen, board)


def run_game(screen, board):
    current_num = 1
    final_num = len(board) + 1

    while True:
        if current_num == final_num:
            new_game(screen)

        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
                terminate()
            elif event.type == MOUSEBUTTONUP:
                for cell in board:
                    if cell.check_hit(event.pos):
                        if cell.number == current_num:
                            current_num += 1
                            cell.blit_color(screen, GREEN)
                        else:
                            cell.blit_color(screen, RED)
                        break


def terminate():
    pygame.quit()
    sys.exit()


def create_random_board(cols, rows=None):
    Cell.width = WIDTH // cols
    Cell.height = HEIGHT // rows

    if not rows:
        rows = cols

    numbers = [i + 1 for i in range(cols * rows)]
    random.shuffle(numbers)
    res = []
    for i in range(rows):
        for j in range(cols):
            cell = Cell(numbers[0], j, i)
            numbers.remove(numbers[0])
            res.append(cell)
    return res


def draw_cells(board, screen):
    for cell in board:
        cell.draw(screen)


if __name__ == '__main__':
    main()

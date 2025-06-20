import pygame
import copy
import time

pygame.font.init()
WIDTH, HEIGHT = 800, 800
SIDES = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
FONT = pygame.font.SysFont(None, 18)
CELL_SIZE = 20
UPDATE_DELAY = 0.1

class View:
    def __init__(self, model, win):
        self.model = model
        self.win = win

    def draw(self):
        self.win.fill((100, 100, 100))
        for i in range(self.model.grid_size):
            for j in range(self.model.grid_size):
                pygame.draw.rect(self.win, (0, 0, 0), (10 + i * CELL_SIZE, 10 + j * CELL_SIZE, CELL_SIZE + 1, CELL_SIZE + 1), 1)
                if self.model.grid[j][i] == 1:
                    pygame.draw.rect(self.win, (255, 255, 255), (11+i*CELL_SIZE, 11+j*CELL_SIZE, CELL_SIZE-0.5, CELL_SIZE-0.5))

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        rect.center = (c_x, c_y)
        self.win.blit(widget, rect)

class Model:
    def __init__(self):
        self.run = True
        self.grid_size = 39
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.last_update = time.time() - 1
        self.simulation = False

    def update(self):
        if time.time() - self.last_update >= UPDATE_DELAY and self.simulation:
            self.new_grid = copy.deepcopy(self.grid)
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    cells = 0
                    for side in SIDES:
                        ni, nj = i + side[0], j + side[1]
                        if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                            if self.grid[nj][ni] == 1:
                                cells += 1

                    if self.grid[j][i] == 0:
                        if cells == 3:
                            self.new_grid[j][i] = 1
                    else:
                        if cells > 3 or cells < 2:
                            self.new_grid[j][i] = 0

            self.grid = copy.deepcopy(self.new_grid)
            self.last_update = time.time()

    def check_clicked_cell(self, x, y, state=1):
        if 10 < x < 790 and 10 < y < 790:
            self.grid[(y-10)//CELL_SIZE][(x-10)//CELL_SIZE] = state

class Controller:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.model = Model()
        self.view = View(self.model, self.win)

        pygame.display.set_caption('Conway\'s Game of Life')

    def run(self):
        clock = pygame.time.Clock()

        while self.model.run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.model.run = False

                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    self.model.check_clicked_cell(x, y)

                elif pygame.mouse.get_pressed()[2]:
                    x, y = pygame.mouse.get_pos()
                    self.model.check_clicked_cell(x, y, 0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.model.simulation:
                            self.model.simulation = False
                        else:
                            self.model.simulation = True

                    elif event.key == pygame.K_0:
                        self.model.grid = [[0 for _ in range(self.model.grid_size)] for _ in range(self.model.grid_size)]

            self.model.update()

            self.view.draw()

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    c = Controller()
    c.run()
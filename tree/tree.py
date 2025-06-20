import pygame
import random
from constants import CELL_SIZE, WIDTH, HEIGHT, FONT

class View:
    def __init__(self, model, win):
        self.model = model
        self.win = win

    def draw(self):
        self.win.fill((100, 100, 100))
        self.draw_all_grids()

    def draw_single_grid(self, top_left_x, top_left_y, data, color=False):
        for i in range(self.model.grid_size):
            for j in range(self.model.grid_size):
                x = top_left_x + i * CELL_SIZE
                y = top_left_y + j * CELL_SIZE
                pygame.draw.rect(self.win, (0, 0, 0), (x, y, CELL_SIZE + 1, CELL_SIZE + 1), 1)

                if color and data[j][i] > 0:
                    pygame.draw.rect(self.win, (125, 125, 0), (x+1, y+1, CELL_SIZE-0.5, CELL_SIZE-0.5))

                if data[j][i] != 0:
                    self.get_text_widget_and_center((0, 0, 0), x + CELL_SIZE // 2, y + CELL_SIZE // 2, FONT, str(data[j][i]))

    def draw_all_grids(self):
        grid_width = self.model.grid_size * CELL_SIZE + (self.model.grid_size - 1)
        grid_height = self.model.grid_size * CELL_SIZE + (self.model.grid_size - 1)

        top_grid_x = (WIDTH - grid_width) // 2
        top_grid_y = 25
        self.draw_single_grid(top_grid_x, top_grid_y, self.model.trees)

        start_x = 100
        start_y = top_grid_y + grid_height + 40
        spacing_x = 32
        spacing_y = 20

        for row in range(2):
            for col in range(3):
                idx = row * 3 + col

                grid_x = start_x + (grid_width + spacing_x) * col
                grid_y = start_y + (grid_height + spacing_y) * row

                label = f"{self.model.square_sizes[idx]} x {self.model.square_sizes[idx]}"

                self.get_text_widget_and_center((0, 0, 0), grid_x + grid_width // 2, grid_y - 10, FONT, label)
                self.draw_single_grid(grid_x, grid_y, self.model.answers[idx], True)

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        rect.center = (c_x, c_y)
        self.win.blit(widget, rect)

class Model:
    def __init__(self):
        self.run = True
        self.grid_size = 6
        self.square_sizes = [4, 3, 2, 2, 1, 1]
        self.trees = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.answers = [[[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)] for _ in range(len(self.square_sizes))]
        self.start_game()

    def start_game(self):
        for size in self.square_sizes:
            self.spawn_trees(size)

    def spawn_trees(self, size):
        spawn_area = self.grid_size - size
        top_left = [random.randint(0, spawn_area), random.randint(0, spawn_area)]
        for i in range(size):
            for j in range(size):
                self.trees[j + top_left[1]][i + top_left[0]] += 1

    def check_clicks(self, x, y):
        grid_width = self.grid_size * CELL_SIZE + (self.grid_size - 1)
        grid_height = self.grid_size * CELL_SIZE + (self.grid_size - 1)

        start_x = 100
        start_y = grid_height + 65
        spacing_x = 32
        spacing_y = 20

        for row in range(2):
            for col in range(3):
                idx = row * 3 + col

                grid_x = start_x + (grid_width + spacing_x) * col
                grid_y = start_y + (grid_height + spacing_y) * row

                if grid_x <= x < grid_x + grid_width and grid_y <= y < grid_y + grid_height:
                    cell_x = (x - grid_x) // CELL_SIZE
                    cell_y = (y - grid_y) // CELL_SIZE
                    if 0 <= cell_x < self.grid_size and 0 <= cell_y < self.grid_size:
                        if self.answers[idx][cell_y][cell_x] == 0:
                            self.answers[idx][cell_y][cell_x] = 1
                        else:
                            self.answers[idx][cell_y][cell_x] = 0

    def find_first_one(self, data):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if data[j][i] == 1:
                    return i, j
        return None, None

    @staticmethod
    def check_for_square(i, j, data, size):
        for x in range(i, i+size, 1):
            for y in range(j, j+size, 1):
                if data[y][x] != 1:
                    return False
        return True

    def check_game_end(self):
        for answer in range(len(self.answers)):
            if sum(a.count(1) for a in self.answers[answer]) != self.square_sizes[answer] ** 2:
                return False
            i, j = self.find_first_one(self.answers[answer])
            if not self.check_for_square(i, j, self.answers[answer], self.square_sizes[answer]):
                return False

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                temp = 0
                for answer in range(len(self.answers)):
                    temp += self.answers[answer][j][i]
                if temp != self.trees[j][i]:
                    return False
        return True

class Controller:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.model = Model()
        self.view = View(self.model, self.win)

        pygame.display.set_caption('Tree')

    def run(self):
        clock = pygame.time.Clock()

        while self.model.run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.model.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        self.model.check_clicks(x, y)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print(self.model.check_game_end())

            self.view.draw()

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    c = Controller()
    c.run()
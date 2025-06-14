import pygame
import random

WIDTH, HEIGHT = 600, 600
SIDES = [[0, 1], [0, -1], [1, 0], [-1, 0]]

class View:
    def __init__(self, model, win):
        self.model = model
        self.win = win

    def draw(self):
        self.win.fill((100, 100, 100))

        for i in range(3):
            for j in range(3):
                pygame.draw.rect(self.win, (0, 0, 0), (120+i*120, 120+j*120, 124, 124), 4)
                if self.model.lights[j][i] == 0:
                    pygame.draw.rect(self.win, (60, 60, 60), (124+i*120, 124+j*120, 116, 116))
                if self.model.lights[j][i] == 1:
                    pygame.draw.rect(self.win, (180, 180, 0), (124+i*120, 124+j*120, 116, 116))

        if self.model.won:
            print('you winnnnn')

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        rect.center = (c_x, c_y)
        self.win.blit(widget, rect)

class Model:
    def __init__(self):
        self.run = True
        self.lights = [[random.randint(0, 1) for _ in range(10)] for _ in range(10)]
        self.won = False

    def get_mouse_pos(self, x, y):
        if 120 < x < 480 and 120 < y < 480 and self.won == False:
            xpos = x // 120 - 1
            ypos = y // 120 - 1

            if self.lights[ypos][xpos] == 0:
                self.lights[ypos][xpos] = 1
            else:
                self.lights[ypos][xpos] = 0

            for i in range(4):
                try:
                    if self.lights[ypos + SIDES[i][1]][xpos + SIDES[i][0]] == 0:
                        self.lights[ypos + SIDES[i][1]][xpos + SIDES[i][0]] = 1
                    else:
                        self.lights[ypos+ SIDES[i][1]][xpos + SIDES[i][0]] = 0

                except IndexError:
                    continue

        self.won = self.check_for_win()

    def check_for_win(self):
        for i in range(3):
            for j in range(3):
                if self.lights[j][i] != 1:
                    return False
        return True

class Controller:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.model = Model()
        self.view = View(self.model, self.win)

        pygame.display.set_caption('Lightbulb')

    def run(self):
        clock = pygame.time.Clock()

        while self.model.run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.model.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.model.get_mouse_pos(x, y)

            self.view.draw()

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    c = Controller()
    c.run()
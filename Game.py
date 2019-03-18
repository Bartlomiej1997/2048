import pygame
import random
import copy
import json


class Game:
    def __init__(self, title, width, height):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(title)
        self.font = pygame.font.SysFont(
            "Times New Roman", self.HEIGHT // 11, bold=True)
        self.matrix = [[0] * 4 for i in range(4)]
        self.running = True
        self.mouse_position = (0, 0)
        with open('colors.json') as f:
            self.colors = json.load(f)

    def run(self):
        self.spawn_tile()
        self.display()
        while self.running:
            self.handle_events()
        pygame.quit()

    def game_over(self):
        for row in self.matrix:
            if 0 in row:
                return False
        for i in range(len(self.matrix) - 1):
            for j in range(len(self.matrix[i]) - 1):
                if self.matrix[i][j] == self.matrix[i + 1][j] or self.matrix[i][j] == self.matrix[i][j + 1]:
                    return False
        for i in range(len(self.matrix) - 1):
            if self.matrix[len(self.matrix) - 1][i] == self.matrix[len(self.matrix) - 1][i + 1]:
                return False
        for i in range(len(self.matrix[len(self.matrix) - 1]) - 1):
            if self.matrix[i][len(self.matrix[i]) - 1] == self.matrix[i + 1][len(self.matrix[i]) - 1]:
                return False
        return True

    def spawn_tile(self):
        while True:
            x, y = random.randint(0, 3), random.randint(0, 3)
            if self.matrix[x][y] == 0:
                self.matrix[x][y] = 2 if random.random() > 0.1 else 4
                break

    def display(self):
        self.window.fill(pygame.Color(self.colors["border"]))
        width = self.WIDTH // 4
        height = self.HEIGHT // 4
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.display_tile(j * width + width * 0.05, i * height +
                                  height * 0.05, width * 0.9, height * 0.9, self.matrix[i][j])

        pygame.display.update()

    def display_game_over(self):
        img = pygame.image.load('game_over.jpg')
        rect = img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.window.blit(img, (rect[0], rect[1]))
        pygame.display.update()

    def display_tile(self, x, y, width, height, value, background_color=-1, font_color=-1):
        if value == 0:
            pygame.draw.rect(self.window, pygame.Color(
                self.colors["tile"]), [x, y, width, height])
        else:
            if background_color == -1:
                background_color = pygame.Color(
                    self.colors[str(value)]["background"])

            if font_color == -1:
                font_color = pygame.Color(self.colors[str(value)]["font"])
            if value > 0:
                pygame.draw.rect(self.window, background_color, [
                                 x, y, width, height])
                text = self.font.render(str(value), True, font_color)
                text_width = text.get_width()
                text_height = text.get_height()
                self.window.blit(text, (x + width // 2 - text_width //
                                        2, y + height // 2 - text_height // 2))

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            self.handle_keyboard_events(e)
            self.handle_mouse_events(e)

    def handle_keyboard_events(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_DOWN or e.key == pygame.K_s:
                self.merge('DOWN')
            elif e.key == pygame.K_LEFT or e.key == pygame.K_a:
                self.merge('LEFT')
            elif e.key == pygame.K_UP or e.key == pygame.K_w:
                self.merge('UP')
            elif e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                self.merge('RIGHT')

    def handle_mouse_events(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self.mouse_position = pygame.mouse.get_pos()
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            new_mouse_position = pygame.mouse.get_pos()
            delta_x = self.mouse_position[0] - new_mouse_position[0]
            delta_y = self.mouse_position[1] - new_mouse_position[1]
            if delta_x * delta_x + delta_y * delta_y > (self.WIDTH + self.HEIGHT) / 2:
                if abs(delta_x) > abs(delta_y):
                    if delta_x > 0:
                        self.merge('LEFT')
                    else:
                        self.merge('RIGHT')
                else:
                    if delta_y > 0:
                        self.merge('UP')
                    else:
                        self.merge('DOWN')

    def merge(self, dir):
        merged = False
        if dir == 'UP':
            merged = self.merge_up()
        elif dir == 'DOWN':
            merged = self.merge_down()
        elif dir == 'LEFT':
            merged = self.merge_left()
        elif dir == 'RIGHT':
            merged = self.merge_right()

        if merged:
            self.spawn_tile()
            self.display()
            if self.game_over():
                self.display_game_over()

    def merge_right(self):
        c = copy.deepcopy(self.matrix)
        for k in range(len(self.matrix)):
            for i in range(len(self.matrix) - 1, -1, -1):
                if self.matrix[k][i] == 0:
                    s = 0
                    for j in range(i):
                        s += self.matrix[k][j]
                    if s > 0:
                        while self.matrix[k][i] == 0:
                            self.matrix[k].pop(i)
                            self.matrix[k].insert(0, 0)

        for k in range(len(self.matrix)):
            for i in range(len(self.matrix) - 1, 0, -1):
                if self.matrix[k][i] == self.matrix[k][i - 1]:
                    self.matrix[k][i] *= 2
                    self.matrix[k].pop(i - 1)
                    self.matrix[k].insert(0, 0)

        return c != self.matrix

    def merge_left(self):
        c = copy.deepcopy(self.matrix)
        for k in range(len(self.matrix)):
            for i in range(len(self.matrix)):
                if self.matrix[k][i] == 0:
                    s = 0
                    for j in range(i, len(self.matrix)):
                        s += self.matrix[k][j]
                    if s > 0:
                        while self.matrix[k][i] == 0:
                            self.matrix[k].pop(i)
                            self.matrix[k].append(0)

        for k in range(len(self.matrix)):
            for i in range(len(self.matrix) - 1):
                if self.matrix[k][i] == self.matrix[k][i + 1]:
                    self.matrix[k][i] *= 2
                    self.matrix[k].pop(i + 1)
                    self.matrix[k].append(0)

        return c != self.matrix

    def merge_down(self):
        self.matrix = list(map(list, zip(*self.matrix)))
        v = self.merge_right()
        self.matrix = list(map(list, zip(*self.matrix)))
        return v

    def merge_up(self):
        self.matrix = list(map(list, zip(*self.matrix)))
        v = self.merge_left()
        self.matrix = list(map(list, zip(*self.matrix)))
        return v

import pygame
import numpy as np

WIDHT, HEIGHT = 800, 800
ROW, COLS = 40, 40

class Pixel(pygame.sprite.Sprite):
    def __init__(self, groups, size, pos):
        super().__init__(groups)
        self.color = (0, 0, 0)
        self.value = 0.0
        self.pos = pos
        self.size = size
        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.rect = self.image.get_frect(topleft=pos)
    
    def update(self):
        return 
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] <= mouse_pos[0] < self.pos[0] + self.size[0] \
            and self.pos[1] <= mouse_pos[1] < self.pos[1] + self.size[1] \
            and pygame.mouse.get_pressed()[0] and self.image is not None:
            color_multiplier = int(255 * self.value)
            self.image.fill((color_multiplier, color_multiplier, color_multiplier))
            self.value += 0.03
            if self.value >= 1.0:
                self.value = 1.0
            print(self.pos)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Draw Number')
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.matrix: list[list[Pixel]] = []
        pixel_size = WIDHT // ROW
        for i in range(ROW):
            row = []
            for j in range(COLS):
                row.append(Pixel(self.all_sprites, (pixel_size, pixel_size), (i * pixel_size, j * pixel_size))) 
            self.matrix.append(row)

    def draw_canvas(self):
        mouse_pos = pygame.mouse.get_pos()
        right_clicked = pygame.mouse.get_pressed()[0]
        directions = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (0, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1)
        ]
        for i, row in enumerate(self.matrix):
            for j, pixel in enumerate(row):
                if pixel.pos[0] <= mouse_pos[0] < pixel.pos[0] + pixel.size[0] \
                    and pixel.pos[1] <= mouse_pos[1] < pixel.pos[1] + pixel.size[1] \
                    and right_clicked:
                        for dir in directions:
                            x = i + dir[0]
                            y = j + dir[1]
                            if x < 0 or x >= len(row) or y < 0 or y >= len(self.matrix):
                                continue
                            pixel = self.matrix[x][y]
                            if (dir[0] == 1 or dir[0] == -1) and (dir[1] == 1 or dir[1] == -1):
                                pixel.value += 0.05
                            elif dir[0] == 0 and dir[1] == 0:
                                pixel.value += 0.07
                            else:
                                pixel.value += 0.06
                            if pixel.value >= 1.0:
                                pixel.value = 1.0
                            color_multiplier = int(255 * pixel.value)
                            if pixel.image is None:
                                continue
                            pixel.image.fill((color_multiplier, color_multiplier, color_multiplier))

    def clear_canvas(self):
        for row in self.matrix:
            for pixel in row:
                pixel.value = 0.0
                if pixel.image is not None:
                    pixel.image.fill((int(pixel.value), int(pixel.value), int(pixel.value)))

    def calculate_matrix(self):
        value = np.zeros((ROW, COLS))
        for i, row in enumerate(self.matrix):
            for j, pixel in enumerate(row):
                value[j, i] = pixel.value
        return value

    def user_input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_a]:
            value = self.calculate_matrix()
            print(value)
        if keys[pygame.K_b]:
            self.clear_canvas()

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.all_sprites.update()
            self.user_input()
            self.draw_canvas()
            self.screen.fill('black')
            self.all_sprites.draw(self.screen)
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
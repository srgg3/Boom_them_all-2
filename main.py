import pygame
import random
import sys
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = bomb_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.exploded = False

    def draw(self, surface):
        if self.exploded:
            surface.blit(explosion_image, (self.x, self.y))
        else:
            surface.blit(self.image, (self.x, self.y))

    def explode(self):
        self.exploded = True


def generate_positions(num_bombs, bomb_size_w, bomb_size_h, padding=10):
    positions = []
    attempts = 0
    max_attempts = num_bombs * 20

    while len(positions) < num_bombs and attempts < max_attempts:
        x = random.randint(padding, width - bomb_size_w - padding)
        y = random.randint(padding, height - bomb_size_h - padding)
        new_rect = pygame.Rect(x, y, bomb_size_w, bomb_size_h)

        if not any(new_rect.colliderect(pygame.Rect(px, py, bomb_size_w, bomb_size_h)) for px, py in positions):
            positions.append((x, y))
        attempts += 1

    return positions


if __name__ == '__main__':
    pygame.init()

    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Boom them all - 2")

    bomb_image = load_image('bomb2.png')
    explosion_image = load_image('boom.png')

    bomb_size_w = bomb_image.get_width()
    bomb_size_h = bomb_image.get_height()

    positions = generate_positions(10, bomb_size_w, bomb_size_h)
    bombs = [Bomb(x, y) for x, y in positions]

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for bomb in bombs:
                    if bomb.rect.collidepoint(mouse_pos) and not bomb.exploded:
                        bomb.explode()

        for bomb in bombs:
            bomb.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
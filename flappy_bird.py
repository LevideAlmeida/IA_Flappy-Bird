import pygame
from pygame.locals import *  # noqa # type:ignore
from pathlib import Path
import random

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
ROOT_FOLDER = Path(__file__).parent

BACKGROUND_IMAGE = pygame.transform.scale2x(
    pygame.image.load(
        ROOT_FOLDER / "imgs" / "bg.png"
    )
)

PIPE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(
        ROOT_FOLDER / "imgs" / "pipe.png"
    )
)

GROUND_IMAGE = pygame.transform.scale2x(
    pygame.image.load(
        ROOT_FOLDER / "imgs" / "base.png"
    )
)

BIRD_IMAGES = [
    pygame.transform.scale2x(
        pygame.image.load(ROOT_FOLDER / "imgs" / "bird1.png")
    ),
    pygame.transform.scale2x(
        pygame.image.load(ROOT_FOLDER / "imgs" / "bird2.png")
    ),
    pygame.transform.scale2x(
        pygame.image.load(ROOT_FOLDER / "imgs" / "bird3.png")
    ),
    pygame.transform.scale2x(
        pygame.image.load(ROOT_FOLDER / "imgs" / "bird2.png")
    ),
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

POINTS_FONT = pygame.font.SysFont("", 50, False, False)


class Bird(pygame.sprite.Sprite):
    # Variaveis de animação de rotação
    MAX_ROTATION = 25
    ROTANTION_SPEED = 20

    def __init__(self, position_x, position_y):
        super().__init__()
        self.position_x = position_x
        self.position_y = position_y
        self.angle = 0
        self.speed = 0
        self.height = self.position_y
        self.time = 0
        self.image_index = 0
        self._sprites = BIRD_IMAGES
        self.sprite_index = 0
        self.image = self._sprites[self.sprite_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position_x, self.position_y)
        self.mask = pygame.mask.from_surface(self.image)

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.position_y

    def move(self):
        self.time += 1
        # S = So + Vo*t + at²/2
        displacement = self.speed * self.time + 1.5 * (self.time**2)

        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        if displacement < 0 or self.position_y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
            if self.angle > -90:
                self.angle += self.ROTANTION_SPEED

    def update(self):
        if self.sprite_index >= len(self._sprites):
            self.sprite_index = 0

        self.image = self._sprites[int(self.sprite_index)]
        self.sprite_index += 0.1

        # se o passaro tiver caindo, ele nao vai bater a asa
        if self.angle <= -80:
            self.image = self._sprites[1]
            self.sprite_index = 1

        # rotacionando a imagem
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.image = rotated_image


class Pipes(pygame.sprite.Sprite):
    def __init__(self, position_x):
        super().__init__()
        self.x = position_x
        self.height = 0
        self.pipes_distance = 200
        self.ground_pipe_position = 0
        self.top_pipe_position = 0
        self.speed = 5
        self.ground_pipe = PIPE_IMAGE
        self.top_pipe = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.passed = False
        self.define_height()

    def define_height(self):
        self.height = random.randrange(100, 450)
        self.top_pipe_position = self.height - self.top_pipe.get_height()
        self.ground_pipe_position = self.height + self.pipes_distance

    def move(self):
        self.x += self.speed

    def draw(self):
        screen.blit(self.top_pipe, (self.x, self.top_pipe_position))
        screen.blit(self.ground_pipe, (self.x, self.ground_pipe_position))

    def collided(self, bird):
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.top_pipe)
        ground_pipe_mask = pygame.mask.from_surface(self.ground_pipe)

        top_distance = (self.x - bird.position_x,
                        self.top_pipe_position - round(bird.position_y))
        ground_distance = (self.x - bird.position_x,
                           self.ground_pipe_position - round(bird.position_y))

        top_point = bird_mask.overlap(top_pipe_mask, top_distance)
        ground_point = bird_mask.overlap(ground_pipe_mask, ground_distance)

        if top_point or ground_point:
            return True
        else:
            return False


class Ground(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = GROUND_IMAGE
        self.width = self.image.get_width()
        self.y = y
        self.x1 = 0
        self.x2 = self.width
        self.speed = 5

    def move(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 + self.width > 0:
            self.x1 = self.width
        if self.x2 + self.width > 0:
            self.x2 = self.width

    def draw(self):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))


all_sprites = pygame.sprite.Group()

bird = Bird(300, 400)
all_sprites.add(bird)

clock = pygame.time.Clock()
fps = 60

while True:
    clock.tick(fps)

    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:  # noqa
            pygame.quit()
            exit()

    all_sprites.draw(screen)
    all_sprites.update()
    bird.update()

    pygame.display.update()

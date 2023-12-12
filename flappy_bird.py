import pygame
from pygame.locals import *  # noqa # type:ignore
from pathlib import Path

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
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

POINTS_FONT = pygame.font.SysFont("", 50, False, False)


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = GROUND_IMAGE


class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = GROUND_IMAGE


class Bird(pygame.sprite.Sprite):
    # Variaveis de animação de rotação
    MAX_ROTATION = 25
    ROTANTION_SPEED = 20
    ANIMATION_TIME = 5

    def __init__(self, position_x, position_y):
        super().__init__()
        self.position_x = position_x
        self.position_y = position_y
        self.angle = 0
        self.speed = 0
        self.height = self.position_y
        self.time = 0
        self.image_index = 0
        self.sprites = BIRD_IMAGES

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


all_sprites = pygame.sprite.Group()
bird = Bird(1, 2)
all_sprites.add(bird)

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:  # noqa
            pygame.quit()
            exit()

    pygame.display.update()

import pygame
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

pygame.display.set_caption("Flappy Bird")

POINTS_FONT = pygame.font.SysFont("", 50, False, False)


class Bird(pygame.sprite.Sprite):
    # Variaveis de animação de rotação
    MAX_ROTATION = 25
    ROTANTION_SPEED = 20
    ANIMATED_TIME = 5

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image_index = 0
        self.images = BIRD_IMAGES
        self.image = self.images[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        self.time += 1
        # S = So + Vo*t + at²/2
        displacement = self.speed * self.time + 1.5 * (self.time**2)

        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTANTION_SPEED

    def draw(self, screen):
        # definir qual imagem do passaro vai usar
        self.image_index += 1

        if self.image_index < self.ANIMATED_TIME:
            self.image = self.images[0]
        elif self.image_index < self.ANIMATED_TIME*2:
            self.image = self.images[1]
        elif self.image_index < self.ANIMATED_TIME*3:
            self.image = self.images[2]
        elif self.image_index < self.ANIMATED_TIME*4:
            self.image = self.images[1]
        elif self.image_index >= self.ANIMATED_TIME*4 + 1:
            self.image = self.images[0]
            self.image_index = 0

        # se o passaro tiver caindo eu não vou bater asa
        if self.angle <= -80:
            self.image = self.images[1]
            self.image_index = self.ANIMATED_TIME*2

        # desenhar a imagem
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        image_center_position = self.image.get_rect(
            topleft=(self.x, self.y)).center
        rect = rotated_image.get_rect(center=image_center_position)
        screen.blit(rotated_image, rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Pipe(pygame.sprite.Sprite):
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
        self.x -= self.speed

    def draw(self, screen):
        screen.blit(self.top_pipe, (self.x, self.top_pipe_position))
        screen.blit(self.ground_pipe, (self.x, self.ground_pipe_position))

    def collided(self, bird):
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.top_pipe)
        ground_pipe_mask = pygame.mask.from_surface(self.ground_pipe)

        top_distance = (self.x - bird.x,
                        self.top_pipe_position - round(bird.y))
        ground_distance = (self.x - bird.x,
                           self.ground_pipe_position - round(bird.y))

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

        if self.x1 + self.width - 5 < 0:
            self.x1 = self.width
        if self.x2 + self.width - 5 < 0:
            self.x2 = self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))


def draw_screen(screen, birds, pipes, ground, score):
    screen.blit(BACKGROUND_IMAGE, (0, -200))
    for bird in birds:
        bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)

    text = POINTS_FONT.render(f"Score: {score}", True, (0, 0, 0))

    screen.blit(text, (10, text.get_height()))

    ground.draw(screen)
    pygame.display.flip()


def main():
    birds = [Bird(200, 300)]
    ground = Ground(SCREEN_HEIGHT - 160)
    pipes = [Pipe(SCREEN_WIDTH)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = 0
    clock = pygame.time.Clock()
    fps = 30

    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # noqa
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:  # noqa
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()
                if event.key == pygame.K_r:
                    birds = [Bird(200, 300)]
                    ground = Ground(SCREEN_HEIGHT - 160)
                    pipes = [Pipe(SCREEN_WIDTH)]
                    score = 0

        for bird in birds:
            bird.move()
        ground.move()

        add_pipe = False
        remove_pipes = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collided(bird):
                    birds.pop(i)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            pipe.move()

            if pipe.x < -(pipe.ground_pipe.get_width()):
                remove_pipes.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(SCREEN_WIDTH))

        for pipe in remove_pipes:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) >= ground.y or bird.y <= 0:
                birds.pop(i)

        draw_screen(screen, birds, pipes, ground, score)


if __name__ == "__main__":
    main()

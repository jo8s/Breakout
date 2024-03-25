import pygame
import random

# set up game window
pygame.init()
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# define game objects
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 80
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(random.choice([RED, GREEN, BLUE]))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 10
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.speed_x = 5
        self.speed_y = -5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > HEIGHT:
            self.rect.centerx = WIDTH // 2
            self.rect.centery = HEIGHT // 2
            self.speed_y = -5
            self.wait_for_enter()

    def wait_for_enter(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False

# create game objects
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
paddle = Paddle()
ball = Ball()
all_sprites.add(paddle, ball)

for i in range(10):
    for j in range(5):
        brick = Brick(i*80+40, j*30+50)
        all_sprites.add(brick)
        bricks.add(brick)

# set up game loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update game objects
    all_sprites.update()

    # check for collisions
    if pygame.sprite.collide_rect(ball, paddle):
        ball.speed_y *= -1

    brick_collisions = pygame.sprite.spritecollide(ball, bricks, True)
    if brick_collisions:
        ball.speed_y *= -1

    # draw game objects
    win.fill(BLACK)
    all_sprites.draw(win)
    pygame.display.flip()

pygame.quit()
exit()

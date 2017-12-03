import pygame
import random
from random import randint as ri
from pygame.locals import *
pygame.init()

# Game Setup
WIDTH = pygame.display.Info().current_w // 2  # game window width
HEIGHT = pygame.display.Info().current_h // 2  # game window height
GAME_RES = WIDTH, HEIGHT
print(GAME_RES)
FPS = 120
window = pygame.display.set_mode(GAME_RES, HWACCEL | HWSURFACE | DOUBLEBUF)
pygame.display.set_caption("copy pong")
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 8)
points_font = pygame.font.SysFont("monospace", 20)
# End Game Setup

# Game Values
objects = {}
player_points = 0
enemy_points = 0
background_color = (ri(0, 255), ri(0, 255), ri(0, 255))  # RGB random value


class Ball(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2
        self.rect.y = HEIGHT//2
        self.x_speed = random.choice([-2, -1, 1, 2])
        self.y_speed = random.choice([-2, -1, 1, 2])

    def move(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def reset(self):
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        self.x_speed = 1
        self.y_speed = 1


class Pad(pygame.sprite.Sprite):
    def __init__(self, image, posx, posy, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

# instance ball
ball_img = pygame.image.load('./ball_sprite.png')
objects["ball"] = Ball(ball_img)
ball_w = objects["ball"].rect.size[0]
ball_h = objects["ball"].rect.size[1]
ball_group = pygame.sprite.Group(objects["ball"])

# instance pad 1
pad_img = pygame.image.load('./player_sprite.png')
objects["pad"] = Pad(pad_img, 10, 10, 0)
pad_w = objects["pad"].rect.size[0]
pad_h = objects["pad"].rect.size[1]

# instance pad 2
speed_pad2 = random.choice([-3, -2, -1, 1, 2, 3])
pad2_img = pygame.image.load('./enemy_sprite.png')
objects["pad2"] = Pad(pad2_img, WIDTH-30, 10, 1)
pad2_w = objects["pad2"].rect.size[0]
pad2_h = objects["pad2"].rect.size[1]

pad_group = pygame.sprite.Group(objects["pad2"], objects["pad"])

# end Game Values

# Game loop
game_ended = False
while not game_ended:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            game_ended = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended = True
                break
            if event.key == K_w:
                objects["pad"].speed = -2
            if event.key == K_s:
                objects["pad"].speed = 2

        if event.type == KEYUP:
            if event.key == K_w:
                objects["pad"].speed = 0
            if event.key == K_s:
                objects["pad"].speed = 0

    # ball collide with right
    if objects["ball"].rect.x > WIDTH-ball_w//2:
        objects["ball"].reset()
        objects["ball"].x_speed = random.choice([-2, -1, 1, 2])
        objects["ball"].y_speed = random.choice([-2, -1, 1, 2])
        player_points += 1

    # ball collide with left
    if objects["ball"].rect.x < 0-ball_w//2:
        objects["ball"].reset()
        objects["ball"].x_speed = random.choice([-2, -1, 1, 2])
        objects["ball"].y_speed = random.choice([-2, -1, 1, 2])
        enemy_points += 1

    # ball collide with bottom
    if objects["ball"].rect.y > HEIGHT-ball_h//2:
        objects["ball"].y_speed *= -1

    # ball collide with top
    if objects["ball"].rect.y == 0-ball_h//2:
        objects["ball"].y_speed *= -1

    # pad collide with bottom
    if objects["pad"].rect.y > HEIGHT - pad_h // 2:
        objects["pad"].speed *= -1

    # pad collide with top
    if objects["pad"].rect.y < 0 - pad_h // 2:
        objects["pad"].speed *= -1

    # pad2 collide with bottom
    if objects["pad2"].rect.y > HEIGHT - pad_h // 2:
        objects["pad2"].speed *= -1

    # pad2 collide with top
    if objects["pad2"].rect.y < 0 - pad_h // 2:
        objects["pad2"].speed *= -1

    # ball collide with pad
    if pygame.sprite.spritecollideany(objects["ball"], pad_group) is not None:
        objects["ball"].x_speed *= -1

    # Display update
    pygame.Surface.fill(window, background_color)  # change screen color
    objects["pad"].move()
    objects["pad2"].move()
    objects["ball"].move()
    ball_group.draw(window)
    pad_group.draw(window)

    # x pos of the pad pos
    x_text = myfont.render("x = " + str(objects["pad"].rect.x), 1, (0, 0, 0))
    window.blit(x_text, (5, 10))
    # y pos of the pad pos
    y_text = myfont.render("y = " + str(objects["pad"].rect.y), 1, (0, 0, 0))
    window.blit(y_text, (5, 30))

    # player points
    p_text = points_font.render(str(player_points), 1, (0, 0, 0))
    window.blit(p_text, (WIDTH // 2-20, 20))
    # enemy points
    e_text = points_font.render(str(enemy_points), 1, (0, 0, 0))
    window.blit(e_text, (WIDTH // 2 + 20, 20))

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
exit(0)

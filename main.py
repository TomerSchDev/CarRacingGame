import pygame
import time
import math
from utils import *

GRASS = pygame.image.load("imgs/grass.jpg")
FINISH = pygame.image.load("imgs/finish.png")
WIDTH, HEIGHT = 600, 700
TRACK = pygame.image.load("imgs/track.png")
TRACK_BORDER = pygame.image.load("imgs/track-border.png")
#   cars Images
RED_CAR = pygame.image.load("imgs/red-car.png")
GREEN_CAR = pygame.image.load("imgs/green-car.png")
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# resize the imgs
TRACK = change_img_size(TRACK, (WIDTH, HEIGHT))
GRASS = change_img_size(GRASS, (WIDTH, HEIGHT))
TRACK_BORDER = change_img_size(TRACK_BORDER, (WIDTH, HEIGHT))
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = img_scale(FINISH, .55)
FINISH_POSITION = (18, 250)
FINISH_MASK = pygame.mask.from_surface(FINISH)

RED_CAR = img_scale(RED_CAR, 0.4)
GREEN_CAR = img_scale(GREEN_CAR, 0.55)
pygame.display.set_caption("Racing Game")
RED_CAR = img_scale(RED_CAR, 0.9)
FPS = 60


class AbstractCar:

    def __init__(self, max_v, rotation_v):
        self.max_v = max_v
        self.rotation_v = rotation_v
        self.vel = 0
        self.angle = 0
        self.img = self.IMG
        self.x, self.y = self.START_POS
        self.acc = 1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_v
        if right:
            self.angle -= self.rotation_v

    def draw(self, win):
        rotate_image(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acc, self.max_v)

    def move(self):
        radiens = (math.radians(self.angle))
        ver = math.cos(radiens) * self.vel
        hor = math.sin(radiens) * self.vel
        self.y -= ver
        self.x -= hor

    def move_backward(self):
        self.vel = max(self.vel - self.acc, -self.max_v / 2)

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):
    START_POS = (200, 200)
    IMG = RED_CAR

    def reduce_speed(self):
        self.vel = max(self.vel - self.acc / 2, 0)

    def bounce(self):
        self.vel = -self.vel
        self.move()


def draw(win, imgs, player):
    for img, pos in imgs:
        win.blit(img, pos)
    player.draw(WIN)
    pygame.display.update()


def move_player():
    moved = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.rotate(left=True)
    if keys[pygame.K_d]:
        player.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player.move_backward()
    if not moved:
        player.reduce_speed()
    player.move()


run = True
player = PlayerCar(10, 4)
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]

while run:

    clock.tick(FPS)
    draw(WIN, images, player)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    move_player()
    if (player.collide(TRACK_BORDER_MASK)) is not None:
        player.bounce()
    finish_poi_collide = player.collide(FINISH_MASK, *FINISH_POSITION)
    if finish_poi_collide is not None:
        if finish_poi_collide[1] != 0:
            player.reset()
        else:
            player.bounce()
pygame.quit()

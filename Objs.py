import pygame
from pygame import gfxdraw
import random

pygame.init()


class Bar:
    def __init__(self, x, y, w, h, a=0):
        self.x = x
        self.y = y
        self.w = w

        self.rect = pygame.Rect(x, y, w, h)
        self.wall_top = (self.rect.left, self.rect.top, self.rect.right, self.rect.top)
        self.wall_left = (self.rect.left, self.rect.top, self.rect.left, self.rect.bottom)
        self.wall_right = (self.rect.right, self.rect.top, self.rect.right, self.rect.bottom)
        # self.center = self.rect.midtop

        # self.h = h
        self.direct = pygame.Vector2(0, 0)
        self.speed = 10
        self.a = a

    def update(self):
        # self.rect.x += self.speed
        self.rect = self.rect.move(self.direct.x * self.speed, 0)
        self.wall_top = (self.rect.left, self.rect.top, self.rect.right, self.rect.top)
        self.wall_left = (self.rect.left, self.rect.top, self.rect.left, self.rect.bottom)
        self.wall_right = (self.rect.right, self.rect.top, self.rect.right, self.rect.bottom)
        # self.center = self.rect.midtop
        # self.rect = self.rect.move(self.direct.lerp(self.direct * self.speed, 0.9).x, 0)

    def show(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 0, self.a)


class Ball:
    def __init__(self, init_pos, init_direct, vel, w):
        self.init_pos = init_pos
        self.init_direct = init_direct
        # self.x = x
        # self.y = y
        self.w = w
        self.r = int(self.w/2)
        self.vel = vel
        # self.pos = pygame.Vector2(init_pos)
        self.rect = pygame.Rect(init_pos, (w, w))
        self.direct = pygame.Vector2(init_direct).normalize()
        self.color = (255, 255, 255)
        self.is_colliding = False

    def update(self):
        self.rect = self.rect.move(self.direct.x * self.vel, self.direct.y * self.vel)
        # self.pos += self.direct * 5

        # self.center = list(map(add, self.center, self.direct))

    def show(self, surface):
        pygame.draw.ellipse(surface, (255, 255, 255), self.rect)
        pygame.gfxdraw.aaellipse(surface, int(self.rect.centerx), int(self.rect.centery), self.r, self.r, self.color)
        # pygame.gfxdraw.aaellipse(surface, int(self.pos.x), int(self.pos.y), self.r, self.r, (255, 255, 255))

    def if_collide(self, wall_list):
        if isinstance(wall_list, (list, tuple)):
            collide_index = self.rect.collidelist(wall_list)
        else:
            raise TypeError("Only lists,tuples are allowed")
        return collide_index

    normal_wall_list = (pygame.Vector2(0, 1), pygame.Vector2(-1, 0), pygame.Vector2(0, -1), pygame.Vector2(1, 0))
    #                           |                                           ^
    #                           |                 <---------                |                   --------->
    #                           V                                           |

    def bounce(self, other_rect):
        # self.direct = self.direct.reflect(normal_wall)
        collision_tolerance = 10
        if abs(other_rect.top - self.rect.bottom) < collision_tolerance and self.direct.y > 0:
            self.direct = self.direct - 2*self.direct.dot(Ball.normal_wall_list[2])*Ball.normal_wall_list[2]

        elif abs(other_rect.bottom - self.rect.top) < collision_tolerance and self.direct.y < 0:
            self.direct = self.direct - 2 * self.direct.dot(Ball.normal_wall_list[0]) * Ball.normal_wall_list[0]

        if abs(other_rect.right - self.rect.left) < collision_tolerance and self.direct.x < 0:
            self.direct = self.direct - 2 * self.direct.dot(Ball.normal_wall_list[3]) * Ball.normal_wall_list[3]

        elif abs(other_rect.left - self.rect.right) < collision_tolerance and self.direct.x > 0:
            self.direct = self.direct - 2 * self.direct.dot(Ball.normal_wall_list[1]) * Ball.normal_wall_list[1]
        # self.is_colliding = True

    def reset(self, pos):
        self.rect = pygame.Rect(pos, (self.w, self.w))
        self.direct = pygame.Vector2(self.init_direct).normalize()


class Ice:
    # crack = (pygame.image.load("crack5.png"),
    #          pygame.image.load("crack4.png"),
    #          pygame.image.load("crack3.png"),
    #          pygame.image.load("crack2.png"),
    #          pygame.image.load("crack1.png"))

    def __init__(self, x, y, w, h):
        self.max_strength = 5
        self.strength = round(random.uniform(1, self.max_strength))
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (int(self.strength*255/self.max_strength),
                      int(self.strength*255/self.max_strength),
                      int(self.strength*255/self.max_strength))

    def update_color(self):
        self.color = (int(self.strength * 255 / self.max_strength),
                      int(self.strength * 255 / self.max_strength),
                      int(self.strength * 255 / self.max_strength))

    def show(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        # if (st := int(self.strength * (len(Ice.crack) + 1) / self.max_strength)) != len(Ice.crack) + 1:
        #     surface.blit(Ice.crack[st-1], self.rect)

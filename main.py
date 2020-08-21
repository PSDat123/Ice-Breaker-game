# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pygame
import sys
import Objs
import random

# initialize

pygame.init()

# setup
is_running = True

screen_width = 960
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ice Breaker")
font = pygame.font.SysFont("Arial", 18)

bar_length = 170
bar = Objs.Bar(int((screen_width/2)-bar_length/2), int(screen_height-75), bar_length, 20, 15)

ball_w = 35
position, direction, speed, width = (int(bar.x+bar.w/2 - ball_w/2), int(bar.y - ball_w)), (1, -1), 8,  ball_w
ball = Objs.Ball(position, direction, speed, width)

# Colors
bg_color = (0, 0, 0)

# Walls Rectangles
wall_right = pygame.Rect(screen_width, 0, 30, screen_height)

wall_left = pygame.Rect(0 - 30, 0, 30, screen_height)

wall_top = pygame.Rect(0, 0-30, screen_width, 30)

wall_bot = pygame.Rect(0, screen_height, screen_width, 30)
wall_list = [wall_top, wall_right, wall_bot, wall_left]

col_num = 10
col_width = int(screen_width/col_num)
row_num = 8
row_width = int((screen_height/2)/row_num)

ice = {}


def get_random_ice(row_index=0):
    _list = []
    for col in range(col_num):
        if round(random.uniform(0, 1)):
            _list.append(Objs.Ice(col * col_width, row_index * row_width, col_width, row_width))
    return _list


def push_ice(row_index=0):
    for y in range(row_index, 0, -1):
        ice[y] = ice[y - 1]
        for z in ice[y]:
            z.rect.top += row_width
    ice[0] = get_random_ice()


for i in range(row_num):
    push_ice(i)
# Loop
while is_running:
    pygame.time.delay(16)
    # Input checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit out
            is_running = False

    # Moving
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        bar.direct.x = -1 if bar.rect.left > 0 else 0
        bar.update()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        bar.direct.x = 1 if bar.rect.right < screen_width else 0
        bar.update()
    # draw rect

    # collision checking
    if (index := ball.if_collide(wall_list)) != -1:
        if wall_list[index] is wall_bot:
            ball.reset((bar.rect.midtop[0] - ball.r, bar.rect.midtop[1] - ball.r * 2))
        else:
            ball.bounce(wall_list[index])

    if ball.if_collide([bar.rect]) != -1:
        ball.bounce(bar.rect)

    for i in range(row_num-1, -1, -1):
        if row_width * i <= ball.rect.top <= row_width * (i + 1) \
                or row_width * i <= ball.rect.bottom <= row_width * (i + 1):
            if (index := ball.if_collide(ice[i])) != -1:
                if not ball.invulnerable:
                    ball.bounce(ice[i][index].rect)

                ice[i][index].strength -= ball.pow
                ice[i][index].update_color()
                if ice[i][index].strength <= 0:
                    ice[i].pop(index)
                    if not ice[i]:
                        ice.pop(i)
                        push_ice(i)
                        # for j in range(i, 0, -1):
                        #     ice[j] = ice[j - 1]
                        #     for z in ice[j]:
                        #         z.rect.top += row_width
                        # ice[0] = get_random_ice()
                break

    ball.update()
    # for i in range(row_num):
    #     if i not in ice:
    #         for j in range(i, 0, -1):
    #             ice[j] = ice[j-1]
    #             for z in ice[j]:
    #                 z.rect.top += row_width
    #         ice[0] = get_random_ice()
    # Draw stuffs
    screen.fill(bg_color)

    for i in ice:
        for j in ice[i]:
            j.show(screen)

    bar.show(screen)
    ball.show(screen)

    # fps counter
    # fps = font.render(str(int(clock.get_fps())), True, white)
    # screen.blit(fps, (0, 0))

    # update window
    pygame.display.flip()
    # clock.tick(60)

pygame.quit()
sys.exit()

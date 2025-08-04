import sys
import pygame
from pygame.locals import Rect
from pygame.locals import *

pygame.init()

DARK_GRAY = (40, 40, 40)
GRAY = (80, 80, 80)
RED = (255, 0, 0)
GREEN = (0, 250, 0)
YELLOW = (250, 250, 20)
WHITE = (250, 250, 250)
BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
NASHI = (160, 160, 160)
PURPLE = (255, 0, 255)
LIME = (220, 220, 0)
ORANGE = (250, 180, 0)

screen = pygame.display.set_mode([600, 600])
pygame.display.set_caption("ekaki")
mouse_x, mouse_y = pygame.mouse.get_pos()
iro = 1
yoko = 0
yoko2 = 0
tate = 0
tate2 = 0
kaisu = 0

screen.fill((220, 220, 220))

for block in range(24):
    for block in range(24):
        pygame.draw.rect(screen, (NASHI), Rect(10 + yoko, 10 + tate, 20, 20))
        yoko += 20
    yoko = 0
    tate += 20
tate = 0
yoko = 0

pygame.draw.rect(screen, (NASHI), Rect(5, 500, 90, 90))
pygame.draw.rect(screen, (BLACK), Rect(105, 500, 90, 90))
pygame.draw.rect(screen, (RED), Rect(205, 500, 90, 90))
pygame.draw.rect(screen, (YELLOW), Rect(305, 500, 90, 90))
pygame.draw.rect(screen, (BLUE), Rect(405, 500, 90, 90))
pygame.draw.rect(screen, (GREEN), Rect(505, 500, 90, 90))
pygame.draw.rect(screen, (GRAY), Rect(505, 400, 90, 90))
pygame.draw.rect(screen, (WHITE), Rect(505, 300, 90, 90))
pygame.draw.rect(screen, (PURPLE), Rect(505, 200, 90, 90))
pygame.draw.rect(screen, (LIME), Rect(505, 100, 90, 90))
pygame.draw.rect(screen, (ORANGE), Rect(505, 0, 90, 90))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not running:
            break

    for block in range(24):
         for block in range(24):
            if mouse_x > 10 + yoko and mouse_x < 30 + yoko and mouse_y > 10 + tate and mouse_y < 30 + tate:
                if event.type == MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, (irob), Rect(10 + yoko, 10 + tate, 20, 20))
            yoko += 20
         yoko = 0
         tate += 20
    tate = 0
    yoko = 0
    
    if iro == 1:
        irob = NASHI
    else:
        if iro == 2:
            irob = BLACK
        else:
            if iro == 3:
                irob = RED
            else:
                if iro == 4:
                    irob = YELLOW
                else:
                    if iro == 5:
                        irob = BLUE
                    else:
                        if iro == 6:
                            irob = GREEN
                        else:
                            if iro == 7:
                                irob = GRAY
                            else:
                                if iro == 8:
                                    irob = WHITE
                                else:
                                    if iro == 9:
                                        irob = PURPLE
                                    else:
                                        if iro == 10:
                                            irob = LIME
                                        else:
                                            if iro == 11:
                                                irob = ORANGE

    for block in range(6):
        if mouse_x > 5 + yoko2 and mouse_x < 95 + yoko2 and mouse_y > 500 and mouse_y < 590:
            if event.type == MOUSEBUTTONDOWN:
                iro = 1 + kaisu
        yoko2 += 100
        kaisu += 1
    yoko2 = 0
    kaisu = 0

    for block in range(5):
        if mouse_x > 505 and mouse_x < 595 and mouse_y > 400 - tate2 and mouse_y < 490 - tate2:
            if event.type == MOUSEBUTTONDOWN:
                iro = 7 + kaisu
        tate2 += 100
        kaisu += 1
    tate2 = 0
    kaisu = 0

    mouse_x, mouse_y = pygame.mouse.get_pos()
   
    pygame.display.flip()
pygame.quit()
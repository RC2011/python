import sys
import pygame
from pygame.locals import Rect
from LCD_font_osero import LCD_font_styles
from LCD_font_osero import LCD_font
from pygame.locals import *
from time import sleep

def DisplayTarn(code):
    lcdtarn.update_col(col=1, code=code)
    lcdtarn.update_col(col=2, code=code + 1)
    lcdtarn.update_col(col=3, code=code + 2)
    lcdtarn.update_col(col=4, code=code+ 3)

pygame.init()

GREEN = (0, 100, 0)
GREEN2 = (0, 150, 0)
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode([820,970])
pygame.display.set_caption("osero")
screen.fill((0, 150, 0)) #RED, GREEN, BLUE
mouse_x, mouse_y = pygame.mouse.get_pos()
kurotarn = 1
kurotarn2 = 1
shirotarn = 0
shirotarn2 = 0
code = 0
x = 0
y = 0
oshita = 0

lcdtarn = LCD_font(screen)
lcdtarn.init_col(BLOCK_SIZE=15, BLOCK_INTV=15, COLOR_ON=BLACK, COLOR_OFF=GREEN2)
lcdtarn.init_row(X_ORG=2, Y_ORG=0.5, COL_INTV=6)

pygame.draw.rect(screen, (BLACK), Rect(10, 130, 800, 800))

for block in range(8):
    for block in range(8):
        pygame.draw.rect(screen, (GREEN), Rect(30 + x, 150 + y, 90, 90))
        x += 95
    x = 0
    y += 95
x = 0
y = 0

DisplayTarn(code)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not running:
            break

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for oshita in range(8):
        for oshita in range(8):
            if mouse_x > 30 + x and mouse_x < 120 + x and mouse_y > 150 + y and mouse_y < 240 + y:
                if event.type == MOUSEBUTTONDOWN:
                    if kurotarn == 1:
                        kurotarn = 0
                        kurotarn2 = 0
                        shirotarn = 1
                        shirotarn2 = 1
                        pygame.draw.circle(screen, (BLACK), (75 + x, 195 + y), 40)
                    if shirotarn == 1:
                        shirotarn = 0
                        shirotarn2 = 0
                        kurotarn = 1
                        kurotarn2 = 1
                        pygame.draw.circle(screen, (WHITE), (75 + x, 195 + y), 40)
            x += 95
        x = 0
        y += 95
    x = 0
    y = 0

    if kurotarn == 1:
        if kurotarn2 == 1:
            shirotarn = 0
            shirotarn2 = 0
            kurotarn2 = 0
            pygame.draw.circle(screen, (BLACK), (60, 60), 50)
    if shirotarn == 1:
        if shirotarn2 == 1:
            kurotarn = 0
            kurotarn2 = 0
            shirotarn2 = 0
            pygame.draw.circle(screen, (WHITE), (60, 60), 50)

    print(f"マウスの位置: ({x}, {y})")
    
    pygame.display.flip()
pygame.quit()
import sys
import pygame
from pygame.locals import Rect
from pygame.locals import *
from LCD_font import LCD_font_styles_ku
from LCD_font import LCD_font_ku
from time import sleep

pygame.init()

WHITE = (250, 250, 250)
BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
ORIZINARU = (0, 230, 0)

screen = pygame.display.set_mode([600, 600])
pygame.display.set_caption("pan clikker")
mouse_x, mouse_y = pygame.mouse.get_pos()
screen.fill((100, 100, 255))

pannnokazu = 0
panseisan = 1
seisansita = 1
utta = 1
kane = 9999999999
panseisankane = 50
panseisanhyouzi = 0
kanenoryou = 5
panseisanurikire = 0
urinekane = 50
urineurikire = 0
urinehyouzi = 0
torofikane = 9999999999
torofi = 0
torofihyouzi = 0

panlcd = LCD_font_ku(screen)
panlcd.init_col(BLOCK_SIZE=7, BLOCK_INTV=8, COLOR_ON=BLACK, COLOR_OFF=BLUE)
panlcd.init_row(X_ORG=2, Y_ORG=3, COL_INTV=6)

kanelcd = LCD_font_ku(screen)
kanelcd.init_col(BLOCK_SIZE=7, BLOCK_INTV=8, COLOR_ON=BLACK, COLOR_OFF=ORIZINARU)
kanelcd.init_row(X_ORG=13, Y_ORG=65, COL_INTV=6)

seisanlcd = LCD_font_ku(screen)
seisanlcd.init_col(BLOCK_SIZE=7, BLOCK_INTV=8, COLOR_ON=BLACK, COLOR_OFF=BLUE)
seisanlcd.init_row(X_ORG=33, Y_ORG=13, COL_INTV=6)

urinelcd = LCD_font_ku(screen)
urinelcd.init_col(BLOCK_SIZE=7, BLOCK_INTV=8, COLOR_ON=BLACK, COLOR_OFF=BLUE)
urinelcd.init_row(X_ORG=33, Y_ORG=22, COL_INTV=6)

torofilcd = LCD_font_ku(screen)
torofilcd.init_col(BLOCK_SIZE=7, BLOCK_INTV=8, COLOR_ON=BLACK, COLOR_OFF=BLUE)
torofilcd.init_row(X_ORG=15, Y_ORG=38, COL_INTV=6)

urulcd = LCD_font_ku(screen)
urulcd.init_col(BLOCK_SIZE=8, BLOCK_INTV=8, COLOR_ON=WHITE, COLOR_OFF=BLACK)
urulcd.init_row(X_ORG=54.5, Y_ORG=2, COL_INTV=6)

seisanuplcd = LCD_font_ku(screen)
seisanuplcd.init_col(BLOCK_SIZE=8, BLOCK_INTV=8, COLOR_ON=WHITE, COLOR_OFF=BLACK)
seisanuplcd.init_row(X_ORG=2.5, Y_ORG=12.75, COL_INTV=6)

urineuplcd = LCD_font_ku(screen)
urineuplcd.init_col(BLOCK_SIZE=8, BLOCK_INTV=8, COLOR_ON=WHITE, COLOR_OFF=BLACK)
urineuplcd.init_row(X_ORG=8.5, Y_ORG=21.5, COL_INTV=6)

torofiuplcd = LCD_font_ku(screen)
torofiuplcd.init_col(BLOCK_SIZE=8, BLOCK_INTV=8, COLOR_ON=WHITE, COLOR_OFF=BLACK)
torofiuplcd.init_row(X_ORG=5.5, Y_ORG=30, COL_INTV=6)

def DisplayKihon():
    screen.fill((100, 100, 255))
    pygame.draw.rect(screen, (0, 230, 0), Rect(0, 370, 600, 600))
    pygame.draw.rect(screen, (195, 215, 140), Rect(260, 400, 90, 92.5))
    pygame.draw.circle(screen, (195, 215, 140), (255, 446), 46)
    pygame.draw.circle(screen, (195, 215, 140), (355, 446), 46)
    pygame.draw.rect(screen, (150, 170, 100), Rect(260, 400, 15, 50))
    pygame.draw.rect(screen, (150, 170, 100), Rect(295, 400, 15, 50))
    pygame.draw.rect(screen, (150, 170, 100), Rect(330, 400, 15, 50))
    pygame.draw.rect(screen, (0, 0, 0), Rect(10, 100, 250, 60))
    pygame.draw.rect(screen, (0, 0, 0), Rect(430, 15, 100, 60))
    pygame.draw.rect(screen, (0, 0, 0), Rect(10, 170, 250, 60))
    pygame.draw.rect(screen, (0, 0, 0), Rect(10, 240, 250, 60))
    DisplayKaneNum(kane)
    DisplayPanNum(pannnokazu)
    if torofi == 1:
        DisplayGameClear()
    urulcd.update_col(col=0, code=36)
    urulcd.update_col(col=1, code=37)
    seisanuplcd.update_col(col=0, code=31)
    seisanuplcd.update_col(col=1, code=32)
    seisanuplcd.update_col(col=2, code=33)
    seisanuplcd.update_col(col=3, code=34)
    seisanuplcd.update_col(col=4, code=35)
    urineuplcd.update_col(col=2, code=46)
    urineuplcd.update_col(col=1, code=45)
    urineuplcd.update_col(col=0, code=36)
    torofiuplcd.update_col(col=0, code=47)
    torofiuplcd.update_col(col=1, code=48)
    torofiuplcd.update_col(col=2, code=49)
    torofiuplcd.update_col(col=3, code=50)
def DisplayPanNum(pannnokazu):
    panlcd.update_col(col=6, code=pannnokazu/1%10)
    panlcd.update_col(col=5, code=pannnokazu/10%10)
    panlcd.update_col(col=4, code=pannnokazu/100%10)
    panlcd.update_col(col=3, code=pannnokazu/1000%10)
    panlcd.update_col(col=2, code=pannnokazu/10000%10)
    panlcd.update_col(col=1, code=pannnokazu/100000%10)
    panlcd.update_col(col=0, code=pannnokazu/1000000%10)
def DisplayKaneNum(kane):
    kanelcd.update_col(col=9, code=kane/1%10)
    kanelcd.update_col(col=8, code=kane/10%10)
    kanelcd.update_col(col=7, code=kane/100%10)
    kanelcd.update_col(col=6, code=kane/1000%10)
    kanelcd.update_col(col=5, code=kane/10000%10)
    kanelcd.update_col(col=4, code=kane/100000%10)
    kanelcd.update_col(col=3, code=kane/1000000%10)
    kanelcd.update_col(col=2, code=kane/10000000%10)
    kanelcd.update_col(col=1, code=kane/100000000%10)
    kanelcd.update_col(col=0, code=kane/1000000000%10)
    kanelcd.update_col(col=-1, code=kane/10000000000%10)
def DisplaySeisanKaneNum(panseisankane):
    if panseisanurikire == 0:
        seisanlcd.update_col(col=6, code=panseisankane%10)
        seisanlcd.update_col(col=5, code=panseisankane/10%10)
        seisanlcd.update_col(col=4, code=panseisankane/100%10)
        seisanlcd.update_col(col=3, code=panseisankane/1000%10)
        seisanlcd.update_col(col=2, code=panseisankane/10000%10)
        seisanlcd.update_col(col=1, code=panseisankane/100000%10)
        seisanlcd.update_col(col=0, code=panseisankane/1000000%10)
    if panseisanurikire == 1:
        seisanlcd.update_col(col=0, code=39)
        seisanlcd.update_col(col=1, code=40)
        seisanlcd.update_col(col=2, code=41)
        seisanlcd.update_col(col=3, code=42)
        seisanlcd.update_col(col=4, code=40)
        seisanlcd.update_col(col=5, code=43)
        seisanlcd.update_col(col=6, code=44)
def DisplayUrineKaneNum(urinekane):
    if urineurikire == 0:
        urinelcd.update_col(col=6, code=urinekane%10)
        urinelcd.update_col(col=5, code=urinekane/10%10)
        urinelcd.update_col(col=4, code=urinekane/100%10)
        urinelcd.update_col(col=3, code=urinekane/1000%10)
        urinelcd.update_col(col=2, code=urinekane/10000%10)
        urinelcd.update_col(col=1, code=urinekane/100000%10)
        urinelcd.update_col(col=0, code=urinekane/1000000%10)
    if urineurikire == 1:
        urinelcd.update_col(col=0, code=39)
        urinelcd.update_col(col=1, code=40)
        urinelcd.update_col(col=2, code=41)
        urinelcd.update_col(col=3, code=42)
        urinelcd.update_col(col=4, code=40)
        urinelcd.update_col(col=5, code=43)
        urinelcd.update_col(col=6, code=44)
def DisplayTorofiKaneNum(torofikane):
    if torofi == 0:
        torofilcd.update_col(col=9, code=torofikane%10)
        torofilcd.update_col(col=8, code=torofikane/10%10)
        torofilcd.update_col(col=7, code=torofikane/100%10)
        torofilcd.update_col(col=6, code=torofikane/1000%10)
        torofilcd.update_col(col=5, code=torofikane/10000%10)
        torofilcd.update_col(col=4, code=torofikane/100000%10)
        torofilcd.update_col(col=3, code=torofikane/1000000%10)
        torofilcd.update_col(col=2, code=torofikane/10000000%10)
        torofilcd.update_col(col=1, code=torofikane/100000000%10)
        torofilcd.update_col(col=0, code=torofikane/1000000000%10)
def DisplayGameClear():
    torofilcd.update_col(col=0, code=55)
    torofilcd.update_col(col=1, code=53)
    torofilcd.update_col(col=2, code=56)
    torofilcd.update_col(col=3, code=52)
    torofilcd.update_col(col=4, code=51)
    torofilcd.update_col(col=5, code=41)
    torofilcd.update_col(col=6, code=52)
    torofilcd.update_col(col=7, code=53)
    torofilcd.update_col(col=8, code=54)
DisplayKihon()

running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not running:
            break

        # 作る！
        if mouse_x > 205 and mouse_x < 399 and mouse_y > 403 and mouse_y < 489:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pannnokazu= pannnokazu + panseisan
                seisansita = 1

        # 売る！
        if mouse_x > 430 and mouse_x < 528 and mouse_y > 14 and mouse_y < 73:
            if event.type == MOUSEBUTTONDOWN:
                if pannnokazu > 0:
                    kane=  (kane + kanenoryou * pannnokazu)
                    pannnokazu = 0
                    utta = 1
        # 生産力up！
        if mouse_x > 10 and mouse_x < 260 and mouse_y > 100 and mouse_y <160:
            if event.type == MOUSEBUTTONDOWN:
                if panseisan < 20 and kane > (panseisankane - 1):
                        panseisan= panseisan + 1
                        kane = kane - panseisankane
                        panseisankane= panseisankane * 1.5
                        katta = 1
        # 売値up！
        if mouse_x > 10 and mouse_x < 260 and mouse_y > 170 and mouse_y <230:
            if event.type == MOUSEBUTTONDOWN:
                if kanenoryou < 30 and kane > (urinekane - 1):
                        kanenoryou= kanenoryou + 1
                        kane= kane - urinekane
                        urinekane= urinekane * 1.5
                        katta = 1
        # トロフィ！
        if mouse_x > 10 and mouse_x < 260 and mouse_y > 240 and mouse_y <300:
            if event.type == MOUSEBUTTONDOWN:
                if torofi == 0 and kane > (torofikane - 1):
                        torofi= 1
                        kane= kane - torofikane
                        katta = 1   

    if kanenoryou == 30:
        urineurikire = 1

    if panseisan == 20:
        panseisanurikire = 1

    if mouse_x > 10 and mouse_x < 260 and mouse_y > 100 and mouse_y <160:
        panseisanhyouzi= 1
    else:
        panseisanhyouzi= 0
        DisplayKihon()
        sleep(panseisanhyouzi==1)

    if mouse_x > 10 and mouse_x < 260 and mouse_y > 170 and mouse_y <230:
        urinehyouzi= 1
    else:
        urinehyouzi= 0
        DisplayKihon()
        sleep(urinehyouzi==1)

    if mouse_x > 10 and mouse_x < 260 and mouse_y > 240 and mouse_y <300:
        torofihyouzi= 1
    else:
        torofihyouzi= 0
        DisplayKihon()
        sleep(torofihyouzi==1)

    if panseisanhyouzi == 1:
        DisplaySeisanKaneNum(panseisankane)

    if urinehyouzi == 1:
        DisplayUrineKaneNum(urinekane)

    if torofihyouzi == 1:
        DisplayTorofiKaneNum(torofikane)

    if seisansita == 1:
        DisplayPanNum(pannnokazu)

    if utta or katta == 1:
        DisplayKaneNum(kane)
        DisplayPanNum(pannnokazu)

    seisansita = 0
    utta = 0
    katta = 0
    
    pygame.display.flip()
pygame.quit()
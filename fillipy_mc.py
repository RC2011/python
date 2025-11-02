# Flippy (an Othello or Reversi clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# Based on the "reversi.py" code that originally appeared in "Invent
# Your Own Computer Games with Python", chapter 15:
#   http://inventwithpython.com/chapter15.html

import sys
import pygame
from pygame.locals import Rect
from pygame.locals import *
from mc_remote.minecraft import Minecraft
import param_mc_remote as param
from param_mc_remote import PLAYER_ORIGIN as PO
from param_mc_remote import block

import random, sys, pygame, time, copy
from pygame.locals import *

x, y, z = 20, param.Y_SEA + 43, -40

mc = Minecraft.create(address=param.ADRS_MCR, port=param.PORT_MCR)
mc.setPlayer(param.PLAYER_NAME, PO.x, PO.y, PO.z)

for _i in range(33):
    for _i in range(33):
        mc.setBlock(
            x, y, z, param.block.BLUE_CONCRETE)
        
        x -= 1
    
    x += 33
    y += 1

x, y, z = 19, param.Y_SEA + 44, -40
for _i in range(31):
    for _i in range(31):
        mc.setBlock(
            x, y, z, param.block.GREEN_CONCRETE)
        
        x -= 1
    
    x += 31
    y += 1

x, y, z = 16, param.Y_SEA + 44, -40
for _i in range(7):
    for _i in range(31):
        mc.setBlock(
            x, y, z, param.block.BLUE_CONCRETE)
        y += 1
    y -= 31
    
    x -= 4

x, y, z = 19, param.Y_SEA + 47, -40
for _i in range(7):
    for _i in range(31):
        mc.setBlock(
            x, y, z, param.block.BLUE_CONCRETE)
        
        x -= 1
    
    x += 31
    y += 4


x, y, z = 19, param.Y_SEA + 44, -40

FPS = 10 # frames per second to update the screen
WINDOWWIDTH = 640 # width of the program's window, in pixels
WINDOWHEIGHT = 480 # height in pixels
SPACESIZE = 50 # width & height of each space on the board, in pixels
MCSPACESIZE = 33
BOARDWIDTH = 8 # how many columns of spaces on the game board
BOARDHEIGHT = 8 # how many rows of spaces on the game board
WHITE_TILE = 'WHITE_TILE' # an arbitrary but unique value
BLACK_TILE = 'BLACK_TILE' # an arbitrary but unique value
EMPTY_SPACE = 'EMPTY_SPACE' # an arbitrary but unique value
HINT_TILE = 'HINT_TILE' # an arbitrary but unique value
ANIMATIONSPEED = 25 # integer from 1 to 100, higher is faster animation
sita = 0
migi = 0

# Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)
MCMARGIN = int((MCSPACESIZE - (MCSPACESIZE * MCSPACESIZE)) / 2)

#              R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN


def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Flippy')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    # Set up the background image.
    boardImage = pygame.image.load('flippyboard.png')
    # Use smoothscale() to stretch the board image to fit the entire board:
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (XMARGIN, YMARGIN)
    BGIMAGE = pygame.image.load('flippybackground.png')
    # Use smoothscale() to stretch the background image to fit the entire window:
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(boardImage, boardImageRect)

    # Run the main game.
    while True:
        if runGame() == False:
            break


def runGame():
    # Plays a single game of reversi each time this function is called.

    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    showHints = False
    turn = random.choice(['computer', 'player'])

    # Draw the starting board and ask the player what color they want.
    drawBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()

    # Make the Surface and Rect objects for the "New Game" and "Hints" buttons
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)
    hintsSurf = FONT.render('Hints', True, TEXTCOLOR, TEXTBGCOLOR2)
    hintsRect = hintsSurf.get_rect()
    hintsRect.topright = (WINDOWWIDTH - 8, 40)

    while True: # main game loop
        # Keep looping for player and computer's turns.
        if turn == 'player':
            # Player's turn:
            if getValidMoves(mainBoard, playerTile) == []:
                # If it's the player's turn but they
                # can't move, then end the game.
                break
            movexy = None
            while movexy == None:
                # Keep looping until the player clicks on a valid space.

                # Determine which board data structure to use for display.
                if showHints:
                    boardToDraw = getBoardWithValidMoves(mainBoard, playerTile)
                else:
                    boardToDraw = mainBoard

                checkForQuit()
                for event in pygame.event.get(): # event handling loop
                    if event.type == MOUSEBUTTONUP:
                        # Handle mouse click events
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint( (mousex, mousey) ):
                            # Start a new game
                            return True
                        elif hintsRect.collidepoint( (mousex, mousey) ):
                            # Toggle hints mode
                            showHints = not showHints
                        # movexy is set to a two-item tuple XY coordinate, or None value
                        movexy = getSpaceClicked(mousex, mousey)
                        if movexy != None and not isValidMove(mainBoard, playerTile, movexy[0], movexy[1]):
                            movexy = None

                # Draw the game board.
                drawBoard(boardToDraw)
                drawInfo(boardToDraw, playerTile, computerTile, turn)

                # Draw the "New Game" and "Hints" buttons.
                DISPLAYSURF.blit(newGameSurf, newGameRect)
                DISPLAYSURF.blit(hintsSurf, hintsRect)

                MAINCLOCK.tick(FPS)
                pygame.display.update()

            # Make the move and end the turn.
            makeMove(mainBoard, playerTile, movexy[0], movexy[1], True)
            if getValidMoves(mainBoard, computerTile) != []:
                # Only set for the computer's turn if it can make a move.
                turn = 'computer'

        else:
            # Computer's turn:
            if getValidMoves(mainBoard, computerTile) == []:
                # If it was set to be the computer's turn but
                # they can't move, then end the game.
                break

            # Draw the board.
            drawBoard(mainBoard)
            drawInfo(mainBoard, playerTile, computerTile, turn)

            # Draw the "New Game" and "Hints" buttons.
            DISPLAYSURF.blit(newGameSurf, newGameRect)
            DISPLAYSURF.blit(hintsSurf, hintsRect)

            # Make it look like the computer is thinking by pausing a bit.
            pauseUntil = time.time() + random.randint(5, 15) * 0.1
            while time.time() < pauseUntil:
                pygame.display.update()

            # Make the move and end the turn.
            fillipyx, fillipyy = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, fillipyx, fillipyy, True)
            if getValidMoves(mainBoard, playerTile) != []:
                # Only set for the player's turn if they can make a move.
                turn = 'player'

    # Display the final score.
    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)

    # Determine the text of the message to display.
    if scores[playerTile] > scores[computerTile]:
        text = 'You beat the computer by %s points! Congratulations!' % \
               (scores[playerTile] - scores[computerTile])
    elif scores[playerTile] < scores[computerTile]:
        text = 'You lost. The computer beat you by %s points.' % \
               (scores[computerTile] - scores[playerTile])
    else:
        text = 'The game was a tie!'

    textSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(textSurf, textRect)

    # Display the "Play again?" text with Yes and No buttons.
    text2Surf = BIGFONT.render('Play again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)

    # Make "Yes" button.
    yesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 90)

    # Make "No" button.
    noSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 90)

    while True:
        # Process events until the user clicks on Yes or No.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint( (mousex, mousey) ):
                    return True
                elif noRect.collidepoint( (mousex, mousey) ):
                    return False
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def translateBoardToPixelCoord(fillipyx, fillipyy):
    return XMARGIN + fillipyx * SPACESIZE + int(SPACESIZE / 2), YMARGIN + fillipyy * SPACESIZE + int(SPACESIZE / 2)


def animateTileChange(tilesToFlip, tileColor, additionalTile):
    # Draw the additional tile that was just laid down. (Otherwise we'd
    # have to completely redraw the board & the board info.)
    if tileColor == WHITE_TILE:
        additionalTileColor = WHITE
    else:
        additionalTileColor = BLACK
    additionalTileX, additionalTileY = translateBoardToPixelCoord(additionalTile[0], additionalTile[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4) #ここで円を描いている 左上は121, 41でそこから50ずつ増えることでマスがかわる
    sita = 0
    migi = 0
    mcsita = 0
    mcmigi = 0
    for yoko in range(8):
        for tate in range(8):
            if additionalTileY > 40 + sita and additionalTileY < 90 + sita and additionalTileX > 120 + migi and additionalTileX < 170 + migi:
                x, y, z = -9 + mcmigi, param.Y_SEA + 72 - mcsita, -40
                for koma in range(3):
                    for koma in range(3):
                        mc.setBlock(x, y, z, param.block.WHITE_CONCRETE if additionalTileColor == WHITE else param.block.BLACK_CONCRETE)
                        x -= 1
                    x += 3
                    y += 1
            sita += 50
            mcsita += 4
        migi += 50
        mcmigi += 4
        mcsita = 0
        sita = 0
    sita = 50
    migi = 50
    mcsita = 0
    mcmigi = 0
    pygame.display.update()

    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        if tileColor == WHITE_TILE:
            color = tuple([rgbValues] * 3) # rgbValues goes from 0 to 255
        elif tileColor == BLACK_TILE:
            color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0

        for fillipyx, fillipyy in tilesToFlip:
            centerx, centery = translateBoardToPixelCoord(fillipyx, fillipyy)
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4) #ここで円を描いている
            sita = 0
            migi = 0
            mcsita = 0
            mcmigi = 0
            for yoko in range(8):
                for tate in range(8):
                    if additionalTileY > 40 + sita and additionalTileY < 90 + sita and additionalTileX > 120 + migi and additionalTileX < 170 + migi:
                        x, y, z = -9 + mcmigi, param.Y_SEA + 72 - mcsita, -40
                        for koma in range(3):
                            for koma in range(3):
                                mc.setBlock(x, y, z, param.block.WHITE_CONCRETE if additionalTileColor == WHITE else param.block.BLACK_CONCRETE)
                                x -= 1
                            x += 3
                            y += 1
                    sita += 50
                    mcsita += 4
                migi += 50
                mcmigi += 4
                mcsita = 0
                sita = 0
            sita = 50
            migi = 50
            mcsita = 0
            mcmigi = 0
        
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        checkForQuit()


def drawBoard(board):
    # Draw background of board.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

    # Draw grid lines of the board.
    for fillipyx in range(BOARDWIDTH + 1):
        # Draw the horizontal lines.
        startx = (fillipyx * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (fillipyx * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
    for fillipyy in range(BOARDHEIGHT + 1):
        # Draw the vertical lines.
        startx = XMARGIN
        starty = (fillipyy * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (fillipyy * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

    # Draw the black & white tiles or hint spots.
    for fillipyx in range(BOARDWIDTH):
        for fillipyy in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(fillipyx, fillipyy)
            if board[fillipyx][fillipyy] == WHITE_TILE or board[fillipyx][fillipyy] == BLACK_TILE:
                if board[fillipyx][fillipyy] == WHITE_TILE:
                    tileColor = WHITE
                else:
                    tileColor = BLACK
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4) #ここで円を描いている
                sita = 0
                migi = 0
                mcsita = 0
                mcmigi = 0
                for yoko in range(8):
                    for tate in range(8):
                        if centery > 40 + sita and centery < 90 + sita and centerx > 120 + migi and centerx < 170 + migi:
                            x, y, z = -9 + mcmigi, param.Y_SEA + 72 - mcsita, -40
                            for koma in range(3):
                                for koma in range(3):
                                    mc.setBlock(x, y, z, param.block.WHITE_CONCRETE if tileColor == WHITE else param.block.BLACK_CONCRETE)
                                    x -= 1
                                x += 3
                                y += 1
                        sita += 50
                        mcsita += 4
                    migi += 50
                    mcmigi += 4
                    mcsita = 0
                    sita = 0
                sita = 50
                migi = 50
                mcsita = 0
                mcmigi = 0
            if board[fillipyx][fillipyy] == HINT_TILE:
                pygame.draw.rect(DISPLAYSURF, HINTCOLOR, (centerx - 4, centery - 4, 8, 8))


def getSpaceClicked(mousex, mousey):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for fillipyx in range(BOARDWIDTH):
        for fillipyy in range(BOARDHEIGHT):
            if mousex > fillipyx * SPACESIZE + XMARGIN and \
               mousex < (fillipyx + 1) * SPACESIZE + XMARGIN and \
               mousey > fillipyy * SPACESIZE + YMARGIN and \
               mousey < (fillipyy + 1) * SPACESIZE + YMARGIN:
                return (fillipyx, fillipyy)
    return None


def drawInfo(board, playerTile, computerTile, turn):
    # Draws scores and whose turn it is at the bottom of the screen.
    scores = getScoreOfBoard(board)
    scoreSurf = FONT.render("Player Score: %s    Computer Score: %s    %s's Turn" % (str(scores[playerTile]), str(scores[computerTile]), turn.title()), True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, WINDOWHEIGHT - 5)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def resetBoard(board):
    # Blanks out the board it is passed, and sets up starting tiles.
    for fillipyx in range(BOARDWIDTH):
        for fillipyy in range(BOARDHEIGHT):
            board[fillipyx][fillipyy] = EMPTY_SPACE

    # Add starting pieces to the center
    board[3][3] = WHITE_TILE
    board[3][4] = BLACK_TILE
    board[4][3] = BLACK_TILE
    board[4][4] = WHITE_TILE


def getNewBoard():
    # Creates a brand new, empty board data structure.
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move is invalid. If it is a valid
    # move, returns a list of spaces of the captured pieces.
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == WHITE_TILE:
        otherTile = BLACK_TILE
    else:
        otherTile = WHITE_TILE

    tilesToFlip = []
    # check each of the eight directions:
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        fillipyx, fillipyy = xstart, ystart
        fillipyx += xdirection
        fillipyy += ydirection
        if isOnBoard(fillipyx, fillipyy) and board[fillipyx][fillipyy] == otherTile:
            # The piece belongs to the other player next to our piece.
            fillipyx += xdirection
            fillipyy += ydirection
            if not isOnBoard(fillipyx, fillipyy):
                continue
            while board[fillipyx][fillipyy] == otherTile:
                fillipyx += xdirection
                fillipyy += ydirection
                if not isOnBoard(fillipyx, fillipyy):
                    break # break out of while loop, continue in for loop
            if not isOnBoard(fillipyx, fillipyy):
                continue
            if board[fillipyx][fillipyy] == tile:
                # There are pieces to flip over. Go in the reverse
                # direction until we reach the original space, noting all
                # the tiles along the way.
                while True:
                    fillipyx -= xdirection
                    fillipyy -= ydirection
                    if fillipyx == xstart and fillipyy == ystart:
                        break
                    tilesToFlip.append([fillipyx, fillipyy])

    board[xstart][ystart] = EMPTY_SPACE # make space empty
    if len(tilesToFlip) == 0: # If no tiles flipped, this move is invalid
        return False
    return tilesToFlip


def isOnBoard(fillipyx, fillipyy):
    # Returns True if the coordinates are located on the board.
    return fillipyx >= 0 and fillipyx < BOARDWIDTH and fillipyy >= 0 and fillipyy < BOARDHEIGHT


def getBoardWithValidMoves(board, tile):
    # Returns a new board with hint markings.
    dupeBoard = copy.deepcopy(board)

    for fillipyx, fillipyy in getValidMoves(dupeBoard, tile):
        dupeBoard[fillipyx][fillipyy] = HINT_TILE
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of (fillipyx,fillipyy) tuples of all valid moves.
    validMoves = []

    for fillipyx in range(BOARDWIDTH):
        for fillipyy in range(BOARDHEIGHT):
            if isValidMove(board, tile, fillipyx, fillipyy) != False:
                validMoves.append((fillipyx, fillipyy))
    return validMoves


def getScoreOfBoard(board):
    # Determine the score by counting the tiles.
    xscore = 0
    oscore = 0
    for fillipyx in range(BOARDWIDTH):
        for fillipyy in range(BOARDHEIGHT):
            if board[fillipyx][fillipyy] == WHITE_TILE:
                xscore += 1
            if board[fillipyx][fillipyy] == BLACK_TILE:
                oscore += 1
    return {WHITE_TILE:xscore, BLACK_TILE:oscore}


def enterPlayerTile():
    # Draws the text and handles the mouse click events for letting
    # the player choose which color they want to be.  Returns
    # [WHITE_TILE, BLACK_TILE] if the player chooses to be White,
    # [BLACK_TILE, WHITE_TILE] if Black.

    # Create the text.
    textSurf = FONT.render('Do you want to be white or black?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    xSurf = BIGFONT.render('White', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    oSurf = BIGFONT.render('Black', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint( (mousex, mousey) ):
                    return [WHITE_TILE, BLACK_TILE]
                elif oRect.collidepoint( (mousex, mousey) ):
                    return [BLACK_TILE, WHITE_TILE]

        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def makeMove(board, tile, xstart, ystart, realMove=False):
    # Place the tile on the board at xstart, ystart, and flip tiles
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile

    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart, ystart))

    for fillipyx, fillipyy in tilesToFlip:
        board[fillipyx][fillipyy] = tile
    return True


def isOnCorner(fillipyx, fillipyy):
    # Returns True if the position is in one of the four corners.
    return (fillipyx == 0 and fillipyy == 0) or \
           (fillipyx == BOARDWIDTH and fillipyy == 0) or \
           (fillipyx == 0 and fillipyy == BOARDHEIGHT) or \
           (fillipyx == BOARDWIDTH and fillipyy == BOARDHEIGHT)


def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [fillipyx, fillipyy] list.
    possibleMoves = getValidMoves(board, computerTile)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # always go for a corner if available.
    for fillipyx, fillipyy in possibleMoves:
        if isOnCorner(fillipyx, fillipyy):
            return [fillipyx, fillipyy]

    # Go through all possible moves and remember the best scoring move
    bestScore = -1
    for fillipyx, fillipyy in possibleMoves:
        dupeBoard = copy.deepcopy(board)
        makeMove(dupeBoard, computerTile, fillipyx, fillipyy)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [fillipyx, fillipyy]
            bestScore = score
    return bestMove


def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()

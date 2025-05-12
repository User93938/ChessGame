"""
This is our main driver file. It will be responsible for handling user input and display the current GameState objects.
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp','wR','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))

def main():
    global sqSelected, validSquareMoves
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    validSquareMoves = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                    validSquareMoves = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    validSquareMoves = [m for m in validMoves if m.startRow == row and m.startCol == col]
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        animateMove(move, screen, gs.board, clock)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                        validSquareMoves = []
                    else:
                        playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    validMoves = gs.getValidMoves()
                    moveMade = True
                    sqSelected = ()
                    playerClicks = []
                    validSquareMoves = []

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    highlightSquares(screen, gs)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('light blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))

            for move in validSquareMoves:
                endRow, endCol = move.endRow, move.endCol
                if gs.board[endRow][endCol] == '--':
                    # Gray dot for non-captures
                    center = (endCol * SQ_SIZE + SQ_SIZE // 2, endRow * SQ_SIZE + SQ_SIZE // 2)
                    p.draw.circle(screen, (128, 128, 128, 100), center, 10)
                else:
                    # Blue overlay for capture squares
                    s = p.Surface((SQ_SIZE, SQ_SIZE))
                    s.set_alpha(100)
                    s.fill(p.Color('red'))
                    screen.blit(s, (endCol * SQ_SIZE, endRow * SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE , SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, board, clock):
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 4
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare

    piece = board[move.endRow][move.endCol]

    for frame in range(frameCount + 1):
        r = move.startRow + dR * frame / frameCount
        c = move.startCol + dC * frame / frameCount
        drawBoard(screen)
        drawPieces(screen, board)

        color = p.Color("white") if (move.endRow + move.endCol) % 2 == 0 else p.Color("grey")
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        p.display.flip()
        clock.tick(60)

if __name__== "__main__":
    main()

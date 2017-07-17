import pygame, sys
from pygame.locals import *

# Change FPS
FPS = 200

WindowWidth = 800
WindowHeight = 600

LineThickness = 10
PaddleSize = 50
PaddleOffset = 20

Black = (0, 0, 0)
White = (255, 255, 255)


def DrawArena():
    DisplaySurf.fill((0, 0, 0))
    pygame.draw.rect(DisplaySurf, White, ((0, 0), (WindowWidth, WindowHeight)),
                     LineThickness * 2)
    pygame.draw.line(DisplaySurf, White, ((WindowWidth / 2), 0),
                     ((WindowWidth / 2), WindowHeight), (LineThickness / 4))


def DrawPaddle(paddle):
    if paddle.bottom > WindowHeight - LineThickness:
        paddle.bottom = WindowHeight - LineThickness
    elif paddle.top < LineThickness:
        paddle.top = LineThickness
    pygame.draw.rect(DisplaySurf, White, paddle)


def DrawBall(ball):
    pygame.draw.rect(DisplaySurf, White, ball)


def MoveBall(ball, balldirx, balldiry):
    ball.x += balldirx * BallSpeed
    ball.y += balldiry * BallSpeed
    return ball


def CheckEdgeCollision(ball, balldirx, balldiry):
    if ball.top == (LineThickness) or ball.bottom == (
            WindowHeight - LineThickness):
        balldiry = balldiry * -1
    if ball.left == (LineThickness) or ball.right == (
            WindowWidth - LineThickness):
        balldirx = balldirx * -1
    return balldirx, balldiry


def CheckHitBall(ball, paddle1, paddle2, balldirx):
    if balldirx == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif balldirx == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else:
        return 1


def CheckPointScored(ball, score1, score2, balldirx):
    if ball.left == LineThickness:
        score2 += 1
        return score1, score2
    elif ball.right == WindowWidth - LineThickness:
        score1 += 1
        return score1, score2
    else:
        return score1, score2


def AI(ball, balldirx, paddle2):
    if balldirx == -1:
        if paddle2.centery < (WindowHeight / 2):
            paddle2.y += 1
        elif paddle2.centery > (WindowHeight / 2):
            paddle2.y -= 1
    elif balldirx == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -= 1
    return paddle2


def DisplayScore(score1, score2):
    ResultSurf = BasicFont.render("%i" % (score1), True, White)
    ResultRect = ResultSurf.get_rect()
    ResultRect.topleft = (WindowWidth / 4, LineThickness * 2)
    DisplaySurf.blit(ResultSurf, ResultRect)
    ResultSurf = BasicFont.render("%i" % (score2), True, White)
    ResultRect = ResultSurf.get_rect()
    ResultRect.topleft = (WindowWidth - (WindowWidth / 4), LineThickness * 2)
    DisplaySurf.blit(ResultSurf, ResultRect)


def main():
    pygame.init()
    global DisplaySurf
    global BasicFont, BasicFontSize
    global BallSpeed
    BallSpeed = 1
    BasicFontSize = 50
    BasicFont = pygame.font.Font("freesansbold.ttf", BasicFontSize)

    FpsClock = pygame.time.Clock()
    DisplaySurf = pygame.display.set_mode((WindowWidth, WindowHeight))
    pygame.display.set_caption("Pong")

    ballx = WindowWidth / 2 - LineThickness / 2
    bally = WindowHeight / 2 - LineThickness / 2
    playerOnePosition = (WindowHeight - PaddleSize) / 2
    playerTwoPosition = (WindowHeight - PaddleSize) / 2
    score1 = 0
    score2 = 0
    hitcount = 0

    balldirx = -1
    balldiry = -1

    paddle1 = pygame.Rect(PaddleOffset, playerOnePosition, LineThickness,
                          PaddleSize)
    paddle2 = pygame.Rect(WindowWidth - PaddleOffset - LineThickness,
                          playerTwoPosition, LineThickness, PaddleSize)
    ball = pygame.Rect(ballx, bally, LineThickness, LineThickness)

    DrawArena()
    DrawPaddle(paddle1)
    DrawPaddle(paddle2)
    DrawBall(ball)

    pygame.mouse.set_visible(0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey
        keys = pygame.key.get_pressed()
        if keys[113]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_UP]:
            paddle1.y -= 1
        if keys[pygame.K_DOWN]:
            paddle1.y += 1

        DrawArena()
        DrawPaddle(paddle1)
        DrawPaddle(paddle2)
        DrawBall(ball)

        ball = MoveBall(ball, balldirx, balldiry)
        balldirx, balldiry = CheckEdgeCollision(ball, balldirx, balldiry)
        score1, score2 = CheckPointScored(ball, score1, score2, balldirx)
        if CheckHitBall(ball, paddle1, paddle2, balldirx) == -1:
            hitcount += 1
            if hitcount % 5 == 0:
                hitcount = 0
                BallSpeed += 1
        balldirx = balldirx * CheckHitBall(ball, paddle1, paddle2, balldirx)
        paddle2 = AI(ball, balldirx, paddle2)
        DisplayScore(score1, score2)

        pygame.display.update()
        FpsClock.tick(FPS)


if __name__ == '__main__':
    main()

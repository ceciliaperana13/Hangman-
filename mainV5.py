import pygame
from settings import SCREENWIDTH, SCREENHEIGHT
from game import HangmanGame

pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Hangman")

game = HangmanGame(screen)
clock = pygame.time.Clock()
RUN = True

while RUN:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.handleClick(event.pos)

    game.checkGameOver()
    game.draw()
    pygame.display.update()

pygame.quit()

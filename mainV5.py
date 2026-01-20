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

        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.handleClick(event.pos)

        # Keyboard handling
        if event.type == pygame.KEYDOWN:
            # Pass the character typed to handleKey
            game.handleKey(event.unicode)

    game.checkGameOver()
    game.draw()
    pygame.display.update()

pygame.quit()


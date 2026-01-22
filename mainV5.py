import pygame
from game import HangmanGame
from settings import SCREENWIDTH, SCREENHEIGHT


def main(screen):
    #  Force the hangman's resolution
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Hangman")

    clock = pygame.time.Clock()
    game = HangmanGame(screen)
    RUN = True

    while RUN:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handleClick(event.pos)

            if event.type == pygame.KEYDOWN:
                game.handleKey(event.unicode)

        game.checkGameOver()
        game.draw()
        pygame.display.update()




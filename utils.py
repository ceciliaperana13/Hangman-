import pygame
import sys
from settings import FONT, WHITE, SCREENWIDTH

def loadWords(filename="easyWordList.txt"):
    words = []
    try:
        with open(filename, "r") as file:
            for line in file:
                for word in line.split(","):
                    word = word.strip()
                    if 3 <= len(word) <= 10:
                        words.append(word.upper())
    except FileNotFoundError:
        print("Fichier de mots introuvable")
        pygame.quit()
        sys.exit()

    return words


def drawLetters(text):
    return FONT.render(text, True, WHITE)


def drawLetterLines(screen, chosenWord, guessWord):
    start_x = SCREENWIDTH // 2 - (len(chosenWord) * 40) // 2
    y = 350

    for i in range(len(chosenWord)):
        pygame.draw.line(screen, WHITE, (start_x, y), (start_x + 25, y), 3)
        if guessWord[i] != " ":
            screen.blit(drawLetters(guessWord[i]), (start_x + 5, y - 30))
        start_x += 40


def drawHangman(screen, guesses):
    pygame.draw.line(screen, WHITE, (100, 400), (275, 400), 3)
    pygame.draw.line(screen, WHITE, (125, 400), (125, 50), 3)
    pygame.draw.line(screen, WHITE, (125, 50), (275, 50), 3)
    pygame.draw.line(screen, WHITE, (275, 50), (275, 125), 3)

    if guesses >= 1:
        pygame.draw.circle(screen, WHITE, (275, 150), 25, 3)
    if guesses >= 2:
        pygame.draw.line(screen, WHITE, (275, 175), (275, 230), 3)
    if guesses >= 3:
        pygame.draw.line(screen, WHITE, (275, 185), (245, 215), 3)
    if guesses >= 4:
        pygame.draw.line(screen, WHITE, (275, 185), (305, 215), 3)
    if guesses >= 5:
        pygame.draw.line(screen, WHITE, (275, 230), (250, 270), 3)
    if guesses >= 6:
        pygame.draw.line(screen, WHITE, (275, 230), (300, 270), 3)

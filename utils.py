import pygame
import sys
from settings import FONT, WHITE, SCREENWIDTH

def load_words(filename="easyWordList.txt"):
    """
    Load words from a file and return a list of valid words.
    Only words with length between 3 and 10 characters are kept.
    """
    words = []
    try:
        with open(filename, "r") as file:
            for line in file:
                for word in line.split(","):
                    word = word.strip()
                    if 3 <= len(word) <= 10:
                        words.append(word.upper())
    except FileNotFoundError:
        print("Word file not found!")
        pygame.quit()
        sys.exit()
    return words


def draw_letters(text):
    """Render a single letter with the default font and color."""
    return FONT.render(text, True, WHITE)


def draw_letter_lines(screen, chosen_word, guess_word):
    """
    Draw the underline for each letter in the chosen word.
    If the letter is guessed, display it above the line.
    """
    start_x = SCREENWIDTH // 2 - (len(chosen_word) * 40) // 2
    y = 350

    for i in range(len(chosen_word)):
        # Draw the line for the letter
        pygame.draw.line(screen, WHITE, (start_x, y), (start_x + 25, y), 3)

        # Draw guessed letter if present
        if guess_word[i] != " ":
            screen.blit(draw_letters(guess_word[i]), (start_x + 5, y - 30))
        start_x += 40


def draw_hangman(screen, guesses):
    """
    Draw the hangman scaffold and body parts based on the number of wrong guesses.
    There are 6 allowed wrong guesses.
    """
    # Scaffold
    pygame.draw.line(screen, WHITE, (100, 400), (275, 400), 3)  # Base
    pygame.draw.line(screen, WHITE, (125, 400), (125, 50), 3)   # Pole
    pygame.draw.line(screen, WHITE, (125, 50), (275, 50), 3)    # Top beam
    pygame.draw.line(screen, WHITE, (275, 50), (275, 125), 3)   # Rope support

    # Hangman body parts
    if guesses >= 1:  # Head
        pygame.draw.circle(screen, WHITE, (275, 150), 25, 3)
    if guesses >= 2:  # Body
        pygame.draw.line(screen, WHITE, (275, 175), (275, 230), 3)
    if guesses >= 3:  # Left arm
        pygame.draw.line(screen, WHITE, (275, 185), (245, 215), 3)
    if guesses >= 4:  # Right arm
        pygame.draw.line(screen, WHITE, (275, 185), (305, 215), 3)
    if guesses >= 5:  # Left leg
        pygame.draw.line(screen, WHITE, (275, 230), (250, 270), 3)
    if guesses >= 6:  # Right leg
        pygame.draw.line(screen, WHITE, (275, 230), (300, 270), 3
        )

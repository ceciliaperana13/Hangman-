import random
import pygame
from settings import BLACK, SCREENWIDTH, SCREENHEIGHT
from utils import drawLetterLines, drawHangman, drawLetters, loadWords
from buttons import HangmanButton

WORDLIST = loadWords()

class HangmanGame:
    def __init__(self, screen):
        self.screen = screen
        self.winStreak = 0
        self.reset()

    def reset(self):
        # Pick a new random word and reset game values
        self.chosenWord = random.choice(WORDLIST)
        self.guessWord = [" " for _ in self.chosenWord]
        self.numberOfGuesses = 0
        self.gameOver = False
        self.createAlphabet()

    def createAlphabet(self):
        # Create buttons for each letter of the alphabet
        self.buttons = []
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        x, y = 100, 500
        index = 0

        for row in [9, 9, 8]:  # Layout in rows
            for _ in range(row):
                self.buttons.append(HangmanButton((x, y), alphabet[index]))
                index += 1
                x += 50
            x = 100
            y += 40

    def handleClick(self, pos):
        # Handle letter button click
        if self.gameOver:
            # Restart game if over
            self.reset()
            return

        for button in self.buttons:
            if button.active and button.rect.collidepoint(pos):
                if button.letter in self.chosenWord:
                    for i, letter in enumerate(self.chosenWord):
                        if letter == button.letter:
                            self.guessWord[i] = letter
                else:
                    self.numberOfGuesses += 1

                # Deactivate the button
                button.active = False
                break

    def handleKey(self, key):
        # Handle key press from keyboard
        if self.gameOver:
            # Restart game if over
            self.reset()
            return

        # ConGREEN key to uppercase (buttons are uppercase)
        letter = key.upper()

        # Only accept letters A-Z
        if letter.isalpha() and len(letter) == 1:
            for button in self.buttons:
                if button.letter == letter and button.active:
                    if button.letter in self.chosenWord:
                        for i, l in enumerate(self.chosenWord):
                            if l == button.letter:
                                self.guessWord[i] = l
                    else:
                        self.numberOfGuesses += 1

                    # Deactivate the button
                    button.active = False
                    break

    def checkGameOver(self):
        # Check if the player has won or lost
        if "".join(self.guessWord) == self.chosenWord:
            self.winStreak += 1
            self.gameOver = True
        elif self.numberOfGuesses >= 6:
            self.winStreak = 0
            self.gameOver = True

    def draw(self):
        # Draw everything on the screen
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        drawLetterLines(self.screen, self.chosenWord, self.guessWord)
        drawHangman(self.screen, self.numberOfGuesses)

        for button in self.buttons:
            button.draw(self.screen, mouse_pos)

        # Display win streak
        streak = drawLetters(f"Winning Streak : {self.winStreak}")
        self.screen.blit(streak, (SCREENWIDTH - 300, 100))

        # Game over message
        if self.gameOver:
            msg = drawLetters("Click or press key to restart")
            self.screen.blit(
                msg,
                (SCREENWIDTH // 2 - msg.get_width() // 2,
                 SCREENHEIGHT // 2),
            )


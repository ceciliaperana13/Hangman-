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
        self.chosenWord = random.choice(WORDLIST)
        self.guessWord = [" " for _ in self.chosenWord]
        self.numberOfGuesses = 0
        self.gameOver = False
        self.createAlphabet()

    def createAlphabet(self):
        self.buttons = []
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        x, y = 100, 500
        index = 0

        for row in [9, 9, 8]:
            for _ in range(row):
                self.buttons.append(HangmanButton((x, y), alphabet[index]))
                index += 1
                x += 50
            x = 100
            y += 40

    def handleClick(self, pos):
        if self.gameOver:
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

                button.active = False
                break

    def checkGameOver(self):
        if "".join(self.guessWord) == self.chosenWord:
            self.winStreak += 1
            self.gameOver = True
        elif self.numberOfGuesses >= 6:
            self.winStreak = 0
            self.gameOver = True

    def draw(self):
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        drawLetterLines(self.screen, self.chosenWord, self.guessWord)
        drawHangman(self.screen, self.numberOfGuesses)

        for button in self.buttons:
            button.draw(self.screen, mouse_pos)

        streak = drawLetters(f"Winning Streak : {self.winStreak}")
        self.screen.blit(streak, (SCREENWIDTH - 300, 100))

        if self.gameOver:
            msg = drawLetters("Click pour rejouer")
            self.screen.blit(
                msg,
                (SCREENWIDTH // 2 - msg.get_width() // 2,
                 SCREENHEIGHT // 2),
            )

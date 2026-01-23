import random
import pygame
import os

from settings import BLACK, SCREENWIDTH, SCREENHEIGHT
from utils import drawLetterLines, drawHangman, drawLetters, loadWords
from buttons import HangmanButton

# =====================
# INIT
# =====================
pygame.mixer.init()

WORDLIST = loadWords()


class HangmanGame:
    def __init__(self, screen):
        self.screen = screen

        # Game difficulty ("normal" or "hard")
        self.difficulty = "normal"
        # Time limit depending on difficulty
        self.timeLimit = 90
        # LOAD ASSETS (WIN / LOSE)
        self.winImage = pygame.image.load("/win.gif").convert_alpha()
        self.loseImage = pygame.image.load("/loss.gif").convert_alpha()

        self.winSound = pygame.mixer.Sound("/win.mp3")
        self.loseSound = pygame.mixer.Sound("/lose.mp3")

        self.resultPlayed = False

        self.reset()

    def reset(self):
        # Pick a new random word and reset game values
        self.chosenWord = self.chooseWord()
        self.guessWord = [" " for _ in self.chosenWord]
        self.numberOfGuesses = 0
        self.gameOver = False
        self.createAlphabet()

        # Timer start
        self.startTime = pygame.time.get_ticks()

        # Total penalty time in milliseconds
        self.timePenalty = 0

        # Reset sound flag
        self.resultPlayed = False

    def chooseWord(self):
        # Choose word depending on difficulty
        if self.difficulty == "hard":
            longWords = [w for w in WORDLIST if len(w) >= 8]
            return random.choice(longWords)
        return random.choice(WORDLIST)

    def toggleDifficulty(self):
        # Switch between normal and hard mode
        if self.difficulty == "normal":
            self.difficulty = "hard"
            self.timeLimit = 45
        else:
            self.difficulty = "normal"
            self.timeLimit = 90

        # Restart the game when difficulty changes
        self.reset()

    def createAlphabet(self):
        # Create buttons for each letter of the alphabet
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
                    if self.difficulty == "hard":
                        self.timePenalty += 3000

                button.active = False
                break

    def handleKey(self, event):
        if event.key == pygame.K_TAB:
            self.toggleDifficulty()
            return

        if self.gameOver:
            self.reset()
            return

        if event.unicode.isalpha():
            letter = event.unicode.upper()
            for button in self.buttons:
                if button.letter == letter and button.active:
                    if button.letter in self.chosenWord:
                        for i, l in enumerate(self.chosenWord):
                            if l == button.letter:
                                self.guessWord[i] = l
                    else:
                        self.numberOfGuesses += 1
                        if self.difficulty == "hard":
                            self.timePenalty += 3000

                    button.active = False
                    break

    def getTimeLeft(self):
        elapsed = (pygame.time.get_ticks() - self.startTime + self.timePenalty) // 1000
        return max(0, self.timeLimit - elapsed)

    def checkGameOver(self):
        if "".join(self.guessWord) == self.chosenWord:
            self.gameOver = True
        elif self.numberOfGuesses >= 6:
            self.gameOver = True
        elif self.getTimeLeft() <= 0:
            self.gameOver = True
        # PLAY WIN / LOSE SOUND
        if self.gameOver and not self.resultPlayed:
            if "".join(self.guessWord) == self.chosenWord:
                self.winSound.play()
            else:
                self.loseSound.play()
            self.resultPlayed = True

    def draw(self):
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        drawLetterLines(self.screen, self.chosenWord, self.guessWord)
        drawHangman(self.screen, self.numberOfGuesses)

        for button in self.buttons:
            button.draw(self.screen, mouse_pos)

        font = pygame.font.Font(None, 36)

        timer = font.render(f"Time : {self.getTimeLeft()}s", True, (255, 0, 0))
        self.screen.blit(timer, (SCREENWIDTH - timer.get_width() - 20, 20))

        mode_text = font.render(f"Mode : {self.difficulty.upper()}", True, (255, 255, 255))
        self.screen.blit(mode_text, (SCREENWIDTH - mode_text.get_width() - 20, 50))
        # GAME OVER SCREEN
        if self.gameOver:
            if "".join(self.guessWord) == self.chosenWord:
                text = drawLetters("YOU WIN!")
                image = self.winImage
            else:
                text = drawLetters("YOU LOSE!")
                image = self.loseImage

            img_rect = image.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 - 80))
            self.screen.blit(image, img_rect)

            self.screen.blit(
                text,
                (SCREENWIDTH // 2 - text.get_width() // 2,
                 SCREENHEIGHT // 2 + 30),
            )

            restart = drawLetters("Click or press key to restart")
            self.screen.blit(
                restart,
                (SCREENWIDTH // 2 - restart.get_width() // 2,
                 SCREENHEIGHT // 2 + 80),
            )
      



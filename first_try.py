import pygame
import random
import sys

SCREENWIDTH = 800
SCREENHEIGHT = 640
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)

# Init
pygame.init()
GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Hangman")

FONT = pygame.font.SysFont("Comic Sans MS", 22)

# switch words
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


WORDLIST = loadWords()

# hangman buttons
class HangmanButton:
    def __init__(self, position, letter):
        self.letter = letter
        self.image = FONT.render(letter, True, WHITE)
        self.position = position
        self.rect = pygame.Rect(position[0] - 5, position[1], 30, 30)
        self.active = True

    def draw(self, screen, mouse_pos):
        if self.active:
            if self.rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, RED, self.rect)
            else:
                pygame.draw.rect(screen, BLACK, self.rect)

            pygame.draw.rect(screen, WHITE, self.rect, 1)
            screen.blit(self.image, self.position)
        else:
            pygame.draw.rect(screen, GRAY, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 1)
            screen.blit(self.image, self.position)


# Draw
def drawLetters(letter):
    return FONT.render(letter, True, WHITE)


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


# Game
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
                (SCREENWIDTH // 2 - msg.get_width() // 2, SCREENHEIGHT // 2),
            )


# game loop
game = HangmanGame(GAMESCREEN)
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


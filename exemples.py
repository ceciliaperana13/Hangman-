import pygame
import random


#  Hangman Button Objects
class HangmanButton:
    def __init__(self, position, image, letter):
        self.position = position
        self.letter = letter
        self.image = image
        self.imageRect = pygame.Rect(self.position[0] - 5, self.position[1], 30, 30)
        self.active = True


    def mouseHighlight(self, window):
        """highlights the rectangle if the mouse is hovering over this button"""
        pygame.draw.rect(window, (255, 0, 0), [self.imageRect[0], self.imageRect[1], self.imageRect[2], self.imageRect[3]])
        window.blit(self.image, self.position)
        pygame.draw.rect(window, WHITE, [self.imageRect[0], self.imageRect[1], self.imageRect[2], self.imageRect[3]], 1)


    def draw(self, window):
        """Draw the letter to the screen, with a box around it."""
        if self.active:
            window.blit(self.image, self.position)
            pygame.draw.rect(window, WHITE, [self.imageRect[0], self.imageRect[1], self.imageRect[2], self.imageRect[3]], 1)
        else:
            self.mouseHighlight(window)


#  Utility Functions
def openFile():
    """Open and load words from the text file into a simple list"""
    with open('easyWordList.txt', 'r') as file:
        content = file.readlines()
        newList = []
        for itemList in content:
            newList.append(itemList.split(','))

        for wordList in newList:
            for word in wordList:
                if len(word.strip()) >= 3 and len(word.strip()) <= 10:
                    WORDLIST.append(word.strip())


def selectRandomWord():
    """Select a random word from the Word List Generated"""
    return random.choice(WORDLIST)


def drawLetters(letter):
    """Creates the font object for text on the screen."""
    text = pygame.font.SysFont('Comic sans', 22)
    printText = text.render(letter, 1, WHITE)
    return printText


def drawLetterLines(word):
    """Draw lines for each letter in chosen word"""
    wordLengthX = len(word) * (25 + 15)

    startXY = [SCREENWIDTH - 50 - wordLengthX, 350]
    lengthXY = [25, 0]
    spacing = [15, 0]

    for ind, letter in enumerate(word):
        pygame.draw.line(GAMESCREEN, WHITE, (startXY[0], startXY[1]), (startXY[0] + lengthXY[0], startXY[1] + lengthXY[1]), 3)
        GAMESCREEN.blit(drawLetters(guessWord[ind]), (startXY[0]+10, 320))
        startXY[0] = startXY[0] + lengthXY[0] + spacing[0]
        startXY[1] = startXY[1] + lengthXY[1] + spacing[1]


def createAlphabet():
    """Creates the alphabet objects for screen"""
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    xPos = 100
    yPos = 500
    letNum = 0
    for num in [9, 9, 8]:
        for _ in range(num):
            ALPHABETBUTTONS.append(HangmanButton((xPos, yPos), drawLetters(alphabet[letNum]), alphabet[letNum]))
            letNum += 1
            xPos += 50
        xPos = 100
        yPos += 40


def drawAlphabet(itemList):
    """Draws the alhpabet to the screen."""
    for item in itemList:
        item.draw(GAMESCREEN)

    GAMESCREEN.blit(drawLetters(f'Winning Streak : {str(winStreak)}'), (SCREENWIDTH - 300, 100))


def endGame():
    """Handles the end of a round"""
    global chosenWord
    global guessWord
    global numberOfGuesses
    global gameOver
    global winStreak

    if ''.join(guessWord) == chosenWord:
        winStreak += 1

    while gameOver:
        ALPHABETBUTTONS.clear()
        GAMESCREEN.fill((0, 0, 0))
        message = drawLetters('Click to play again')
        GAMESCREEN.blit(message, (SCREENWIDTH // 2 - message.get_width() // 2, SCREENHEIGHT // 2 + 30))

        if ''.join(guessWord) == chosenWord:
            message = drawLetters(f'Congratulations! You guessed {chosenWord}!')
            GAMESCREEN.blit(message, (SCREENWIDTH//2 - message.get_width()//2, SCREENHEIGHT//2))
        elif numberOfGuesses == 6:
            message = drawLetters(f'Sorry, you lost! The word was {chosenWord}!')
            GAMESCREEN.blit(message, (SCREENWIDTH//2 - message.get_width()//2, SCREENHEIGHT//2))
            winStreak = 0

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                numberOfGuesses = 0
                chosenWord = selectRandomWord().upper()
                guessWord = [' ' for letter in chosenWord]
                createAlphabet()
                drawAlphabet(ALPHABETBUTTONS)
                gameOver = False
            if event.type == pygame.QUIT:
                pygame.quit()



#  Hangman Animation Functions
def drawGallows(window):
    """Draw the Gallows"""
    pygame.draw.line(window, WHITE, (100, 400), (275, 400), 3)
    pygame.draw.line(window, WHITE, (125, 400), (125, 50), 3)
    pygame.draw.line(window, WHITE, (125, 50), (275, 50), 3)
    pygame.draw.line(window, WHITE, (125, 100), (175, 50), 3)
    pygame.draw.line(window, WHITE, (275, 50), (275, 125), 3)


def drawHead(window):
    """Draws the Hanged man's Head"""
    pygame.draw.circle(window, WHITE, (275, 150), (25), 3)


def drawBody(window):
    """Draws the Hanged Man's Body"""
    pygame.draw.line(window, WHITE, (275, 175), (275, 225), 3)


def drawLeftArm(window):
    """Draws the Hanged Man's Left Arm"""
    pygame.draw.line(window, WHITE, (275, 185), (245, 215), 3)


def drawRightArm(window):
    """Draws the Hanged Man's Right Arm"""
    pygame.draw.line(window, WHITE, (275, 185), (305, 215), 3)


def drawLeftLeg(window):
    """Draws the Hanged Man's Left Leg"""
    pygame.draw.line(window, WHITE, (275, 225), (250, 250), 3)
    pygame.draw.line(window, WHITE, (250, 250), (250, 275), 3)
    pygame.draw.line(window, WHITE, (250, 275), (240, 275), 3)


def drawRightLeg(window):
    """Draws the Hanged Man's Left Leg"""
    pygame.draw.line(window, WHITE, (275, 225), (300, 250), 3)
    pygame.draw.line(window, WHITE, (300, 250), (300, 275), 3)
    pygame.draw.line(window, WHITE, (300, 275), (310, 275), 3)


def drawHangman(window, numberGuesses):
    """Draws the various stages of the Hanged Man"""
    if numberGuesses >= 0:
        drawGallows(window)
    if numberGuesses >= 1:
        drawHead(window)
    if numberGuesses >= 2:
        drawBody(window)
    if numberGuesses >= 3:
        drawLeftArm(window)
    if numberGuesses >= 4:
        drawRightArm(window)
    if numberGuesses >= 5:
        drawLeftLeg(window)
    if numberGuesses >= 6:
        drawRightLeg(window)


#  Hangman Words list
WORDLIST = []
openFile()
ALPHABETBUTTONS = []


#  initialization of the pygame module
pygame.init()


#  Game settings
SCREENWIDTH = 800
SCREENHEIGHT = 640
WHITE = (255, 255, 255)

#  Display Initialization
GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Hang Man')

#  Game Variables and load functions
numberOfGuesses = 0
chosenWord = selectRandomWord().upper()
guessWord = [' ' for letter in chosenWord]
createAlphabet()
print(chosenWord)
print(guessWord)
mouseClicked = False
gameOver = False
winStreak = 0


#  Main game loop.
RUN = True
while RUN:

    #  Fill the screen with Black Color
    GAMESCREEN.fill((0, 0, 0))

    #  Pygame event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseClicked = True

            for item in ALPHABETBUTTONS:
                if item.imageRect.collidepoint(event.pos):
                    if item.letter in chosenWord:
                        for ind, let in enumerate(chosenWord):
                            if item.letter == let:
                                guessWord[ind] = item.letter
                    elif item.letter not in chosenWord and item.active:
                        numberOfGuesses += 1
                    item.active = False

        elif event.type == pygame.MOUSEBUTTONUP:
            mouseclicked = False

    drawLetterLines(chosenWord)
    drawAlphabet(ALPHABETBUTTONS)
    drawHangman(GAMESCREEN, numberOfGuesses)

    #  Detect Mouse Collision with buttons
    for ALPHABETBUTTON in ALPHABETBUTTONS:
        if ALPHABETBUTTON.imageRect.collidepoint(pygame.mouse.get_pos()):
            ALPHABETBUTTON.mouseHighlight(GAMESCREEN)

    #  Update the display screen
    pygame.display.update()

    if ''.join(guessWord) == chosenWord or numberOfGuesses == 6:
        gameOver = True
        endGame()


pygame.quit()
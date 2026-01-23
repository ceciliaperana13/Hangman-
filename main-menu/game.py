import random
import pygame
from settings import BLACK, SCREENWIDTH, SCREENHEIGHT
from utils import drawLetterLines, drawHangman, drawLetters, loadWords
from buttons import HangmanButton
from score import add_score  # Import de la fonction add_score

WORDLIST = loadWords()

class HangmanGame:
    def __init__(self, screen):
        self.screen = screen

        
        self.difficulty = "normal"

        
        self.timeLimit = 90

        # Player name
        self.player_name = "Player"
        
        # Flag to track if score was already saved
        self.score_saved = False

        self.reset()

    def set_player_name(self, name):
        """Définit le nom du joueur"""
        self.player_name = name if name.strip() else "Player"

    def reset(self):
        # Pick a new random word and reset game values
        self.chosenWord = self.chooseWord()
        self.guessWord = [" " for _ in self.chosenWord]
        self.numberOfGuesses = 0
        self.gameOver = False
        self.score_saved = False  # Reset du flag de sauvegarde
        self.createAlphabet()

        # Timer start
        self.startTime = pygame.time.get_ticks()

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

                    # Time penalty in hard mode
                    if self.difficulty == "hard":
                        self.startTime += 3000

                # Deactivate the button
                button.active = False
                break

    def handleKey(self, event):
        # Handle key press from keyboard

        # Change difficulty with TAB key
        if event.key == pygame.K_TAB:
            self.toggleDifficulty()
            return

        if self.gameOver:
            # Restart game if over
            self.reset()
            return

        # Only accept letters A-Z
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

                        # Time penalty in hard mode
                        if self.difficulty == "hard":
                            self.startTime += 3000

                    # Deactivate the button
                    button.active = False
                    break

    def getTimeLeft(self):
        # Calculate remaining time
        elapsed = (pygame.time.get_ticks() - self.startTime) // 1000
        return max(0, self.timeLimit - elapsed)

    def checkGameOver(self):
        # Check if the player has won or lost
        won = "".join(self.guessWord) == self.chosenWord
        lost_hangman = self.numberOfGuesses >= 6
        lost_time = self.getTimeLeft() <= 0

        if won and not self.score_saved:
            # VICTOIRE : Sauvegarder le score
            self.gameOver = True
            max_attempts = 6
            add_score(
                player_name=self.player_name,
                word=self.chosenWord,
                result="WIN",
                attempts=self.numberOfGuesses,
                max_attempts=max_attempts
            )
            self.score_saved = True
            print(f" VICTOIRE ! Score enregistré pour {self.player_name}")

        elif (lost_hangman or lost_time) and not self.score_saved:
            # DÉFAITE : Sauvegarder le score
            self.gameOver = True
            max_attempts = 6
            add_score(
                player_name=self.player_name,
                word=self.chosenWord,
                result="LOSE",
                attempts=self.numberOfGuesses,
                max_attempts=max_attempts
            )
            self.score_saved = True
            print(f" DÉFAITE ! Score enregistré pour {self.player_name}")

    def draw(self):
        # Draw everything on the screen
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        drawLetterLines(self.screen, self.chosenWord, self.guessWord)
        drawHangman(self.screen, self.numberOfGuesses)

        for button in self.buttons:
            button.draw(self.screen, mouse_pos)

        # Draw timer on the right
        font = pygame.font.Font(None, 36)
        timer = font.render(f"Time : {self.getTimeLeft()}s", True, (255, 0, 0))
        self.screen.blit(timer, (SCREENWIDTH - timer.get_width() - 20, 20))

        # Draw current difficulty on the right
        mode_text = font.render(f"Mode : {self.difficulty.upper()}", True, (255, 255, 255))
        self.screen.blit(mode_text, (SCREENWIDTH - mode_text.get_width() - 20, 50))

        # Draw player name
        player_text = font.render(f"Player : {self.player_name}", True, (255, 255, 255))
        self.screen.blit(player_text, (20, 20))

        # Game over message
        if self.gameOver:
            # Afficher si victoire ou défaite
            if "".join(self.guessWord) == self.chosenWord:
                result_msg = drawLetters("YOU WIN!")
                result_color = (0, 255, 0)  # Vert
            else:
                result_msg = drawLetters("YOU LOSE!")
                result_color = (255, 0, 0)  # Rouge
                # Afficher le mot correct
                word_msg = drawLetters(f"Word was: {self.chosenWord}")
                self.screen.blit(
                    word_msg,
                    (SCREENWIDTH // 2 - word_msg.get_width() // 2,
                     SCREENHEIGHT // 2 - 40),
                )
            
            # Afficher résultat en couleur
            result_surface = pygame.font.Font(None, 72).render(
                "YOU WIN!" if "".join(self.guessWord) == self.chosenWord else "YOU LOSE!",
                True, result_color
            )
            self.screen.blit(
                result_surface,
                (SCREENWIDTH // 2 - result_surface.get_width() // 2,
                 SCREENHEIGHT // 2 - 80),
            )

            # Message pour redémarrer
            msg = drawLetters("Click or press key to restart")
            self.screen.blit(
                msg,
                (SCREENWIDTH // 2 - msg.get_width() // 2,
                 SCREENHEIGHT // 2 + 40),
            )
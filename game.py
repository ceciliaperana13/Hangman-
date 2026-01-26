import random
import pygame
from settings import BLACK, SCREENWIDTH, SCREENHEIGHT
from utils import draw_letter_lines, draw_hangman, draw_letters, load_words
from buttons import HangmanButton
from score import add_score  # Import the add_score function

WORDLIST = load_words()


class HangmanGame:
    def __init__(self, screen):
        self.screen = screen

        # Game difficulty ("normal" or "hard")
        self.difficulty = "normal"

        # Time limit in seconds
        self.timeLimit = 90

        # Player name
        self.player_name = "Player"
        
        # Flag to track if the score has already been saved
        self.score_saved = False

        self.reset()

    def set_player_name(self, name):
        """Set the player's name"""
        self.player_name = name if name.strip() else "Player"

    def reset(self):
        # Pick a new random word and reset all game values
        self.chosenWord = self.chooseWord()
        self.guessWord = [" " for _ in self.chosenWord]
        self.numberOfGuesses = 0
        self.gameOver = False
        self.score_saved = False  # Reset score saved flag
        self.createAlphabet()

        # Start the timer
        self.startTime = pygame.time.get_ticks()

    def chooseWord(self):
        # Choose a word depending on the difficulty
        if self.difficulty == "hard":
            longWords = [w for w in WORDLIST if len(w) >= 8]
            return random.choice(longWords)
        return random.choice(WORDLIST)

    def toggleDifficulty(self):
        # Switch between normal and hard mode
        if self.difficulty == "normal":
            self.difficulty = "hard"
            self.timeLimit = 80
        else:
            self.difficulty = "normal"
            self.timeLimit = 90

        # Restart the game when the difficulty changes
        self.reset()

    def createAlphabet(self):
        # Create buttons for each letter of the alphabet
        self.buttons = []
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        x, y = 100, 500
        index = 0

        # Layout letters in rows
        for row in [9, 9, 8]:
            for _ in range(row):
                self.buttons.append(HangmanButton((x, y), alphabet[index]))
                index += 1
                x += 50
            x = 100
            y += 40

    def handleClick(self, pos):
        # Handle mouse click on letter buttons
        if self.gameOver:
            # Restart the game if it is over
            self.reset()
            return

        for button in self.buttons:
            if button.active and button.rect.collidepoint(pos):
                if button.letter in self.chosenWord:
                    # Reveal all matching letters
                    for i, letter in enumerate(self.chosenWord):
                        if letter == button.letter:
                            self.guessWord[i] = letter
                else:
                    # Wrong guess
                    self.numberOfGuesses += 1

                    # Time penalty in hard mode
                    if self.difficulty == "hard":
                        self.startTime += 3000

                # Deactivate the button after use
                button.active = False
                break

    def handleKey(self, event):
        # Handle keyboard input

        # Change difficulty using TAB key
        if event.key == pygame.K_TAB:
            self.toggleDifficulty()
            return

        if self.gameOver:
            # Restart the game if it is over
            self.reset()
            return

        # Accept only alphabetical characters
        if event.unicode.isalpha():
            letter = event.unicode.upper()
            for button in self.buttons:
                if button.letter == letter and button.active:
                    if button.letter in self.chosenWord:
                        # Reveal matching letters
                        for i, l in enumerate(self.chosenWord):
                            if l == button.letter:
                                self.guessWord[i] = l
                    else:
                        # Wrong guess
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
            # WIN: save the score
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
            print(f"WIN! Score saved for {self.player_name}")

        elif (lost_hangman or lost_time) and not self.score_saved:
            # LOSS: save the score
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
            print(f"LOSS! Score saved for {self.player_name}")

    def draw(self):
        # Draw everything on the screen
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        draw_letter_lines(self.screen, self.chosenWord, self.guessWord)
        draw_hangman(self.screen, self.numberOfGuesses)

        # Draw letter buttons
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)

        # Draw timer (top right)
        font = pygame.font.Font(None, 36)
        timer = font.render(f"Time : {self.getTimeLeft()}s", True, (255, 0, 0))
        self.screen.blit(timer, (SCREENWIDTH - timer.get_width() - 20, 20))

        # Draw current difficulty (top right)
        mode_text = font.render(
            f"Mode : {self.difficulty.upper()}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(mode_text, (SCREENWIDTH - mode_text.get_width() - 20, 50))

        # Draw player name (top left)
        player_text = font.render(
            f"Player : {self.player_name}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(player_text, (20, 20))

        # Game over screen
        if self.gameOver:
            # Display win or loss message
            if "".join(self.guessWord) == self.chosenWord:
                result_color = (0, 255, 0)  # Green
            else:
                result_color = (255, 0, 0)  # Red

                # Display the correct word
                word_msg = draw_letters(f"Word was: {self.chosenWord}")
                self.screen.blit(
                    word_msg,
                    (SCREENWIDTH // 2 - word_msg.get_width() // 2,
                     SCREENHEIGHT // 2 - 40),
                )

            # Display result text
            result_surface = pygame.font.Font(None, 72).render(
                "YOU WIN!" if "".join(self.guessWord) == self.chosenWord else "YOU LOSE!",
                True,
                result_color
            )
            self.screen.blit(
                result_surface,
                (SCREENWIDTH // 2 - result_surface.get_width() // 2,
                 SCREENHEIGHT // 2 - 80),
            )

            # Restart instruction
            msg = draw_letters("Click or press key to restart")
            self.screen.blit(
                msg,
                (SCREENWIDTH // 2 - msg.get_width() // 2,
                 SCREENHEIGHT // 2 + 40),
            )



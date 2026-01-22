import pygame
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Guess - History")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

font = pygame.font.Font(None, 40)

words = ["KIT"]

history = []

try:
    open("history.txt", "r").close()
except:
    open("history.txt", "w").close()

def load_history():
    with open("history.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

history = load_history()

def add_history(result):
    history.append(result)
    with open("history.txt", "a") as f:
        f.write(result + "\n")

MAX_ERRORS = 6

def new_game():
    return {
        "word": random.choice(words),
        "found_letters": set(),
        "wrong_letters": set(),
        "errors": 0
    }

game = new_game()

def draw_text(text, x, y, color=WHITE):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def draw_word():
    display = ""
    for letter in game["word"]:
        if letter in game["found_letters"]:
            display += letter + " "
        else:
            display += "_ "
    draw_text(display, 250, 300)

def check_win():
    return all(l in game["found_letters"] for l in game["word"])

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    screen.fill(BLACK)

    draw_word()
    draw_text(f"Errors : {game['errors']} / {MAX_ERRORS}", 20, 20)

    y = 450
    draw_text("History:", 20, 400)
    for result in history[-5:]:
        color = GREEN if result == "WIN" else RED
        draw_text(result, 20, y, color)
        y += 30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            letter = event.unicode.upper()

            if len(letter) == 1 and "A" <= letter <= "Z":
                if letter in game["word"]:
                    game["found_letters"].add(letter)
                else:
                    if letter not in game["wrong_letters"]:
                        game["wrong_letters"].add(letter)
                        game["errors"] += 1

    if check_win():
        win_sound.play()
        draw_text("YOU WIN!", 300, 350, GREEN)
        pygame.display.flip()
        pygame.time.delay(1500)
        add_history("WIN")
        game = new_game()

    if game["errors"] >= MAX_ERRORS:
        lose_sound.play()
        draw_text(f"YOU LOSE! Word: {game['word']}", 230, 350, RED)
        pygame.display.flip()
        pygame.time.delay(1500)
        add_history("LOSE")
        game = new_game()

    pygame.display.flip()

pygame.quit()

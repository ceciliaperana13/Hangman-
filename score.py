import pygame
import random
import datetime

pygame.init()

HISTORY_FILE = "score.txt"

game_history = []

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Score History")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Font
font = pygame.font.SysFont(None, 30)

# Button class
class Button:
    def __init__(self, x, y, w, h, text, color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        txt = font.render(self.text, True, self.text_color)
        txt_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Buttons
add_button = Button(50, HEIGHT - 60, 200, 40, "Add Game", BLUE)
quit_button = Button(350, HEIGHT - 60, 200, 40, "Quit", RED)

# -------------------------------

def read_history():
    """Read history from HISTORY_FILE and return a list of dicts."""
    history = []
    try:
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    date, win, loss = line.split(";")
                    history.append({
                        "date": date,
                        "win": int(win),
                        "loss": int(loss)
                    })
    except FileNotFoundError:
       
        pass
    return history

def add_history(win, loss):
    """Add a new game result to file and list."""
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    game_history.append({"date": date, "win": win, "loss": loss})
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{date};{win};{loss}\n")

game_history = read_history()

# -------------------------------
def add_game():
    win = random.randint(0, 1)
    loss = 1 - win
    add_history(win, loss)

# -------------------------------
running = True
while running:
    screen.fill(WHITE)

    pygame.draw.rect(screen, GRAY, (50, 50, 500, 250))

    headers = ["Date", "Win", "Loss"]
    for i, header in enumerate(headers):
        txt = font.render(header, True, BLACK)
        screen.blit(txt, (60 + i*150, 60))

    for j, entry in enumerate(game_history[-8:]):
        y = 90 + j*30
        screen.blit(font.render(entry["date"], True, BLACK), (60, y))
        screen.blit(font.render(str(entry["win"]), True, GREEN), (210, y))
        screen.blit(font.render(str(entry["loss"]), True, RED), (360, y))

    add_button.draw(screen)
    quit_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if add_button.is_clicked(event.pos):
                add_game()
            elif quit_button.is_clicked(event.pos):
                running = False

    pygame.display.flip()

pygame.quit()

import pygame
import random
import datetime

pygame.init()

historique_parties = []

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Historique des scores")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)


font = pygame.font.SysFont(None, 30)


historique = []


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

add_button = Button(50, HEIGHT - 60, 200, 40, "Ajouter une partie", BLUE)
quit_button = Button(350, HEIGHT - 60, 200, 40, "Quitter", RED)


def ajouter_partie():
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    victoire = random.randint(0, 1)  # 0 ou 1
    defaite = 1 - victoire
    historique.append({"date": date, "victoire": victoire, "defaite": defaite})


running = True
while running:
    screen.fill(WHITE)


    pygame.draw.rect(screen, GRAY, (50, 50, 500, 250))

    headers = ["Date", "Victoire", "Défaite"]
    for i, header in enumerate(headers):
        txt = font.render(header, True, BLACK)
        screen.blit(txt, (60 + i*150, 60))


    for j, entry in enumerate(historique[-8:]): 
        screen.blit(font.render(entry["date"], True, BLACK), (60, 90 + j*30))
        screen.blit(font.render(str(entry["victoire"]), True, GREEN), (210, 90 + j*30))
        screen.blit(font.render(str(entry["defaite"]), True, RED), (360, 90 + j*30))


    add_button.draw(screen)
    quit_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if add_button.is_clicked(event.pos):
                ajouter_partie()
            elif quit_button.is_clicked(event.pos):
                running = False

    pygame.display.flip()

pygame.quit()

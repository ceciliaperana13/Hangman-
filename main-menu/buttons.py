import pygame
from settings import FONT, WHITE, RED, BLACK, GRAY

class HangmanButton:
    def __init__(self, position, letter):
        self.letter = letter
        self.image = FONT.render(letter, True, WHITE)
        self.position = position
        self.rect = pygame.Rect(position[0] - 5, position[1], 30, 30)
        self.active = True

    def draw(self, screen, mouse_pos):
        if self.active:
            color = RED if self.rect.collidepoint(mouse_pos) else BLACK
            pygame.draw.rect(screen, color, self.rect)
        else:
            pygame.draw.rect(screen, GRAY, self.rect)

        pygame.draw.rect(screen, WHITE, self.rect, 1)
        screen.blit(self.image, self.position)
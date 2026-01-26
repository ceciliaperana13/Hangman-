import pygame
from settings import FONT, WHITE, RED, BLACK, GRAY


class HangmanButton:
    def __init__(self, position, letter):
        # Letter associated with this button
        self.letter = letter
        
        # Render the letter using the predefined font
        self.image = FONT.render(letter, True, WHITE)
        
        # Position where the letter will be drawn
        self.position = position
        
        # Rectangle defining the button area (for collision detection)
        self.rect = pygame.Rect(position[0] - 5, position[1], 30, 30)
        
        # Indicates whether the button is active (clickable)
        self.active = True

    def draw(self, screen, mouse_pos):
        # Draw the button depending on its active state
        if self.active:
            # Change color when the mouse is hovering over the button
            color = RED if self.rect.collidepoint(mouse_pos) else BLACK
            pygame.draw.rect(screen, color, self.rect)
        else:
            # Draw disabled button
            pygame.draw.rect(screen, GRAY, self.rect)

        # Draw the button border
        pygame.draw.rect(screen, WHITE, self.rect, 1)
        
        # Draw the letter on top of the button
        screen.blit(self.image, self.position)

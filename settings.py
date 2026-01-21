import pygame

SCREENWIDTH = 800
SCREENHEIGHT = 640

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)

pygame.font.init()
FONT = pygame.font.SysFont("Comic Sans MS", 22)

# colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GRAY_LIGTH = (200, 200, 200)
GRAY_DARK = (60, 60, 60)
BROWN = (139, 69, 19)
BROWN_DARK = (101, 67, 33)
BLUE = (70, 130, 180)
BLUE_LIGTH = (100, 160, 210)
GREEN = (46, 125, 50)


class button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hovers = False
    
    def draw(self, surface):
        color = BLUE_LIGTH if self.hovers else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=10)
        
        police = pygame.font.Font(None, 40)
        text = police.render(self.text, True, WHITE)
        rect_text = text.get_rect(center=self.rect.center)
        surface.blit(text, rect_text)
    
    def check_hover(self, pos):
        self.hovers = self.rect.collidepoint(pos)
    
    def for_clic(self, pos):
        return self.rect.collidepoint(pos)


class cursor:
    def __init__(self, x, y, width, name, initial_value):
        self.x = x
        self.y = y
        self.width = width
        self.name = name
        self.value = initial_value
        self.movement = False
        self.rect_button = pygame.Rect(0, 0, 20, 30)
        self.to_update()
    
    def to_update(self):
        self.value = max(0, min(self.value, 100))
        pos_x = self.x + int((self.value / 100) * self.width)
        self.rect_button.center = (pos_x, self.y)
    
    def draw(self, surface):
        police = pygame.font.Font(None, 32)
        text = police.render(self.name, True, WHITE)
        surface.blit(text, (self.x - 150, self.y - 10))
        
        value_text = police.render(f"{self.value}%", True, WHITE)
        surface.blit(value_text, (self.x + self.width + 20, self.y - 10))
        
        pygame.draw.line(surface, GRAY, (self.x, self.y), (self.x + self.width, self.y), 4)
        pygame.draw.line(surface, BLUE, (self.x, self.y), (self.rect_button.centerx, self.y), 6)
        
        pygame.draw.rect(surface, BLUE_LIGTH, self.rect_button, border_radius=5)
        pygame.draw.rect(surface, WHITE, self.rect_button, 2, border_radius=5)
    
    def manage_clic(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_button.collidepoint(pos):
                self.movement = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.movement = False
        elif event.type == pygame.MOUSEMOTION and self.movement:
            new_pos = max(self.x, min(pos[0], self.x + self.width))
            self.value = int(((new_pos - self.x) / self.width) * 100)
            self.to_update()


class buttonSwitch:
    def __init__(self, x, y, name, active):
        self.x = x
        self.y = y
        self.name = name
        self.active = active
        self.rect = pygame.Rect(x, y, 60, 30)
    
    def draw(self, surface):
        police = pygame.font.Font(None, 32)
        text = police.render(self.name, True, WHITE)
        surface.blit(text, (self.x - 150, self.y))
        
        color = GREEN if self.active else GRAY_DARK
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=15)
        
        circle_x = self.x + 45 if self.active else self.x + 15
        pygame.draw.circle(surface, WHITE, (circle_x, self.y + 15), 12)
    
    def clic(self, pos):
        if self.rect.collidepoint(pos):
            self.active = not self.active
            return True
        return False


class Selector:
    def __init__(self, x, y, name, options, option_active):
        self.x = x
        self.y = y
        self.name = name
        self.options = options
        self.index = options.index(option_active)
        self.rect = pygame.Rect(x, y, 200, 40)
        self.hovers = False
    
    def draw(self, surface):
        police = pygame.font.Font(None, 32)
        text = police.render(self.name, True, WHITE)
        surface.blit(text, (self.x - 150, self.y + 5))
        
        color = BLUE_LIGTH if self.hovers else BLUE
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        
        police_option = pygame.font.Font(None, 28)
        option_text = police_option.render(self.options[self.index], True, WHITE)
        rect_text = option_text.get_rect(center=self.rect.center)
        surface.blit(option_text, rect_text)
        
        police_arrow = pygame.font.Font(None, 28)
        surface.blit(police_arrow.render("<", True, WHITE), (self.rect.x + 10, self.rect.centery - 10))
        surface.blit(police_arrow.render(">", True, WHITE), (self.rect.right - 25, self.rect.centery - 10))
    
    def check_hover(self, pos):
        self.hovers = self.rect.collidepoint(pos)
    
    def clic(self, pos):
        if self.rect.collidepoint(pos):
            if pos[0] < self.rect.centerx:
                self.index = (self.index - 1) % len(self.options)
            else:
                self.index = (self.index + 1) % len(self.options)
            return True
        return False
    
    def get_value(self):
        return self.options[self.index]


def draw_potence(surface, x, y, swing):
    pygame.draw.rect(surface, BROWN, (x, y + 190, 40, 25))
    pygame.draw.rect(surface, BROWN_DARK, (x, y + 190, 40, 25), 2)
    pygame.draw.rect(surface, BROWN, (x + 110, y + 190, 40, 25))
    pygame.draw.rect(surface, BROWN_DARK, (x + 110, y + 190, 40, 25), 2)
    
    pygame.draw.rect(surface, BROWN, (x + 15, y, 15, 195))
    pygame.draw.rect(surface, BROWN_DARK, (x + 15, y, 15, 195), 2)
    pygame.draw.rect(surface, BROWN, (x + 120, y, 15, 195))
    pygame.draw.rect(surface, BROWN_DARK, (x + 120, y, 15, 195), 2)
    
    pygame.draw.rect(surface, BROWN, (x + 30, y, 100, 15))
    pygame.draw.rect(surface, BROWN_DARK, (x + 30, y, 100, 15), 2)
    
    pygame.draw.polygon(surface, BROWN_DARK, [(x + 30, y + 15), (x + 30, y), (x + 60, y)])
    
    corde_x = x + 90 + int(swing * 10)
    pygame.draw.line(surface, (218, 165, 32), (x + 90, y + 15), (corde_x, y + 45), 3)
    
    pygame.draw.circle(surface, WHITE, (corde_x, y + 60), 15, 3)
    pygame.draw.line(surface, WHITE, (corde_x, y + 75), (corde_x, y + 125), 3)
    pygame.draw.line(surface, WHITE, (corde_x, y + 85), (corde_x - 20, y + 95), 3)
    pygame.draw.line(surface, WHITE, (corde_x, y + 85), (corde_x + 20, y + 95), 3)
    pygame.draw.line(surface, WHITE, (corde_x, y + 125), (corde_x - 15, y + 150), 3)
    pygame.draw.line(surface, WHITE, (corde_x, y + 125), (corde_x + 15, y + 150), 3)
    
    pygame.draw.rect(surface, GRAY, (corde_x - 30, y + 155, 60, 8))
    pygame.draw.rect(surface, GRAY_LIGTH, (corde_x - 30, y + 155, 60, 8), 2)


def draw_title(surface, text, y, color):
    police = pygame.font.Font(None, 64)
    tittle = police.render(text, True, color)
    rect = tittle.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(tittle, rect)

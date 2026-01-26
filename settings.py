import pygame

SCREENWIDTH = 800
SCREENHEIGHT = 640


pygame.font.init()
FONT = pygame.font.SysFont("Comic Sans MS", 22)

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GRAY_LIGTH = (200, 200, 200)
GRAY_DARK = (60, 60, 60)
BROWN = (139, 69, 19)
BROWN_DARK = (101, 67, 33)
BLUE = (70, 130, 180)
BLUE_LIGTH = (100, 160, 210)
GREEN = (46, 125, 50)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class button:
    def __init__(self, x, y, width, height, text, color):
        # Button rectangle
        self.rect = pygame.Rect(x, y, width, height)
        
        # Button label
        self.text = text
        
        # Default button color
        self.color = color
        
        # Hover state
        self.hovers = False
    
    def draw(self, surface):
        # Change color when hovered
        color = BLUE_LIGTH if self.hovers else self.color
        
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=10)
        
        # Draw button text
        font = pygame.font.Font(None, 40)
        text = font.render(self.text, True, WHITE)
        rect_text = text.get_rect(center=self.rect.center)
        surface.blit(text, rect_text)
    
    def check_hover(self, pos):
        # Check if the mouse is hovering over the button
        self.hovers = self.rect.collidepoint(pos)
    
    def for_clic(self, pos):
        # Check if the button is clicked
        return self.rect.collidepoint(pos)


class cursor:
    def __init__(self, x, y, width, name, initial_value):
        # Slider position and size
        self.x = x
        self.y = y
        self.width = width
        
        # Slider label
        self.name = name
        
        # Current value (0–100)
        self.value = initial_value
        
        # Drag state
        self.movement = False
        
        # Slider handle rectangle
        self.rect_button = pygame.Rect(0, 0, 20, 30)
        self.to_update()
    
    def to_update(self):
        # Clamp value between 0 and 100 and update handle position
        self.value = max(0, min(self.value, 100))
        pos_x = self.x + int((self.value / 100) * self.width)
        self.rect_button.center = (pos_x, self.y)
    
    def draw(self, surface):
        font = pygame.font.Font(None, 32)
        
        # Slider label
        text = font.render(self.name, True, WHITE)
        surface.blit(text, (self.x - 150, self.y - 10))
        
        # Slider value
        value_text = font.render(f"{self.value}%", True, WHITE)
        surface.blit(value_text, (self.x + self.width + 20, self.y - 10))
        
        # Slider line
        pygame.draw.line(surface, GRAY, (self.x, self.y), (self.x + self.width, self.y), 4)
        pygame.draw.line(surface, BLUE, (self.x, self.y), (self.rect_button.centerx, self.y), 6)
        
        # Slider handle
        pygame.draw.rect(surface, BLUE_LIGTH, self.rect_button, border_radius=5)
        pygame.draw.rect(surface, WHITE, self.rect_button, 2, border_radius=5)
    
    def manage_clic(self, event, pos):
        # Handle slider interaction
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
        # Switch position and label
        self.x = x
        self.y = y
        self.name = name
        
        # Switch state
        self.active = active
        
        # Switch rectangle
        self.rect = pygame.Rect(x, y, 60, 30)
    
    def draw(self, surface):
        font = pygame.font.Font(None, 32)
        
        # Switch label
        text = font.render(self.name, True, WHITE)
        surface.blit(text, (self.x - 150, self.y))
        
        # Switch background
        color = GREEN if self.active else GRAY_DARK
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=15)
        
        # Switch knob
        circle_x = self.x + 45 if self.active else self.x + 15
        pygame.draw.circle(surface, WHITE, (circle_x, self.y + 15), 12)
    
    def clic(self, pos):
        # Toggle switch on click
        if self.rect.collidepoint(pos):
            self.active = not self.active
            return True
        return False


class Selector:
    def __init__(self, x, y, name, options, option_active):
        # Selector position and label
        self.x = x
        self.y = y
        self.name = name
        
        # Available options
        self.options = options
        
        # Current option index
        self.index = options.index(option_active)
        
        # Selector rectangle
        self.rect = pygame.Rect(x, y, 200, 40)
        
        # Hover state
        self.hovers = False
    
    def draw(self, surface):
        font = pygame.font.Font(None, 32)
        
        # Selector label
        text = font.render(self.name, True, WHITE)
        surface.blit(text, (self.x - 150, self.y + 5))
        
        # Selector background
        color = BLUE_LIGTH if self.hovers else BLUE
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        
        # Current option text
        font_option = pygame.font.Font(None, 28)
        option_text = font_option.render(self.options[self.index], True, WHITE)
        rect_text = option_text.get_rect(center=self.rect.center)
        surface.blit(option_text, rect_text)
        
        # Arrow indicators
        font_arrow = pygame.font.Font(None, 28)
        surface.blit(font_arrow.render("<", True, WHITE), (self.rect.x + 10, self.rect.centery - 10))
        surface.blit(font_arrow.render(">", True, WHITE), (self.rect.right - 25, self.rect.centery - 10))
    
    def check_hover(self, pos):
        # Check hover state
        self.hovers = self.rect.collidepoint(pos)
    
    def clic(self, pos):
        # Change selected option
        if self.rect.collidepoint(pos):
            if pos[0] < self.rect.centerx:
                self.index = (self.index - 1) % len(self.options)
            else:
                self.index = (self.index + 1) % len(self.options)
            return True
        return False
    
    def get_value(self):
        # Return the selected option
        return self.options[self.index]


def draw_potence(surface, x, y, swing):
    """Draw the gallows and the hangman with a swing animation"""
    
    # Base
    pygame.draw.rect(surface, BROWN, (x, y + 190, 40, 25))
    pygame.draw.rect(surface, BROWN_DARK, (x, y + 190, 40, 25), 2)
    pygame.draw.rect(surface, BROWN, (x + 110, y + 190, 40, 25))
    pygame.draw.rect(surface, BROWN_DARK, (x + 110, y + 190, 40, 25), 2)
    
    # Vertical poles
    pygame.draw.rect(surface, BROWN, (x + 15, y, 15, 195))
    pygame.draw.rect(surface, BROWN_DARK, (x + 15, y, 15, 195), 2)
    pygame.draw.rect(surface, BROWN, (x + 120, y, 15, 195))
    pygame.draw.rect(surface, BROWN_DARK, (x + 120, y, 15, 195), 2)
    
    # Top beam
    pygame.draw.rect(surface, BROWN, (x + 30, y, 100, 15))
    pygame.draw.rect(surface, BROWN_DARK, (x + 30, y, 100, 15), 2)
    
    # Support triangle
    pygame.draw.polygon(
        surface,
        BROWN_DARK,
        [(x + 30, y + 15), (x + 30, y), (x + 60, y)]
    )
    
    # Rope with swing effect
    rope_x = x + 90 + int(swing * 10)
    pygame.draw.line(surface, (218, 165, 32), (x + 90, y + 15), (rope_x, y + 45), 3)
    
    # Hangman body
    pygame.draw.circle(surface, WHITE, (rope_x, y + 60), 15, 3)
    pygame.draw.line(surface, WHITE, (rope_x, y + 75), (rope_x, y + 125), 3)
    pygame.draw.line(surface, WHITE, (rope_x, y + 85), (rope_x - 20, y + 95), 3)
    pygame.draw.line(surface, WHITE, (rope_x, y + 85), (rope_x + 20, y + 95), 3)
    pygame.draw.line(surface, WHITE, (rope_x, y + 125), (rope_x - 15, y + 150), 3)
    pygame.draw.line(surface, WHITE, (rope_x, y + 125), (rope_x + 15, y + 150), 3)
    
    # Ground platform
    pygame.draw.rect(surface, GRAY, (rope_x - 30, y + 155, 60, 8))
    pygame.draw.rect(surface, GRAY_LIGTH, (rope_x - 30, y + 155, 60, 8), 2)


def draw_title(surface, text, y, color):
    """Draw a centered title at the given Y position"""
    font = pygame.font.Font(None, 64)
    title = font.render(text, True, color)
    rect = title.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(title, rect)

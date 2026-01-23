import pygame
from settings import button, draw_title


WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (70, 130, 180)
GREEN = (46, 125, 50)
RED = (220, 53, 69)
FOND = (30, 30, 50)

FPS = 60


def save_words(text, filename="easyWordList.txt"):
    """Ajoute un ou plusieurs mots séparés par des virgules"""
    try:
        # Lire les mots existants
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing = [line.strip().lower() for line in f]
        except:
            existing = []
        
        # Séparer par virgules
        words = [w.strip() for w in text.split(',') if w.strip()]
        
        if not words:
            return False, "Enter a word!"
        
        # Ajouter les nouveaux
        added = []
        for word in words:
            if word.lower() not in existing:
                added.append(word)
                existing.append(word.lower())
        
        if added:
            with open(filename, 'a', encoding='utf-8') as f:
                for word in added:
                    f.write(word + '\n')
            return True, f"{len(added)} word(s) added!"
        else:
            return False, "Word(s) already exist!"
    except:
        return False, "Error!"


def add_word(screen, clock):
    """Page simple pour ajouter des mots"""
    w, h = screen.get_width(), screen.get_height()
    
    # Boutons
    btn_add = button(w//2 - 110, h//2 + 80, 220, 60, "ADD", GREEN)
    btn_return = button(w//2 - 110, h - 100, 220, 60, "RETURN", BLUE)
    
    # Zone de texte
    input_rect = pygame.Rect(w//2 - 300, h//2 - 30, 600, 70)
    text = ''
    active = False
    
    message = ""
    msg_color = WHITE
    msg_timer = 0
    
    while True:
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter", screen
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Clic sur input
                active = input_rect.collidepoint(pos)
                
                # Bouton ADD
                if btn_add.for_clic(pos) and text.strip():
                    success, msg = save_words(text)
                    message = msg
                    msg_color = GREEN if success else RED
                    msg_timer = 120
                    if success:
                        text = ''
                
                # Bouton RETURN
                if btn_return.for_clic(pos):
                    return "menu", screen
            
            
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_RETURN and text.strip():
                    success, msg = save_words(text)
                    message = msg
                    msg_color = GREEN if success else RED
                    msg_timer = 120
                    if success:
                        text = ''
                elif len(text) < 80:  # Limite de caractères
                    if event.unicode.isalpha() or event.unicode in ' ,-\'éèêàùç':
                        text += event.unicode
        
        # Hover
        btn_add.check_hover(pos)
        btn_return.check_hover(pos)
        
        if msg_timer > 0:
            msg_timer -= 1
            if msg_timer == 0:
                message = ""
        
        # Dessiner
        screen.fill(FOND)
        draw_title(screen, "ADD WORDS", 50, WHITE)
        
        # Instructions
        font = pygame.font.Font(None, 28)
        txt = font.render("Separate multiple words with commas (ex: cat, dog, fish)", True, GRAY)
        screen.blit(txt, (w//2 - txt.get_width()//2, h//2 - 100))
        
        
        color = BLUE if active else GRAY
        pygame.draw.rect(screen, (50, 50, 70), input_rect)
        pygame.draw.rect(screen, color, input_rect, 3)
        
        font_input = pygame.font.Font(None, 32)
        txt_surface = font_input.render(text, True, WHITE)
        screen.blit(txt_surface, (input_rect.x + 10, input_rect.y + 20))
        
        
        btn_add.draw(screen)
        btn_return.draw(screen)
        
        # Message
        if message:
            font_msg = pygame.font.Font(None, 32)
            msg_surf = font_msg.render(message, True, msg_color)
            screen.blit(msg_surf, (w//2 - msg_surf.get_width()//2, h//2 + 160))
        
        pygame.display.flip()
        clock.tick(FPS)
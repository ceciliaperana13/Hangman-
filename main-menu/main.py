import pygame
import sys
import math
import mainV5
import score 
import add_word
from settings import button, cursor, buttonSwitch, Selector, draw_potence, draw_title




pygame.init()
pygame.mixer.init()

# load music
pygame.mixer.music.load("./song/song_de_base.mp3")
pygame.mixer.music.set_volume(0.5)  # 50% 
pygame.mixer.music.play(-1)

FPS = 60

# colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (70, 130, 180)
BLUE_LIGTH = (100, 160, 210)
GREEN = (46, 125, 50)
FOND = (30, 30, 50)

# window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hangman Game")
clock = pygame.time.Clock()


class ManageOptions:
    def __init__(self, screen):
        self.volume_music = 50
        self.volume_effects = 50
        self.full_screen = False
        self.resolution = '800x600'
        self.screen = screen
    
    def apply_resolution(self):
        width, height = map(int, self.resolution.split('x'))
        flags = pygame.FULLSCREEN if self.full_screen else 0
        self.screen = pygame.display.set_mode((width, height), flags)
        return self.screen
    
    def save(self, music, effects, full_screen, resolution):
        self.volume_music = music
        self.volume_effects = effects
        self.full_screen = full_screen
        self.resolution = resolution
        self.screen = self.apply_resolution()
        return self.screen


#  Main Menu
def main_menu(screen, clock, options_manager):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Boutons principaux centrés
    center_x = screen_width // 2
    btn_width = 300
    
    buttons = [
        button(center_x - btn_width // 2, screen_height - 280, btn_width, 60, "PLAY", BLUE),
        button(center_x - btn_width // 2, screen_height - 200, btn_width, 60, "OPTIONS", BLUE),
        button(center_x - btn_width // 2, screen_height - 120, btn_width, 60, "QUIT", BLUE)
    ]
    
    # Petits boutons en haut à droite
    btn_add_word = button(screen_width - 160, 20, 140, 40, "Add Word", GREEN)
    btn_scores = button(screen_width - 160, 70, 140, 40, "Scores", BLUE)
    
    time = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter", screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if buttons[0].for_clic(pos):
                    return "PLAY", screen
                    
                elif buttons[1].for_clic(pos):
                    return "options", screen
                elif buttons[2].for_clic(pos):
                    return "quitter", screen
                elif btn_add_word.for_clic(pos):
                    return "add_world",screen
                    # return "add_word", screen
                elif btn_scores.for_clic(pos):
                    return "scores", screen
        
        pos = pygame.mouse.get_pos()
        for btn in buttons:
            btn.check_hover(pos)
        btn_add_word.check_hover(pos)
        btn_scores.check_hover(pos)
        
        time += 1
        swing = math.sin(time * 0.05) * 0.5
        
        screen.fill(FOND)
        draw_title(screen, "HANGMAN GAME", 60, WHITE)
        
        # Potence centrée
        potence_x = center_x - 75
        draw_potence(screen, potence_x, 120, swing)
        
        for btn in buttons:
            btn.draw(screen)
        
        # Dessiner les petits boutons
        btn_add_word.draw(screen)
        btn_scores.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)


# Options
def page_options(screen, clock, options_manager):
    btn_systeme = button(50, 80, 180, 50, "SYSTEM", BLUE)
    btn_sound = button(250, 80, 180, 50, "SOUND", GRAY)
    btn_return = button(300, 520, 200, 50, "RETURN", GREEN)
    
    Selector_res = Selector(
        400, 200, "Resolution:", 
        ['800x600', '1024x768', '1280x720', '1920x1080'], 
        options_manager.resolution
    )
    switch_full_screen = buttonSwitch(400, 280, "Fullscreen:", options_manager.full_screen)
    
    cursor_music = cursor(400, 220, 250, "Music:", options_manager.volume_music)
    cursor_effects = cursor(400, 300, 250, "Effects:", options_manager.volume_effects)
    
    category = "systeme"
    
    while True:
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter", screen
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_return.for_clic(pos):
                    screen = options_manager.save(
                        cursor_music.value,
                        cursor_effects.value,
                        switch_full_screen.active,
                        Selector_res.get_value()
                    )
                    pygame.mixer.music.set_volume(cursor_music.value / 100)
                    return "menu", screen
                
                if btn_systeme.for_clic(pos):
                    category = "systeme"
                    btn_systeme.color = BLUE
                    btn_sound.color = GRAY
                
                if btn_sound.for_clic(pos):
                    category = "sound"
                    btn_systeme.color = GRAY
                    btn_sound.color = BLUE
                
                if category == "systeme":
                    Selector_res.clic(pos)
                    switch_full_screen.clic(pos)
            
            if category == "sound":
                cursor_music.manage_clic(event, pos)
                cursor_effects.manage_clic(event, pos)

                #sound update 
                pygame.mixer.music.set_volume(cursor_music.value / 100)
        
        btn_systeme.check_hover(pos)
        btn_sound.check_hover(pos)
        btn_return.check_hover(pos)
        if category == "systeme":
            Selector_res.check_hover(pos)
        
        screen.fill(FOND)
        draw_title(screen, "OPTIONS", 40, WHITE)
        
        btn_systeme.draw(screen)
        btn_sound.draw(screen)
        
        police = pygame.font.Font(None, 40)
        if category == "systeme":
            tittle_cat = police.render("Screen and Display", True, WHITE)
            screen.blit(tittle_cat, (80, 160))
            Selector_res.draw(screen)
            switch_full_screen.draw(screen)
        else:
            tittle_cat = police.render("Audio Settings", True, WHITE)
            screen.blit(tittle_cat, (80, 160))
            cursor_music.draw(screen)
            cursor_effects.draw(screen)
        
        btn_return.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)




def main():
    options_manager = ManageOptions(screen)
    page = "menu"
    screen_actuel = screen
    
    while True:
        if page == "menu":
            page, screen_actuel = main_menu(screen_actuel, clock, options_manager)  

        elif page == "options":
            page, screen_actuel = page_options(screen_actuel, clock, options_manager)

        elif page == "PLAY":
            page = mainV5.main(screen_actuel)
            screen_actuel = options_manager.apply_resolution()
            
        elif page == "scores":
            page, screen_actuel = score.page_scores(screen_actuel, clock)

        elif page == "add_world":
            page, screen_actuel = add_word.add_word(screen_actuel, clock)

        elif page == "quitter":
            break
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

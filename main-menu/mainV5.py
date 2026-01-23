import pygame
from game import HangmanGame
from settings import SCREENWIDTH, SCREENHEIGHT, BLACK, WHITE, BLUE, GREEN

def ask_player_name(screen, clock):
    """Demande le nom du joueur avant de commencer"""
    player_name = ""
    input_active = True
    
    font_title = pygame.font.Font(None, 60)
    font_instruction = pygame.font.Font(None, 36)
    font_input = pygame.font.Font(None, 64)
    
    # Dimensions  boîte d'input
    input_box = pygame.Rect(SCREENWIDTH // 2 - 200, SCREENHEIGHT // 2 - 35, 400, 70)
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Valider avec Entrée
                    if player_name.strip():
                        return player_name.strip()
                elif event.key == pygame.K_ESCAPE:
                    # Annuler avec Échap
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    # Supprimer le dernier caractère
                    player_name = player_name[:-1]
                elif event.unicode.isalnum() or event.unicode == " ":
                    # Ajouter des caractères alphanumériques
                    if len(player_name) < 15:
                        player_name += event.unicode
        
        
        screen.fill(BLACK)
        
        # Titre
        title = font_title.render("ENTER YOUR NAME", True, WHITE)
        screen.blit(title, (SCREENWIDTH // 2 - title.get_width() // 2, 100))
        
        # Instructions
        instruction1 = font_instruction.render("Type your name and press ENTER", True, (200, 200, 200))
        instruction2 = font_instruction.render("or press ESC to skip", True, (150, 150, 150))
        screen.blit(instruction1, (SCREENWIDTH // 2 - instruction1.get_width() // 2, 200))
        screen.blit(instruction2, (SCREENWIDTH // 2 - instruction2.get_width() // 2, 240))
        
        # Boîte d'input
        color = WHITE if player_name.strip() else (100, 100, 100)
        pygame.draw.rect(screen, color, input_box, 3)
        
        # Texte saisi
        if player_name:
            name_surface = font_input.render(player_name, True, WHITE)
            screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))
        else:
            # Placeholder
            placeholder = font_instruction.render("Player", True, (80, 80, 80))
            screen.blit(placeholder, (input_box.x + 10, input_box.y + 20))
        
        # Curseur clignotant
        if player_name and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = input_box.x + 10 + font_input.size(player_name)[0]
            pygame.draw.line(screen, WHITE, 
                           (cursor_x, input_box.y + 10), 
                           (cursor_x, input_box.y + 60), 3)
        
        # Indication de touche
        hint = font_instruction.render("Press ENTER to start", True, GREEN if player_name.strip() else (80, 80, 80))
        screen.blit(hint, (SCREENWIDTH // 2 - hint.get_width() // 2, SCREENHEIGHT - 100))
        
        pygame.display.flip()
        clock.tick(60)
    
    return "Player"  


def main(screen):
    """Fonction principale du jeu Hangman"""
    
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Hangman")

    clock = pygame.time.Clock()
    
    #  ÉTAPE 1 : Demander le nom du joueur
    player_name = ask_player_name(screen, clock)
    
    # Si l'utilisateur a fermé la fenêtre ou appuyé sur ESC
    if player_name is None:
        return "menu"
    
    
    game = HangmanGame(screen)
    game.set_player_name(player_name)
    
    print(f"🎮 Partie démarrée pour : {player_name}")
    
    RUN = True

    while RUN:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handleClick(event.pos)

            if event.type == pygame.KEYDOWN:
                # Retour au menu avec ESC
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                
                # Pass the whole event object to handleKey
                game.handleKey(event)

        
        game.checkGameOver()
        
        
        game.draw()
        pygame.display.update()
    
    return "menu"
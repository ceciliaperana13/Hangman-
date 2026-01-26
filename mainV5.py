import pygame
from game import HangmanGame
from settings import SCREENWIDTH, SCREENHEIGHT, BLACK, WHITE, BLUE, GREEN


def ask_player_name(screen, clock):
    """Ask the player for their name before starting the game"""
    player_name = ""
    input_active = True
    
    font_title = pygame.font.Font(None, 60)
    font_instruction = pygame.font.Font(None, 36)
    font_input = pygame.font.Font(None, 64)
    
    # Input box dimensions
    input_box = pygame.Rect(
        SCREENWIDTH // 2 - 200,
        SCREENHEIGHT // 2 - 35,
        400,
        70
    )
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Validate with ENTER
                    if player_name.strip():
                        return player_name.strip()
                
                elif event.key == pygame.K_ESCAPE:
                    # Cancel with ESC
                    return None
                
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character
                    player_name = player_name[:-1]
                
                elif event.unicode.isalnum() or event.unicode == " ":
                    # Add alphanumeric characters
                    if len(player_name) < 15:
                        player_name += event.unicode
        
        screen.fill(BLACK)
        
        # Title
        title = font_title.render("ENTER YOUR NAME", True, WHITE)
        screen.blit(
            title,
            (SCREENWIDTH // 2 - title.get_width() // 2, 100)
        )
        
        # Instructions
        instruction1 = font_instruction.render(
            "Type your name and press ENTER",
            True,
            (200, 200, 200)
        )
        instruction2 = font_instruction.render(
            "or press ESC to skip",
            True,
            (150, 150, 150)
        )
        screen.blit(
            instruction1,
            (SCREENWIDTH // 2 - instruction1.get_width() // 2, 200)
        )
        screen.blit(
            instruction2,
            (SCREENWIDTH // 2 - instruction2.get_width() // 2, 240)
        )
        
        # Input box
        color = WHITE if player_name.strip() else (100, 100, 100)
        pygame.draw.rect(screen, color, input_box, 3)
        
        # Typed text
        if player_name:
            name_surface = font_input.render(player_name, True, WHITE)
            screen.blit(
                name_surface,
                (input_box.x + 10, input_box.y + 10)
            )
        else:
            # Placeholder text
            placeholder = font_instruction.render("Player", True, (80, 80, 80))
            screen.blit(
                placeholder,
                (input_box.x + 10, input_box.y + 20)
            )
        
        # Blinking cursor
        if player_name and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = input_box.x + 10 + font_input.size(player_name)[0]
            pygame.draw.line(
                screen,
                WHITE,
                (cursor_x, input_box.y + 10),
                (cursor_x, input_box.y + 60),
                3
            )
        
        # Key hint
        hint = font_instruction.render(
            "Press ENTER to start",
            True,
            GREEN if player_name.strip() else (80, 80, 80)
        )
        screen.blit(
            hint,
            (SCREENWIDTH // 2 - hint.get_width() // 2, SCREENHEIGHT - 100)
        )
        
        pygame.display.flip()
        clock.tick(60)
    
    return "Player"


def main(screen):
    """Main Hangman game function"""
    
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Hangman")

    clock = pygame.time.Clock()
    
    # STEP 1: Ask for the player's name
    player_name = ask_player_name(screen, clock)
    
    # If the user closed the window or pressed ESC
    if player_name is None:
        return "menu"
    
    game = HangmanGame(screen)
    game.set_player_name(player_name)
    
    print(f"🎮 Game started for: {player_name}")
    
    RUN = True

    while RUN:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handleClick(event.pos)

            if event.type == pygame.KEYDOWN:
                # Return to menu with ESC
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                
                # Pass the full event object to handleKey
                game.handleKey(event)
        
        # Check win/lose conditions
        game.checkGameOver()
        
        # Draw the game
        game.draw()
        pygame.display.update()
    
    return "menu"





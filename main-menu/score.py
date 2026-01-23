import pygame
from datetime import datetime
from settings import button, draw_title

# Colors
WHITE = (255, 255, 255)
BLUE = (70, 130, 180)
GREEN = (46, 125, 50)
RED = (220, 50, 50)
FOND = (30, 30, 50)
GRAY = (200, 200, 200)

SCORES_FILE = "scores.txt"


def load_scores():
    """Charge les scores depuis le fichier scores.txt"""
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            scores = []
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split("|")
                    if len(parts) >= 7:
                        score_entry = {
                            "player": parts[0],
                            "word": parts[1],
                            "result": parts[2],
                            "score": int(parts[3]),
                            "attempts": int(parts[4]),
                            "max_attempts": int(parts[5]),
                            "date": parts[6],
                            "timestamp": float(parts[7]) if len(parts) > 7 else 0
                        }
                        scores.append(score_entry)
            return scores
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f" Erreur lors du chargement: {e}")
        return []


def save_all_scores(scores):
    """Sauvegarde tous les scores dans le fichier"""
    try:
        with open(SCORES_FILE, "w", encoding="utf-8") as f:
            for score in scores:
                line = f"{score['player']}|{score['word']}|{score['result']}|{score['score']}|{score['attempts']}|{score['max_attempts']}|{score['date']}|{score['timestamp']}\n"
                f.write(line)
    except Exception as e:
        print(f" Erreur lors de la sauvegarde: {e}")


def add_score(player_name, word, result, attempts, max_attempts):
    """
    Ajoute un nouveau score à scores.txt
    
    Args:
        player_name: Nom du joueur
        word: Mot à deviner
        result: "WIN" ou "LOSE"
        attempts: Nombre d'erreurs faites
        max_attempts: Nombre maximum d'erreurs autorisées
    """
    scores = load_scores()
    
    # Calculer le score (100 points max - points perdus pour chaque erreur)
    if result == "WIN":
        score_value = max(100 - (attempts * 10), 10)  # Minimum 10 points
    else:
        score_value = 0
    
    new_score = {
        "player": player_name,
        "word": word,
        "result": result,
        "score": score_value,
        "attempts": attempts,
        "max_attempts": max_attempts,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "timestamp": datetime.now().timestamp()
    }
    
    scores.append(new_score)
    
    # Trier par score décroissant, puis par date
    scores.sort(key=lambda x: (-x["score"], -x["timestamp"]))
    
    # Sauvegarder dans le fichier
    save_all_scores(scores)
    
    print(f" Score sauvegardé: {player_name} - {result} - {score_value} points")


def clear_scores():
    """Efface tous les scores du fichier"""
    try:
        with open(SCORES_FILE, "w", encoding="utf-8") as f:
            f.write("")
        print(" Scores effacés")
    except Exception as e:
        print(f" Erreur lors de l'effacement: {e}")


def page_scores(screen, clock):
    """Affiche l'historique des scores en temps réel depuis scores.txt"""
    
    btn_return = button(300, 520, 200, 50, "RETURN", GREEN)
    btn_clear = button(100, 520, 180, 50, "CLEAR ALL", RED)
    
    scroll_offset = 0
    
    while True:
        pos = pygame.mouse.get_pos()
        
        # Recharger les scores depuis le fichier à chaque frame
        scores_data = load_scores()
        max_scroll = max(0, len(scores_data) * 35 - 300)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter", screen
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_return.for_clic(pos):
                    return "menu", screen
                
                if btn_clear.for_clic(pos):
                    clear_scores()
            
            # Scroll avec la molette
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset = max(0, min(scroll_offset - event.y * 20, max_scroll))
        
        btn_return.check_hover(pos)
        btn_clear.check_hover(pos)
        
        screen.fill(FOND)
        draw_title(screen, "SCOREBOARD", 40, WHITE)
        
        # Afficher les scores
        font = pygame.font.Font(None, 28)
        y_offset = 150
        
        if not scores_data:
            no_scores = font.render("No scores yet! Play to add scores.", True, GRAY)
            screen.blit(no_scores, (screen.get_width() // 2 - no_scores.get_width() // 2, 250))
        else:
            # En-têtes du tableau
            header_font = pygame.font.Font(None, 26)
            rank_text = header_font.render("Rank", True, WHITE)
            player_text = header_font.render("Player", True, WHITE)
            word_text = header_font.render("Word", True, WHITE)
            result_text = header_font.render("Result", True, WHITE)
            score_text = header_font.render("Score", True, WHITE)
            date_text = header_font.render("Date", True, WHITE)
            
            screen.blit(rank_text, (30, y_offset))
            screen.blit(player_text, (100, y_offset))
            screen.blit(word_text, (250, y_offset))
            screen.blit(result_text, (380, y_offset))
            screen.blit(score_text, (480, y_offset))
            screen.blit(date_text, (570, y_offset))
            
            y_offset += 35
            
            # Ligne de séparation
            pygame.draw.line(screen, WHITE, (20, y_offset), (780, y_offset), 2)
            y_offset += 10
            
            # Afficher chaque score
            for i, score_entry in enumerate(scores_data):
                item_y = y_offset + (i * 35) - scroll_offset
                
                # Ne dessiner que si visible
                if item_y < y_offset - 40 or item_y > y_offset + 300:
                    continue
                
                rank = font.render(f"#{i+1}", True, GRAY)
                player = font.render(score_entry["player"][:12], True, WHITE)
                word = font.render(score_entry["word"][:10], True, WHITE)
                
                # Couleur selon résultat
                result_color = GREEN if score_entry["result"] == "WIN" else RED
                result = font.render(score_entry["result"], True, result_color)
                
                score_val = font.render(str(score_entry["score"]), True, GREEN)
                date = font.render(score_entry["date"].split()[0], True, GRAY)
                
                screen.blit(rank, (30, item_y))
                screen.blit(player, (100, item_y))
                screen.blit(word, (250, item_y))
                screen.blit(result, (380, item_y))
                screen.blit(score_val, (480, item_y))
                screen.blit(date, (570, item_y))
            
            # Indicateur de scroll
            if max_scroll > 0:
                info_text = font.render("Use mouse wheel to scroll", True, GRAY)
                screen.blit(info_text, (screen.get_width() // 2 - info_text.get_width() // 2, 470))
        
        btn_clear.draw(screen)
        btn_return.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    # Retour de sécurité 
    return "menu", screen
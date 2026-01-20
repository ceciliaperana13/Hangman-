import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
FPS = 60

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (128, 128, 128)
GRIS_CLAIR = (200, 200, 200)
MARRON = (139, 69, 19)
MARRON_FONCE = (101, 67, 33)
BLEU = (70, 130, 180)
BLEU_CLAIR = (100, 160, 210)

# Création de la fenêtre
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu du Pendu - Menu Principal")
horloge = pygame.time.Clock()

class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, couleur, couleur_survol):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = couleur
        self.couleur_survol = couleur_survol
        self.survole = False
    
    def dessiner(self, surface):
        couleur_actuelle = self.couleur_survol if self.survole else self.couleur
        pygame.draw.rect(surface, couleur_actuelle, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLANC, self.rect, 3, border_radius=10)
        
        police = pygame.font.Font(None, 48)
        texte_surface = police.render(self.texte, True, BLANC)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)
    
    def verifier_survol(self, pos):
        self.survole = self.rect.collidepoint(pos)
        return self.survole
    
    def est_clique(self, pos):
        return self.rect.collidepoint(pos)

def dessiner_potence(surface, x, y, balancement):
    # Base gauche
    pygame.draw.rect(surface, MARRON, (x, y + 190, 40, 25))
    pygame.draw.rect(surface, MARRON_FONCE, (x, y + 190, 40, 25), 2)
    
    # Poteau gauche
    pygame.draw.rect(surface, MARRON, (x + 15, y, 15, 195))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 15, y, 15, 195), 2)
    
    # Poutre horizontale
    pygame.draw.rect(surface, MARRON, (x + 30, y, 100, 15))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 30, y, 100, 15), 2)
    
    # Support diagonal
    points = [(x + 30, y + 15), (x + 30, y), (x + 60, y)]
    pygame.draw.polygon(surface, MARRON_FONCE, points)
    
    # Base droite
    pygame.draw.rect(surface, MARRON, (x + 110, y + 190, 40, 25))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 110, y + 190, 40, 25), 2)
    
    # Poteau droit
    pygame.draw.rect(surface, MARRON, (x + 120, y, 15, 195))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 120, y, 15, 195), 2)
    
    # Point d'attache de la corde
    corde_x = x + 90
    corde_y = y + 15
    
    # Corde avec balancement
    corde_fin_x = corde_x + int(balancement * 10)
    corde_fin_y = corde_y + 30
    pygame.draw.line(surface, (218, 165, 32), (corde_x, corde_y), (corde_fin_x, corde_fin_y), 3)
    
    # Bonhomme avec balancement
    tete_x = corde_fin_x
    tete_y = corde_fin_y + 15
    
    # Tête
    pygame.draw.circle(surface, BLANC, (tete_x, tete_y), 15, 3)
    
    # Corps
    corps_fin_y = tete_y + 50
    pygame.draw.line(surface, BLANC, (tete_x, tete_y + 15), (tete_x, corps_fin_y), 3)
    
    # Bras gauche
    pygame.draw.line(surface, BLANC, (tete_x, tete_y + 25), (tete_x - 20, tete_y + 35), 3)
    # Bras droit
    pygame.draw.line(surface, BLANC, (tete_x, tete_y + 25), (tete_x + 20, tete_y + 35), 3)
    
    # Jambe gauche
    pygame.draw.line(surface, BLANC, (tete_x, corps_fin_y), (tete_x - 15, corps_fin_y + 25), 3)
    # Jambe droite
    pygame.draw.line(surface, BLANC, (tete_x, corps_fin_y), (tete_x + 15, corps_fin_y + 25), 3)
    
    # Plateforme 
    pygame.draw.rect(surface, GRIS, (tete_x - 30, corps_fin_y + 30, 60, 8))
    pygame.draw.rect(surface, GRIS_CLAIR, (tete_x - 30, corps_fin_y + 30, 60, 8), 2)

def main():
    # Création des boutons
    boutons = [
        Bouton(LARGEUR // 2 - 150, 320, 300, 60, "JOUER", BLEU, BLEU_CLAIR),
        Bouton(LARGEUR // 2 - 150, 400, 300, 60, "OPTIONS", BLEU, BLEU_CLAIR),
        Bouton(LARGEUR // 2 - 150, 480, 300, 60, "QUITTER", BLEU, BLEU_CLAIR)
    ]
    
    temps = 0
    
    
    en_cours = True
    while en_cours:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_souris = pygame.mouse.get_pos()
                
                if boutons[0].est_clique(pos_souris):  # Jouer
                    print("Lancement du jeu...")
                    
                
                elif boutons[1].est_clique(pos_souris):  # OPTIONS
                    print("Ouverture des options...")
                    #ouvrir l'option ici cecilia
                
                elif boutons[2].est_clique(pos_souris):  # QUITTER
                    en_cours = False
        
        
        pos_souris = pygame.mouse.get_pos()
        for bouton in boutons:
            bouton.verifier_survol(pos_souris)
        
        # Calcul du balancement
        temps += 1
        balancement = math.sin(temps * 0.05) * 0.5
        
        
        ecran.fill((30, 30, 50))
        
        
        police_titre = pygame.font.Font(None, 72)
        titre = police_titre.render("JEU DU PENDU", True, BLANC)
        titre_rect = titre.get_rect(center=(LARGEUR // 2, 60))
        ecran.blit(titre, titre_rect)
        
       
        dessiner_potence(ecran, LARGEUR // 2 - 75, 120, balancement)
        
        
        for bouton in boutons:
            bouton.dessiner(ecran)
        
        
        pygame.display.flip()
        horloge.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
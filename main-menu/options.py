import pygame

# Couleurs
BLANC = (255, 255, 255)
GRIS = (128, 128, 128)
GRIS_CLAIR = (200, 200, 200)
GRIS_FONCE = (60, 60, 60)
MARRON = (139, 69, 19)
MARRON_FONCE = (101, 67, 33)
BLEU = (70, 130, 180)
BLEU_CLAIR = (100, 160, 210)
VERT = (46, 125, 50)


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, couleur):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = couleur
        self.survole = False
    
    def dessiner(self, surface):
        couleur = BLEU_CLAIR if self.survole else self.couleur
        pygame.draw.rect(surface, couleur, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLANC, self.rect, 3, border_radius=10)
        
        police = pygame.font.Font(None, 40)
        texte = police.render(self.texte, True, BLANC)
        rect_texte = texte.get_rect(center=self.rect.center)
        surface.blit(texte, rect_texte)
    
    def verifier_survol(self, pos):
        self.survole = self.rect.collidepoint(pos)
    
    def est_clique(self, pos):
        return self.rect.collidepoint(pos)


class Curseur:
    def __init__(self, x, y, largeur, nom, valeur_initiale):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.nom = nom
        self.valeur = valeur_initiale
        self.en_deplacement = False
        self.rect_bouton = pygame.Rect(0, 0, 20, 30)
        self.mettre_a_jour()
    
    def mettre_a_jour(self):
        pos_x = self.x + int((self.valeur / 100) * self.largeur)
        self.rect_bouton.center = (pos_x, self.y)
    
    def dessiner(self, surface):
        # Nom
        police = pygame.font.Font(None, 32)
        texte = police.render(self.nom, True, BLANC)
        surface.blit(texte, (self.x - 150, self.y - 10))
        
        # Valeur
        valeur_texte = police.render(f"{self.valeur}%", True, BLANC)
        surface.blit(valeur_texte, (self.x + self.largeur + 20, self.y - 10))
        
        # Barre
        pygame.draw.line(surface, GRIS, (self.x, self.y), (self.x + self.largeur, self.y), 4)
        pygame.draw.line(surface, BLEU, (self.x, self.y), (self.rect_bouton.centerx, self.y), 6)
        
        # Bouton
        pygame.draw.rect(surface, BLEU_CLAIR, self.rect_bouton, border_radius=5)
        pygame.draw.rect(surface, BLANC, self.rect_bouton, 2, border_radius=5)
    
    def gerer_clic(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_bouton.collidepoint(pos):
                self.en_deplacement = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.en_deplacement = False
        elif event.type == pygame.MOUSEMOTION and self.en_deplacement:
            nouvelle_pos = max(self.x, min(pos[0], self.x + self.largeur))
            self.valeur = int(((nouvelle_pos - self.x) / self.largeur) * 100)
            self.mettre_a_jour()


class BoutonSwitch:
    def __init__(self, x, y, nom, actif):
        self.x = x
        self.y = y
        self.nom = nom
        self.actif = actif
        self.rect = pygame.Rect(x, y, 60, 30)
    
    def dessiner(self, surface):
        police = pygame.font.Font(None, 32)
        texte = police.render(self.nom, True, BLANC)
        surface.blit(texte, (self.x - 150, self.y))
        
        couleur = VERT if self.actif else GRIS_FONCE
        pygame.draw.rect(surface, couleur, self.rect, border_radius=15)
        pygame.draw.rect(surface, BLANC, self.rect, 2, border_radius=15)
        
        cercle_x = self.x + 45 if self.actif else self.x + 15
        pygame.draw.circle(surface, BLANC, (cercle_x, self.y + 15), 12)
    
    def clic(self, pos):
        if self.rect.collidepoint(pos):
            self.actif = not self.actif
            return True
        return False


class Selecteur:
    def __init__(self, x, y, nom, options, option_active):
        self.x = x
        self.y = y
        self.nom = nom
        self.options = options
        self.index = options.index(option_active)
        self.rect = pygame.Rect(x, y, 200, 40)
        self.survole = False
    
    def dessiner(self, surface):
        police = pygame.font.Font(None, 32)
        texte = police.render(self.nom, True, BLANC)
        surface.blit(texte, (self.x - 150, self.y + 5))
        
        couleur = BLEU_CLAIR if self.survole else BLEU
        pygame.draw.rect(surface, couleur, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLANC, self.rect, 2, border_radius=8)
        
        police_option = pygame.font.Font(None, 28)
        option_texte = police_option.render(self.options[self.index], True, BLANC)
        rect_texte = option_texte.get_rect(center=self.rect.center)
        surface.blit(option_texte, rect_texte)
        
        police_fleche = pygame.font.Font(None, 28)
        surface.blit(police_fleche.render("<", True, BLANC), (self.rect.x + 10, self.rect.centery - 10))
        surface.blit(police_fleche.render(">", True, BLANC), (self.rect.right - 25, self.rect.centery - 10))
    
    def verifier_survol(self, pos):
        self.survole = self.rect.collidepoint(pos)
    
    def clic(self, pos):
        if self.rect.collidepoint(pos):
            if pos[0] < self.rect.centerx:
                self.index = (self.index - 1) % len(self.options)
            else:
                self.index = (self.index + 1) % len(self.options)
            return True
        return False
    
    def obtenir_valeur(self):
        return self.options[self.index]


def dessiner_potence(surface, x, y, balancement):
    # Bases
    pygame.draw.rect(surface, MARRON, (x, y + 190, 40, 25))
    pygame.draw.rect(surface, MARRON_FONCE, (x, y + 190, 40, 25), 2)
    pygame.draw.rect(surface, MARRON, (x + 110, y + 190, 40, 25))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 110, y + 190, 40, 25), 2)
    
    # Poteaux
    pygame.draw.rect(surface, MARRON, (x + 15, y, 15, 195))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 15, y, 15, 195), 2)
    pygame.draw.rect(surface, MARRON, (x + 120, y, 15, 195))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 120, y, 15, 195), 2)
    
    # Poutre
    pygame.draw.rect(surface, MARRON, (x + 30, y, 100, 15))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 30, y, 100, 15), 2)
    
    # Support
    pygame.draw.polygon(surface, MARRON_FONCE, [(x + 30, y + 15), (x + 30, y), (x + 60, y)])
    
    # Corde
    corde_x = x + 90 + int(balancement * 10)
    pygame.draw.line(surface, (218, 165, 32), (x + 90, y + 15), (corde_x, y + 45), 3)
    
    # Bonhomme
    pygame.draw.circle(surface, BLANC, (corde_x, y + 60), 15, 3)
    pygame.draw.line(surface, BLANC, (corde_x, y + 75), (corde_x, y + 125), 3)
    pygame.draw.line(surface, BLANC, (corde_x, y + 85), (corde_x - 20, y + 95), 3)
    pygame.draw.line(surface, BLANC, (corde_x, y + 85), (corde_x + 20, y + 95), 3)
    pygame.draw.line(surface, BLANC, (corde_x, y + 125), (corde_x - 15, y + 150), 3)
    pygame.draw.line(surface, BLANC, (corde_x, y + 125), (corde_x + 15, y + 150), 3)
    
    # Plateforme
    pygame.draw.rect(surface, GRIS, (corde_x - 30, y + 155, 60, 8))
    pygame.draw.rect(surface, GRIS_CLAIR, (corde_x - 30, y + 155, 60, 8), 2)


def dessiner_titre(surface, texte, y, couleur):
    police = pygame.font.Font(None, 64)
    titre = police.render(texte, True, couleur)
    rect = titre.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(titre, rect)
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
GRIS_FONCE = (60, 60, 60)
MARRON = (139, 69, 19)
MARRON_FONCE = (101, 67, 33)
BLEU = (70, 130, 180)
BLEU_CLAIR = (100, 160, 210)
VERT = (46, 125, 50)
VERT_CLAIR = (76, 175, 80)

# Création de la fenêtre
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu du Pendu")
horloge = pygame.time.Clock()

# Options du jeu
options_jeu = {
    'volume_musique': 50,
    'volume_effets': 50,
    'plein_ecran': False,
    'resolution': '800x600'
}

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
        
        taille_police = 48 if len(self.texte) < 10 else 36
        police = pygame.font.Font(None, taille_police)
        texte_surface = police.render(self.texte, True, BLANC)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)
    
    def verifier_survol(self, pos):
        self.survole = self.rect.collidepoint(pos)
        return self.survole
    
    def est_clique(self, pos):
        return self.rect.collidepoint(pos)

class Curseur:
    def __init__(self, x, y, largeur, valeur_min, valeur_max, valeur_initiale, nom):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.valeur_min = valeur_min
        self.valeur_max = valeur_max
        self.valeur = valeur_initiale
        self.nom = nom
        self.en_deplacement = False
        self.rect_curseur = pygame.Rect(0, 0, 20, 30)
        self.mettre_a_jour_position()
    
    def mettre_a_jour_position(self):
        ratio = (self.valeur - self.valeur_min) / (self.valeur_max - self.valeur_min)
        pos_x = self.x + int(ratio * self.largeur)
        self.rect_curseur.center = (pos_x, self.y)
    
    def dessiner(self, surface):
        # Label
        police = pygame.font.Font(None, 32)
        label = police.render(self.nom, True, BLANC)
        surface.blit(label, (self.x - 200, self.y - 10))
        
        # Valeur
        valeur_texte = police.render(f"{self.valeur}%", True, BLANC)
        surface.blit(valeur_texte, (self.x + self.largeur + 20, self.y - 10))
        
        # Ligne du curseur
        pygame.draw.line(surface, GRIS, (self.x, self.y), (self.x + self.largeur, self.y), 4)
        # Partie remplie
        pos_curseur = self.rect_curseur.centerx
        pygame.draw.line(surface, BLEU, (self.x, self.y), (pos_curseur, self.y), 6)
        # Bouton du curseur
        pygame.draw.rect(surface, BLEU_CLAIR, self.rect_curseur, border_radius=5)
        pygame.draw.rect(surface, BLANC, self.rect_curseur, 2, border_radius=5)
    
    def gerer_evenement(self, event, pos_souris):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_curseur.collidepoint(pos_souris):
                self.en_deplacement = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.en_deplacement = False
        elif event.type == pygame.MOUSEMOTION and self.en_deplacement:
            nouvelle_pos = max(self.x, min(pos_souris[0], self.x + self.largeur))
            ratio = (nouvelle_pos - self.x) / self.largeur
            self.valeur = int(self.valeur_min + ratio * (self.valeur_max - self.valeur_min))
            self.mettre_a_jour_position()

class BoutonBascule:
    def __init__(self, x, y, nom, actif=False):
        self.x = x
        self.y = y
        self.nom = nom
        self.actif = actif
        self.rect = pygame.Rect(x, y, 60, 30)
        self.survole = False
    
    def dessiner(self, surface):
        # Label
        police = pygame.font.Font(None, 32)
        label = police.render(self.nom, True, BLANC)
        surface.blit(label, (self.x - 200, self.y))
        
        # Fond du bouton
        couleur_fond = VERT if self.actif else GRIS_FONCE
        pygame.draw.rect(surface, couleur_fond, self.rect, border_radius=15)
        pygame.draw.rect(surface, BLANC, self.rect, 2, border_radius=15)
        
        # Cercle mobile
        cercle_x = self.x + 45 if self.actif else self.x + 15
        pygame.draw.circle(surface, BLANC, (cercle_x, self.y + 15), 12)
    
    def verifier_survol(self, pos):
        self.survole = self.rect.collidepoint(pos)
    
    def clic(self, pos):
        if self.rect.collidepoint(pos):
            self.actif = not self.actif
            return True
        return False

class SelecteurOption:
    def __init__(self, x, y, nom, options, option_active):
        self.x = x
        self.y = y
        self.nom = nom
        self.options = options
        self.index_actif = options.index(option_active)
        self.rect = pygame.Rect(x, y, 200, 40)
        self.survole = False
    
    def dessiner(self, surface):
        # Label
        police = pygame.font.Font(None, 32)
        label = police.render(self.nom, True, BLANC)
        surface.blit(label, (self.x - 200, self.y + 5))
        
        # Boîte de sélection
        couleur = BLEU_CLAIR if self.survole else BLEU
        pygame.draw.rect(surface, couleur, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLANC, self.rect, 2, border_radius=8)
        
        # Texte de l'option active
        police_option = pygame.font.Font(None, 28)
        texte = self.options[self.index_actif]
        texte_surface = police_option.render(texte, True, BLANC)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)
        
        # Flèches
        police_fleche = pygame.font.Font(None, 28)
        fleche_gauche = police_fleche.render("<", True, BLANC)
        fleche_droite = police_fleche.render(">", True, BLANC)
        surface.blit(fleche_gauche, (self.rect.x + 10, self.rect.centery - 10))
        surface.blit(fleche_droite, (self.rect.right - 25, self.rect.centery - 10))
    
    def verifier_survol(self, pos):
        self.survole = self.rect.collidepoint(pos)
    
    def clic(self, pos):
        if self.rect.collidepoint(pos):
            if pos[0] < self.rect.centerx:
                self.index_actif = (self.index_actif - 1) % len(self.options)
            else:
                self.index_actif = (self.index_actif + 1) % len(self.options)
            return True
        return False
    
    def obtenir_valeur(self):
        return self.options[self.index_actif]

def dessiner_potence(surface, x, y, balancement):
    pygame.draw.rect(surface, MARRON, (x, y + 190, 40, 25))
    pygame.draw.rect(surface, MARRON_FONCE, (x, y + 190, 40, 25), 2)
    pygame.draw.rect(surface, MARRON, (x + 15, y, 15, 195))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 15, y, 15, 195), 2)
    pygame.draw.rect(surface, MARRON, (x + 30, y, 100, 15))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 30, y, 100, 15), 2)
    points = [(x + 30, y + 15), (x + 30, y), (x + 60, y)]
    pygame.draw.polygon(surface, MARRON_FONCE, points)
    pygame.draw.rect(surface, MARRON, (x + 110, y + 190, 40, 25))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 110, y + 190, 40, 25), 2)
    pygame.draw.rect(surface, MARRON, (x + 120, y, 15, 195))
    pygame.draw.rect(surface, MARRON_FONCE, (x + 120, y, 15, 195), 2)
    
    corde_x = x + 90
    corde_y = y + 15
    corde_fin_x = corde_x + int(balancement * 10)
    corde_fin_y = corde_y + 30
    pygame.draw.line(surface, (218, 165, 32), (corde_x, corde_y), (corde_fin_x, corde_fin_y), 3)
    
    tete_x = corde_fin_x
    tete_y = corde_fin_y + 15
    pygame.draw.circle(surface, BLANC, (tete_x, tete_y), 15, 3)
    corps_fin_y = tete_y + 50
    pygame.draw.line(surface, BLANC, (tete_x, tete_y + 15), (tete_x, corps_fin_y), 3)
    pygame.draw.line(surface, BLANC, (tete_x, tete_y + 25), (tete_x - 20, tete_y + 35), 3)
    pygame.draw.line(surface, BLANC, (tete_x, tete_y + 25), (tete_x + 20, tete_y + 35), 3)
    pygame.draw.line(surface, BLANC, (tete_x, corps_fin_y), (tete_x - 15, corps_fin_y + 25), 3)
    pygame.draw.line(surface, BLANC, (tete_x, corps_fin_y), (tete_x + 15, corps_fin_y + 25), 3)
    pygame.draw.rect(surface, GRIS, (tete_x - 30, corps_fin_y + 30, 60, 8))
    pygame.draw.rect(surface, GRIS_CLAIR, (tete_x - 30, corps_fin_y + 30, 60, 8), 2)

def page_options():
    # Boutons de catégories
    btn_systeme = Bouton(50, 100, 200, 50, "SYSTÈME", BLEU, BLEU_CLAIR)
    btn_son = Bouton(270, 100, 200, 50, "SON", GRIS, GRIS_CLAIR)
    btn_retour = Bouton(LARGEUR // 2 - 100, 520, 200, 50, "RETOUR", VERT, VERT_CLAIR)
    
    # Options système
    selecteur_resolution = SelecteurOption(450, 200, "Résolution:", 
                                          ['800x600', '1024x768', '1280x720', '1920x1080'], 
                                          options_jeu['resolution'])
    bouton_plein_ecran = BoutonBascule(450, 270, "Plein écran:", options_jeu['plein_ecran'])
    
    # Options son
    curseur_musique = Curseur(450, 200, 250, 0, 100, options_jeu['volume_musique'], "Musique:")
    curseur_effets = Curseur(450, 280, 250, 0, 100, options_jeu['volume_effets'], "Effets:")
    
    categorie_active = "systeme"
    
    en_cours = True
    while en_cours:
        pos_souris = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retour.est_clique(pos_souris):
                    # Sauvegarder les options
                    options_jeu['volume_musique'] = curseur_musique.valeur
                    options_jeu['volume_effets'] = curseur_effets.valeur
                    options_jeu['plein_ecran'] = bouton_plein_ecran.actif
                    options_jeu['resolution'] = selecteur_resolution.obtenir_valeur()
                    print(f"Options sauvegardées: {options_jeu}")
                    return "menu"
                
                if btn_systeme.est_clique(pos_souris):
                    categorie_active = "systeme"
                    btn_systeme.couleur = BLEU
                    btn_son.couleur = GRIS
                
                if btn_son.est_clique(pos_souris):
                    categorie_active = "son"
                    btn_systeme.couleur = GRIS
                    btn_son.couleur = BLEU
                
                if categorie_active == "systeme":
                    selecteur_resolution.clic(pos_souris)
                    bouton_plein_ecran.clic(pos_souris)
            
            if categorie_active == "son":
                curseur_musique.gerer_evenement(event, pos_souris)
                curseur_effets.gerer_evenement(event, pos_souris)
        
        # Vérification survol
        btn_systeme.verifier_survol(pos_souris)
        btn_son.verifier_survol(pos_souris)
        btn_retour.verifier_survol(pos_souris)
        selecteur_resolution.verifier_survol(pos_souris)
        bouton_plein_ecran.verifier_survol(pos_souris)
        
        # Dessin
        ecran.fill((30, 30, 50))
        
        # Titre
        police_titre = pygame.font.Font(None, 64)
        titre = police_titre.render("OPTIONS", True, BLANC)
        titre_rect = titre.get_rect(center=(LARGEUR // 2, 50))
        ecran.blit(titre, titre_rect)
        
        # Boutons de catégories
        btn_systeme.dessiner(ecran)
        btn_son.dessiner(ecran)
        
        # Affichage selon la catégorie active
        if categorie_active == "systeme":
            police_cat = pygame.font.Font(None, 48)
            cat_titre = police_cat.render("Fenêtre et Affichage", True, BLANC)
            ecran.blit(cat_titre, (100, 170))
            
            selecteur_resolution.dessiner(ecran)
            bouton_plein_ecran.dessiner(ecran)
        
        elif categorie_active == "son":
            police_cat = pygame.font.Font(None, 48)
            cat_titre = police_cat.render("Réglages Audio", True, BLANC)
            ecran.blit(cat_titre, (100, 170))
            
            curseur_musique.dessiner(ecran)
            curseur_effets.dessiner(ecran)
        
        btn_retour.dessiner(ecran)
        
        pygame.display.flip()
        horloge.tick(FPS)

def menu_principal():
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
                return "quitter"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_souris = pygame.mouse.get_pos()
                
                if boutons[0].est_clique(pos_souris):
                    print("Lancement du jeu...")
                    # Ici votre code de jeu
                
                elif boutons[1].est_clique(pos_souris):
                    return "options"
                
                elif boutons[2].est_clique(pos_souris):
                    return "quitter"
        
        pos_souris = pygame.mouse.get_pos()
        for bouton in boutons:
            bouton.verifier_survol(pos_souris)
        
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

def main():
    page_actuelle = "menu"
    
    while True:
        if page_actuelle == "menu":
            page_actuelle = menu_principal()
        elif page_actuelle == "options":
            page_actuelle = page_options()
        elif page_actuelle == "quitter":
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
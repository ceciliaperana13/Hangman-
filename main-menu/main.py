import pygame
import sys
import math
from options import Bouton, Curseur, BoutonSwitch, Selecteur, dessiner_potence, dessiner_titre

pygame.init()
pygame.mixer.init()

# Charger musique
pygame.mixer.music.load("main-menu/song/song_de_base.mp3")
pygame.mixer.music.set_volume(0.5)  # 50% par défaut
pygame.mixer.music.play(-1)

FPS = 60

# Couleurs
BLANC = (255, 255, 255)
GRIS = (128, 128, 128)
BLEU = (70, 130, 180)
BLEU_CLAIR = (100, 160, 210)
VERT = (46, 125, 50)
FOND = (30, 30, 50)

# Fenêtre
ecran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jeu du Pendu")
horloge = pygame.time.Clock()


class GestionnaireOptions:
    def __init__(self, ecran):
        self.volume_musique = 50
        self.volume_effets = 50
        self.plein_ecran = False
        self.resolution = '800x600'
        self.ecran = ecran
    
    def appliquer_resolution(self):
        largeur, hauteur = map(int, self.resolution.split('x'))
        flags = pygame.FULLSCREEN if self.plein_ecran else 0
        self.ecran = pygame.display.set_mode((largeur, hauteur), flags)
        return self.ecran
    
    def sauvegarder(self, musique, effets, plein_ecran, resolution):
        self.volume_musique = musique
        self.volume_effets = effets
        self.plein_ecran = plein_ecran
        self.resolution = resolution
        self.ecran = self.appliquer_resolution()
        return self.ecran


#  MENU PRINCIPAL 
def menu_principal(ecran, horloge, gestionnaire_options):
    boutons = [
        Bouton(250, 320, 300, 60, "JOUER", BLEU),
        Bouton(250, 400, 300, 60, "OPTIONS", BLEU),
        Bouton(250, 480, 300, 60, "QUITTER", BLEU)
    ]
    temps = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter", ecran
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if boutons[0].est_clique(pos):
                    return "menu", ecran  
                elif boutons[1].est_clique(pos):
                    return "options", ecran
                elif boutons[2].est_clique(pos):
                    return "quitter", ecran
        
        pos = pygame.mouse.get_pos()
        for btn in boutons:
            btn.verifier_survol(pos)
        
        temps += 1
        balancement = math.sin(temps * 0.05) * 0.5
        
        ecran.fill(FOND)
        dessiner_titre(ecran, "JEU DU PENDU", 60, BLANC)
        dessiner_potence(ecran, 275, 120, balancement)
        
        for btn in boutons:
            btn.dessiner(ecran)
        
        pygame.display.flip()
        horloge.tick(FPS)


# Options
def page_options(ecran, horloge, gestionnaire_options):
    btn_systeme = Bouton(50, 80, 180, 50, "SYSTÈME", BLEU)
    btn_son = Bouton(250, 80, 180, 50, "SON", GRIS)
    btn_retour = Bouton(300, 520, 200, 50, "RETOUR", VERT)
    
    selecteur_res = Selecteur(
        400, 200, "Résolution:", 
        ['800x600', '1024x768', '1280x720', '1920x1080'], 
        gestionnaire_options.resolution
    )
    switch_plein_ecran = BoutonSwitch(400, 280, "Plein écran:", gestionnaire_options.plein_ecran)
    
    curseur_musique = Curseur(400, 220, 250, "Musique:", gestionnaire_options.volume_musique)
    curseur_effets = Curseur(400, 300, 250, "Effets:", gestionnaire_options.volume_effets)
    
    categorie = "systeme"
    
    while True:
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter", ecran
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retour.est_clique(pos):
                    ecran = gestionnaire_options.sauvegarder(
                        curseur_musique.valeur,
                        curseur_effets.valeur,
                        switch_plein_ecran.actif,
                        selecteur_res.obtenir_valeur()
                    )
                    pygame.mixer.music.set_volume(curseur_musique.valeur / 100)
                    return "menu", ecran
                
                if btn_systeme.est_clique(pos):
                    categorie = "systeme"
                    btn_systeme.couleur = BLEU
                    btn_son.couleur = GRIS
                
                if btn_son.est_clique(pos):
                    categorie = "son"
                    btn_systeme.couleur = GRIS
                    btn_son.couleur = BLEU
                
                if categorie == "systeme":
                    selecteur_res.clic(pos)
                    switch_plein_ecran.clic(pos)
            
            if categorie == "son":
                curseur_musique.gerer_clic(event, pos)
                curseur_effets.gerer_clic(event, pos)

                #Song update 
                pygame.mixer.music.set_volume(curseur_musique.valeur / 100)
        
        btn_systeme.verifier_survol(pos)
        btn_son.verifier_survol(pos)
        btn_retour.verifier_survol(pos)
        if categorie == "systeme":
            selecteur_res.verifier_survol(pos)
        
        ecran.fill(FOND)
        dessiner_titre(ecran, "OPTIONS", 40, BLANC)
        
        btn_systeme.dessiner(ecran)
        btn_son.dessiner(ecran)
        
        police = pygame.font.Font(None, 40)
        if categorie == "systeme":
            titre_cat = police.render("Fenêtre et Affichage", True, BLANC)
            ecran.blit(titre_cat, (80, 160))
            selecteur_res.dessiner(ecran)
            switch_plein_ecran.dessiner(ecran)
        else:
            titre_cat = police.render("Réglages Audio", True, BLANC)
            ecran.blit(titre_cat, (80, 160))
            curseur_musique.dessiner(ecran)
            curseur_effets.dessiner(ecran)
        
        btn_retour.dessiner(ecran)
        pygame.display.flip()
        horloge.tick(FPS)


#  MAIN 
def main():
    gestionnaire_options = GestionnaireOptions(ecran)
    page = "menu"
    ecran_actuel = ecran
    
    while True:
        if page == "menu":
            page, ecran_actuel = menu_principal(ecran_actuel, horloge, gestionnaire_options)
        elif page == "options":
            page, ecran_actuel = page_options(ecran_actuel, horloge, gestionnaire_options)
        elif page == "quitter":
            break
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
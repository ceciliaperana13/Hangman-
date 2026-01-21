import pygame
import random
import string
import os

pygame.init()
LARGEUR, HAUTEUR = 800, 600
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Mot")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (200, 0, 0)
VERT = (0, 200, 0)

# Police
font = pygame.font.Font(None, 40)
petite_font = pygame.font.Font(None, 30)

# Mots
mots = ["KIT"]

# ================= SCORE TEXTE AUTO =================

# Création automatique du fichier
if not os.path.exists("score.txt"):
    with open("score.txt", "w") as f:
        f.write("0\n0")

def charger_score():
    with open("score.txt", "r") as f:
        win = int(f.readline())
        lose = int(f.readline())
    return win, lose

def sauvegarder_score(win, lose):
    with open("score.txt", "w") as f:
        f.write(f"{win}\n{lose}")

# Charger score
win, lose = charger_score()
party = 0

# ===================================================

MAX_ERREURS = 6

def nouvelle_partie():
    return {
        "mot": random.choice(mots),
        "lettres_trouvees": set(),
        "lettres_ratees": set(),
        "chances": 0
    }

jeu = nouvelle_partie()

def afficher_texte(texte, x, y, couleur=BLANC):
    rendu = font.render(texte, True, couleur)
    ecran.blit(rendu, (x, y))

def afficher_score():
    afficher_texte(f"Win : {win}", 20, 20, VERT)
    afficher_texte(f"Lose : {lose}", 20, 60, ROUGE)
    afficher_texte(f"Party : {party}", 20, 100, BLANC)

def afficher_mot():
    affichage = ""
    for lettre in jeu["mot"]:
        if lettre in jeu["lettres_trouvees"]:
            affichage += lettre + " "
        else:
            affichage += "_ "
    afficher_texte(affichage, 200, 300)

def verifier_victoire():
    return all(l in jeu["lettres_trouvees"] for l in jeu["mot"])

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    ecran.fill(NOIR)

    afficher_score()
    afficher_mot()
    afficher_texte(f"Chances : {jeu['chances']} / {MAX_ERREURS}", 20, 150)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            lettre = event.unicode.upper()
            if lettre in string.ascii_uppercase:
                if lettre in jeu["mot"]:
                    jeu["lettres_trouvees"].add(lettre)
                else:
                    if lettre not in jeu["lettres_ratees"]:
                        jeu["lettres_ratees"].add(lettre)
                        jeu["chances"] += 1

    # VICTOIRE
    if verifier_victoire():
        afficher_texte("U WIN !", 300, 400, VERT)
        pygame.display.flip()
        pygame.time.delay(1500)
        win += 1
        party += 1
        sauvegarder_score(win, lose)
        jeu = nouvelle_partie()

    # DEFAITE
    if jeu["chances"] >= MAX_ERREURS:
        afficher_texte(f"U LOSE ! Mot : {jeu['mot']}", 250, 400, ROUGE)
        pygame.display.flip()
        pygame.time.delay(1500)
        lose += 1
        party += 1
        sauvegarder_score(win, lose)
        jeu = nouvelle_partie()

    pygame.display.flip()

pygame.quit()

import pygame
import os


score = []

if not os.path.exists("score.txt"):
    open("score.txt", "w").close()

def charger_historique():
    with open("score.txt", "r") as f:
        return [ligne.strip() for ligne in f if ligne.strip()]

def ajouter_historique(resultat):
    score.append(resultat)
    with open("score.txt", "a") as f:
        f.write(resultat + "\n")

score = charger_historique()


print("score au démarrage :", score)

ajouter_historique("WIN")
ajouter_historique("LOSE")
ajouter_historique("WIN")

print("score après ajout :", score)

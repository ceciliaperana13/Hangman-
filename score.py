import pygame
import os

scores = []

if not os.path.exists("score.txt"):
    open("score.txt", "w").close()

def load_history():
    with open("score.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def add_to_history(result):
    scores.append(result)
    with open("score.txt", "a") as f:
        f.write(result + "\n")

scores = load_history()

print("score at startup:", scores)

add_to_history("WIN")
add_to_history("LOSE")
add_to_history("WIN")

print("score after adding:", scores)
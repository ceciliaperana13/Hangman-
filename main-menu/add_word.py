import random



def add_word():
    new_word = input("Enter a new word to add: ").strip().upper()
    if new_word.isalpha():
        with open("easyWordList.txt", "a") as f:
            f.write(new_word + "\n")
        print(f"The word '{new_word}' has been added.")
    else:
        print("Invalid word. Please enter alphabetic characters only.")


def save_world():
    words = []
    try:
        with open("easyWordList.txt", "r") as f:
            words = [line.strip().upper() for line in f if line.strip().isalpha()]
    except FileNotFoundError:
        print("easyWordList.txt not found. Creating a new one.")

    with open("easyWordList.txt", "w") as f:
        for word in words:
            f.write(word + "\n")
    print("Words saved successfully.")

       
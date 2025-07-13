import random
import string
import os
import sys

if not os.path.isfile("sentences.txt"):
    print(f"Error: The file 'sentences.txt' does not exist.")
    sys.exit(1)

with open("sentences.txt", "r") as file:
    sentence_list = [line.strip() for line in file if line.strip()]

if not sentence_list:
    print(f"Error. The file 'sentences.txt' is empty. Please add some sentences to play.")
    sys.exit(1)

def display_word(secret_sentence, guessed_letters):
    displayed = ''
    for letter in secret_sentence:
        if not letter.isalpha() or letter.lower() in guessed_letters:
            displayed += letter + ' '
        else:
            displayed += '_ '
    return displayed.strip()

def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())
    return text

def main():
    secret_sentence = random.choice(sentence_list)
    normalized_secret = normalize_text(secret_sentence)

    guessed_letters = set()
    wrong_guesses = 0
    max_wrong_guesses = 5

    print("Let's play Hangman!")
    print(f"Guess the word one letter at a time, or try to guess the entire sentence!")
    print(f"You have {max_wrong_guesses} wrong guesses allowed.")
    print(display_word(secret_sentence, guessed_letters))

    while wrong_guesses < max_wrong_guesses:
        guess = input("Guess a letter (or the full sentence): ").strip()

        if len(guess) > 1:
            if normalize_text(guess) == normalized_secret:
                print(f"Congratulations! You guessed the entire sentence: {secret_sentence}")
                break
            else:
                wrong_guesses += 1
                attempts_left = max_wrong_guesses - wrong_guesses
                print(f"Wrong guess for the full sentence! Attempts left: {attempts_left}")
                print(display_word(secret_sentence, guessed_letters))
                continue

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single letter or guess the full sentence.")
            continue

        guess = guess.lower()

        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try another letter.")
            continue

        guessed_letters.add(guess)

        if guess in secret_sentence.lower():
            print("Good guess!")
        else:
            wrong_guesses += 1
            attempts_left = max_wrong_guesses - wrong_guesses
            print(f"Wrong guess! Attempts left: {attempts_left}")

        print(display_word(secret_sentence, guessed_letters))
        print("Guessed letters:", ' '.join(letter.upper() for letter in sorted(guessed_letters)))

        if all(letter.lower() in guessed_letters or not letter.isalpha() for letter in secret_sentence):
            print(f"Congratulations! You guessed the word: {secret_sentence}")
            break
    else:
        print(f"Game over! The word was '{secret_sentence}'.")

if __name__ == '__main__':
    while True:
        main()
        again = input("Would you like to play again? (y/n): ").lower()
        if again != 'y':
            print("Thanks for playing!")
            break

import random
import string
import os
import sys
import tkinter as tk
from tkinter import messagebox

if not os.path.isfile("sentences.txt"):
    messagebox.showerror("Error", "The file 'sentences.txt' does not exist.")
    sys.exit(1)

with open("sentences.txt", "r") as file:
    sentence_list = [line.strip() for line in file if line.strip()]

if not sentence_list:
    messagebox.showerror("Error", "The file 'sentences.txt' is empty. Please add some sentences to play.")
    sys.exit(1)

def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())
    return text

def display_word(secret_sentence, guessed_letters):
    displayed = ''
    for letter in secret_sentence:
        if not letter.isalpha() or letter.lower() in guessed_letters:
            displayed += letter + ' '
        else:
            displayed += '_ '
    return displayed.strip()

class HangmanGUI:
    def __init__(self, master):
        self.master = master
        master.title("Hangman Game")

        self.max_wrong_guesses = 5
        self.start_new_game()

        self.sentence_label = tk.Label(master, text=self.displayed_sentence, font=("Consolas", 20))
        self.sentence_label.pack(pady=10)

        self.guessed_label = tk.Label(master, text="Guessed letters: ", font=("Arial", 12))
        self.guessed_label.pack()

        self.attempts_label = tk.Label(master, text=f"Attempts left: {self.max_wrong_guesses}", font=("Arial", 12))
        self.attempts_label.pack(pady=5)

        self.guess_entry = tk.Entry(master, font=("Arial", 14))
        self.guess_entry.pack(pady=5)
        self.guess_entry.focus()

        self.guess_button = tk.Button(master, text="Guess", command=self.process_guess)
        self.guess_button.pack(pady=5)

        self.restart_button = tk.Button(master, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(pady=10)

    def start_new_game(self):
        self.secret_sentence = random.choice(sentence_list)
        self.normalized_secret = normalize_text(self.secret_sentence)
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.displayed_sentence = display_word(self.secret_sentence, self.guessed_letters)

    def update_display(self):
        self.displayed_sentence = display_word(self.secret_sentence, self.guessed_letters)
        self.sentence_label.config(text=self.displayed_sentence)
        guessed_letters_str = ' '.join(letter.upper() for letter in sorted(self.guessed_letters))
        self.guessed_label.config(text=f"Guessed letters: {guessed_letters_str}")
        attempts_left = self.max_wrong_guesses - self.wrong_guesses
        self.attempts_label.config(text=f"Attempts left: {attempts_left}")

    def process_guess(self):
        guess = self.guess_entry.get().strip()
        self.guess_entry.delete(0, tk.END)

        if not guess:
            messagebox.showinfo("Input Error", "Please enter a guess.")
            return

        if len(guess) > 1:
            if normalize_text(guess) == self.normalized_secret:
                self.displayed_sentence = self.secret_sentence
                self.update_display()
                messagebox.showinfo("Congratulations!", f"You guessed the entire sentence:\n{self.secret_sentence}")
                self.disable_game()
            else:
                self.wrong_guesses += 1
                self.update_display()
                if self.wrong_guesses >= self.max_wrong_guesses:
                    messagebox.showinfo("Game Over", f"Wrong guess! No attempts left.\nThe sentence was:\n{self.secret_sentence}")
                    self.disable_game()
                else:
                    messagebox.showinfo("Wrong Guess", f"Wrong guess for the full sentence! Attempts left: {self.max_wrong_guesses - self.wrong_guesses}")
            return

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showinfo("Input Error", "Invalid input. Please enter a single letter or guess the full sentence.")
            return

        guess = guess.lower()

        if guess in self.guessed_letters:
            messagebox.showinfo("Already Guessed", f"You already guessed '{guess}'. Try another letter.")
            return

        self.guessed_letters.add(guess)

        if guess in self.secret_sentence.lower():
            messagebox.showinfo("Good Guess!", f"'{guess.upper()}' is in the sentence!")
        else:
            self.wrong_guesses += 1
            if self.wrong_guesses >= self.max_wrong_guesses:
                self.update_display()
                messagebox.showinfo("Game Over", f"Wrong guess! No attempts left.\nThe sentence was:\n{self.secret_sentence}")
                self.disable_game()
                return
            else:
                messagebox.showinfo("Wrong Guess", f"'{guess.upper()}' is not in the sentence! Attempts left: {self.max_wrong_guesses - self.wrong_guesses}")

        self.update_display()

        if all(letter.lower() in self.guessed_letters or not letter.isalpha() for letter in self.secret_sentence):
            messagebox.showinfo("Congratulations!", f"You guessed the sentence:\n{self.secret_sentence}")
            self.disable_game()

    def disable_game(self):
        self.guess_entry.config(state='disabled')
        self.guess_button.config(state='disabled')

    def restart_game(self):
        self.start_new_game()
        self.guess_entry.config(state='normal')
        self.guess_button.config(state='normal')
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGUI(root)
    root.mainloop()

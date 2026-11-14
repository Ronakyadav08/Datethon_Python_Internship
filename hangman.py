"""
Hangman Word Guessing Game (Console)

- Picks a random secret word
- Player guesses one letter at a time (6 wrong attempts allowed)
- ASCII gallows art updates with each wrong guess
- Tracks guessed letters and does not penalise duplicate guesses
"""

import os
import random

MAX_MISTAKES = 6
WORDS_FILE = "google-10000-english-no-swears.txt"  # downloaded English words list

# 7 stages: index = number of wrong guesses (0 to 6)
HANGMAN_STAGES = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========
    """,
]


def load_words():
    """Load words from the words file (same folder as this script)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), WORDS_FILE)
    if not os.path.exists(path):
        raise SystemExit(f"Error: '{WORDS_FILE}' not found. "
                         "Put it in the same folder as hangman.py.")
    with open(path, "r") as f:
        words = [w.lower() for w in f.read().split()
                 if w.isalpha() and len(w) >= 4]
    if not words:
        raise SystemExit(f"Error: no usable words found in '{WORDS_FILE}'.")
    return words


def choose_word(words):
    """Pick a random secret word."""
    return random.choice(words).lower()


def get_masked_word(secret, guessed):
    """Return the word with unguessed letters hidden, e.g. '_ A _ H E O N'."""
    return " ".join(ch.upper() if ch in guessed else "_" for ch in secret)


def display_board(secret, guessed, mistakes):
    """Print the gallows, masked word, and guessed letters."""
    print(HANGMAN_STAGES[mistakes])
    print("Word:", get_masked_word(secret, guessed))
    print(f"Mistakes: {mistakes}/{MAX_MISTAKES}")
    if guessed:
        print("Guessed letters:", " ".join(sorted(guessed)).upper())
    print()


def get_guess(guessed):
    """Ask for a valid single new letter. Duplicates are rejected without penalty."""
    while True:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (A-Z).")
        elif guess in guessed:
            print(f"You already guessed '{guess.upper()}'. Try a different letter.")
        else:
            return guess


def show_victory(secret):
    print("=" * 40)
    print("   CONGRATULATIONS! YOU WON!")
    print(f"   The word was: {secret.upper()}")
    print("=" * 40)


def show_defeat(secret):
    print(HANGMAN_STAGES[MAX_MISTAKES])
    print("=" * 40)
    print("   GAME OVER! YOU LOST!")
    print(f"   The word was: {secret.upper()}")
    print("=" * 40)


def play_game(words):
    """Run one round of Hangman."""
    secret = choose_word(words)
    guessed = set()
    mistakes = 0

    print("\nWelcome to HANGMAN!")
    print(f"The word has {len(secret)} letters. You get {MAX_MISTAKES} wrong guesses.")

    while mistakes < MAX_MISTAKES:
        display_board(secret, guessed, mistakes)

        guess = get_guess(guessed)
        guessed.add(guess)

        if guess in secret:
            print(f"Good job! '{guess.upper()}' is in the word.")
        else:
            mistakes += 1
            print(f"Sorry, '{guess.upper()}' is not in the word.")

        # Win check: every letter of the secret has been guessed
        if all(ch in guessed for ch in secret):
            display_board(secret, guessed, mistakes)
            show_victory(secret)
            return

    show_defeat(secret)


def main():
    words = load_words()
    while True:
        play_game(words)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing. Goodbye!")
            break


if __name__ == "__main__":
    main()
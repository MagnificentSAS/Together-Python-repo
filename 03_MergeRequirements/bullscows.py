import random

def bullcows(guess: str, mystery: str) -> (int, int):
    bulls = set()
    cows = set()
    for a, b in zip(guess, mystery):
        if a == b:
            bulls.add(a)

        if a in mystery:
            cows.add(a)

    cows = cows - bulls

    return len(bulls), len(cows)

def gameplay(ask, inform, words: list[str]) -> int:
    mystery = random.choice(words)
    attempt = 0

    while True:
        guess = ask("Введите слово: ", words)
        attempt += 1
        b, c = bullcows(guess, mystery)
        inform("Быки: {}, Коровы: {}", b, c)
        if guess == mystery:
            return attempt

def ask(prompt: str, valid: list[str] = None) -> str:
    word = input(prompt)
    while valid and word not in valid:
        word = input(prompt)
    return word

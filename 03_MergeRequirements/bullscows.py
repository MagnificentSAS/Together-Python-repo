#!/usr/bin/env python3
import argparse
import os
import random
import sys
import urllib.request

from cowsay import cowsay

def bullcows(guess: str, mystery: str) -> tuple[int, int]:
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
    print(cowsay(prompt))
    word = sys.stdin.buffer.readline().decode('utf-8', errors='ignore').strip()
    while valid and word not in valid:
        print(cowsay(prompt))
        word = sys.stdin.buffer.readline().decode('utf-8', errors='ignore').strip()
    return word

def inform(format_string: str, bulls: int, cows: int) -> None:
    words = format_string.split("{}")
    print(cowsay(f"{words[0]}{bulls}{words[1]}{cows}{words[2]}"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Сыграйте в быков и коров от al_bonch!")
    parser.add_argument("dict", help="Словарь")
    parser.add_argument("length", nargs="?", type=int, default=5, help="Длина слов (по умолчанию 5)")
    args = parser.parse_args()

    if os.path.exists(args.dict):
        with open(args.dict, 'r', encoding='utf-8') as f:
            words = f.read().splitlines()
    else: # args.dict.startswith(("http://", "https://", "ftp://")):
        print("Загрузка слов!")
        with urllib.request.urlopen(args.dict) as r:
            words = r.read().decode('utf-8').splitlines()
        print("Загрузка завершена")
    #else:
     #   print("Нет такого файла и ссылка не верна")
      #  exit(1)

    game_dict = [w for w in words if len(w) == args.length]
    if len(game_dict) == 0:
        print("Пустой словарь :(")
        exit(1)

    print("Вы выиграли, отгадав за ", gameplay(ask, inform, game_dict), " попыток!")

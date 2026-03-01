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

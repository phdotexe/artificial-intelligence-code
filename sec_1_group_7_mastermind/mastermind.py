import itertools
from enum import Enum
from typing import Sequence


class Color(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    ORANGE = 5
    PURPLE = 6


def knuth_mastermind_algo(code_to_guess: list[Color]):
    set_all_code = list(itertools.product(Color, repeat=len(code_to_guess)))

    set_pruned_code = set_all_code.copy()
    current_guess = [Color.RED, Color.RED, Color.YELLOW, Color.YELLOW]

    attempts = 0

    while attempts < 8:
        attempts += 1

        score = scoring(current_guess, code_to_guess)

        print(
            f"Guess: {current_guess}, Score: {score[0]} black keys, {score[1]} white keys\n"
        )

        if score == (4, 0):
            winner = [color.name for color in current_guess]
            print("YOU WON")
            print(f"the code was: {winner}")
            return

        set_pruned_code = [
            c for c in set_pruned_code if scoring(current_guess, c) == score
        ]

        current_guess = minimax(set_pruned_code, set_all_code)

    print("Game over: you couldn't guess it")


def minimax(pruned_code: list[tuple[Color, ...]], all_code: list[tuple[Color, ...]]):
    best_guess = all_code[0]
    min_max_score = float("inf")

    for candidate in all_code:
        score_counter = {}

        for s in pruned_code:
            score = scoring(candidate, s)
            score_counter[score] = score_counter.get(score, 0) + 1

        worst_case = max(score_counter.values())

        if worst_case < min_max_score:
            min_max_score = worst_case
            best_guess = candidate

        elif worst_case == min_max_score:
            if candidate in pruned_code and best_guess not in pruned_code:
                best_guess = candidate

    return best_guess


def scoring(attempt: Sequence[Color], code: Sequence[Color]) -> tuple:
    black = sum(a == c for a, c in zip(attempt, code))
    white = sum(min(attempt.count(c), code.count(c)) for c in set(code)) - black
    return black, white


knuth_mastermind_algo([Color.GREEN, Color.YELLOW, Color.YELLOW, Color.RED])

from itertools import product
from typing import Dict, List, Tuple

NUM_POSITIONS = 4
COLORS = ["R", "G", "B", "Y", "O", "P"]


def generate_all_feedbacks() -> List[Tuple[int, int]]:
    feedbacks = []
    for black in range(NUM_POSITIONS + 1):
        for white in range(NUM_POSITIONS + 1 - black):
            if black + white <= NUM_POSITIONS:
                if not (black == NUM_POSITIONS - 1 and white == 1):
                    feedbacks.append((black, white))
    return feedbacks


ALL_FEEDBACKS = generate_all_feedbacks()


def calculate_feedback(
    guess: Tuple[str, ...], secret: Tuple[str, ...]
) -> Tuple[int, int]:
    black_pegs = 0
    guess_remaining = []
    secret_remaining = []

    for g, s in zip(guess, secret):
        if g == s:
            black_pegs += 1
        else:
            guess_remaining.append(g)
            secret_remaining.append(s)
    white_pegs = 0
    for g in guess_remaining:
        if g in secret_remaining:
            white_pegs += 1
            secret_remaining.remove(g)

    return (black_pegs, white_pegs)


def generate_all_codes() -> List[Tuple[str, ...]]:
    return list(product(COLORS, repeat=NUM_POSITIONS))


def partition_by_feedback(
    guess: Tuple[str, ...], possible_codes: List[Tuple[str, ...]]
) -> Dict[Tuple[int, int], List[Tuple[str, ...]]]:

    partitions: Dict[Tuple[int, int], List[Tuple[str, ...]]] = {}

    for code in possible_codes:
        feedback = calculate_feedback(guess, code)
        if feedback not in partitions:
            partitions[feedback] = []
        partitions[feedback].append(code)

    return partitions


def minimax_score(
    guess: Tuple[str, ...],
    possible_codes: List[Tuple[str, ...]],
    depth: int,
    max_depth: int,
    memo: Dict,
) -> int:
    partitions = partition_by_feedback(guess, possible_codes)

    worst_case = 0

    for feedback, codes_subset in partitions.items():
        if feedback == (NUM_POSITIONS, 0):
            branch_score = 1
        elif len(codes_subset) == 1:
            branch_score = 2
        elif depth >= max_depth:
            branch_score = 1 + estimate_guesses_needed(len(codes_subset))
        else:
            sub_key = tuple(sorted(codes_subset))
            if sub_key in memo:
                branch_score = 1 + memo[sub_key]
            else:
                best_sub_score = recursive_find_best_score(
                    codes_subset, depth + 1, max_depth, memo
                )
                memo[sub_key] = best_sub_score
                branch_score = 1 + best_sub_score

        worst_case = max(worst_case, branch_score)

    return worst_case


def estimate_guesses_needed(n: int) -> int:
    if n <= 1:
        return 1
    elif n <= 6:
        return 2
    elif n <= 20:
        return 3
    elif n <= 100:
        return 4
    else:
        return 5


def recursive_find_best_score(
    possible_codes: List[Tuple[str, ...]], depth: int, max_depth: int, memo: Dict
) -> int:
    if len(possible_codes) == 1:
        return 1

    if len(possible_codes) == 2:
        return 2

    best_score = float("inf")

    candidates = possible_codes if len(possible_codes) <= 50 else possible_codes[:50]

    for guess in candidates:
        score = minimax_score(guess, possible_codes, depth, max_depth, memo)
        best_score = min(best_score, score)

        if score <= 2:
            break

    return best_score  # type: ignore


def choose_best_guess_recursive(
    possible_codes: List[Tuple[str, ...]],
    all_codes: List[Tuple[str, ...]],
    is_first_guess: bool = False,
    max_depth: int = 5,
) -> Tuple[str, ...]:
    if is_first_guess:
        return (COLORS[0], COLORS[0], COLORS[1], COLORS[1])

    if len(possible_codes) == 1:
        return possible_codes[0]

    if len(possible_codes) == 2:
        return possible_codes[0]

    memo: Dict = {}
    best_guess = possible_codes[0]
    best_score = float("inf")

    candidates = possible_codes
    if len(possible_codes) > 10:
        for code in all_codes[:20]:
            if code not in candidates:
                candidates = candidates + [code]

    for guess in candidates:
        score = minimax_score(guess, possible_codes, 0, max_depth, memo)

        if score < best_score:
            best_score = score
            best_guess = guess
        if score == 1:
            break

    return best_guess


def filter_by_feedback(
    possible_codes: List[Tuple[str, ...]],
    guess: Tuple[str, ...],
    feedback: Tuple[int, int],
) -> List[Tuple[str, ...]]:
    return [
        code for code in possible_codes if calculate_feedback(guess, code) == feedback
    ]


def solve_recursive_minimax(
    secret: Tuple[str, ...],
    possible_codes: List[Tuple[str, ...]],
    all_codes: List[Tuple[str, ...]],
    guess_number: int = 1,
    max_guesses: int = 10,
    verbose: bool = True,
) -> Tuple[bool, int, List[Tuple[Tuple[str, ...], Tuple[int, int]]]]:
    if not possible_codes:
        if verbose:
            print("Error: No possible codes remain!")
        return (False, guess_number - 1, [])

    # Base case: exceeded guess limit
    if guess_number > max_guesses:
        if verbose:
            print(f"Failed: Exceeded {max_guesses} guesses")
        return (False, guess_number - 1, [])

    # Choose best guess using recursive minimax
    is_first = guess_number == 1
    guess = choose_best_guess_recursive(possible_codes, all_codes, is_first)

    # Get feedback
    feedback = calculate_feedback(guess, secret)
    black_pegs, white_pegs = feedback

    if verbose:
        print(f"Guess {guess_number}: {guess}")
        print(f"  Feedback: {black_pegs} black, {white_pegs} white")
        print(f"  Possibilities before: {len(possible_codes)}")

    # Base case: found the secret!
    if black_pegs == NUM_POSITIONS:
        if verbose:
            print(f"\n*** Solved! Found {secret} in {guess_number} guesses ***")
        return (True, guess_number, [(guess, feedback)])

    # Recursive case: filter and continue
    remaining = filter_by_feedback(possible_codes, guess, feedback)

    if verbose:
        print(f"  Possibilities after: {len(remaining)}")
        if len(remaining) <= 6:
            print(f"  Remaining: {remaining}")
        print()

    # Recurse with reduced problem
    success, total, history = solve_recursive_minimax(
        secret, remaining, all_codes, guess_number + 1, max_guesses, verbose
    )

    return (success, total, [(guess, feedback)] + history)


def solve_mastermind(
    secret: Tuple[str, ...], verbose: bool = True
) -> Tuple[bool, int, List[Tuple[Tuple[str, ...], Tuple[int, int]]]]:
    """
    Main entry point for the Mastermind solver.

    Args:
        secret: The secret code to find
        verbose: Whether to print progress

    Returns:
        (success, num_guesses, history) tuple
    """
    all_codes = generate_all_codes()

    if verbose:
        print("=" * 50)
        print("MASTERMIND SOLVER - Recursive Minimax Algorithm")
        print("=" * 50)
        print(f"Secret: {secret}")
        print(f"Colors: {COLORS}")
        print(f"Positions: {NUM_POSITIONS}")
        print(f"Total codes: {len(all_codes)}")
        print("=" * 50)
        print()

    return solve_recursive_minimax(secret, all_codes, all_codes, verbose=verbose)


def demonstrate_minimax_recursion(verbose: bool = True):
    """
    Demonstrate how the recursive minimax works by showing the decision process.
    """
    if verbose:
        print("\n" + "=" * 60)
        print("DEMONSTRATION: Recursive Minimax Decision Process")
        print("=" * 60)
        print()
        print("The minimax algorithm works by recursively asking:")
        print("'If I make this guess, what's the WORST case outcome?'")
        print()
        print("For each guess, it:")
        print("1. Partitions possible codes by feedback they'd produce")
        print("2. For each partition, RECURSIVELY evaluates the subproblem")
        print("3. Takes the MAX (worst case) across all partitions")
        print("4. Chooses the guess that MINIMIZES this maximum")
        print()

    # Small example
    example_codes = [
        ("R", "R", "G", "G"),
        ("R", "G", "R", "G"),
        ("R", "G", "G", "R"),
        ("G", "R", "R", "G"),
    ]

    if verbose:
        print(f"Example with {len(example_codes)} possible codes:")
        for code in example_codes:
            print(f"  {code}")
        print()

    # Show partitioning for one guess
    test_guess = ("R", "R", "G", "G")
    partitions = partition_by_feedback(test_guess, example_codes)

    if verbose:
        print(f"If we guess {test_guess}, partitions by feedback:")
        for feedback, codes in partitions.items():
            print(f"  Feedback {feedback}: {codes}")
        print()
        print("The minimax algorithm recursively evaluates each partition")
        print("to determine the total guesses needed in the worst case.")
        print()


# Main execution
if __name__ == "__main__":
    import random

    print("=" * 60)
    print("MASTERMIND - RECURSIVE MINIMAX SOLVER")
    print("=" * 60)

    # Demonstrate the concept
    demonstrate_minimax_recursion()

    # Test cases
    test_secrets = [
        ("R", "G", "B", "Y"),
        ("R", "R", "G", "G"),
        ("P", "O", "Y", "B"),
        ("B", "B", "B", "B"),
    ]

    results = []

    for secret in test_secrets:
        print("\n" + "-" * 60 + "\n")
        success, guesses, history = solve_mastermind(secret)
        results.append((secret, success, guesses))

    # Summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    for secret, success, guesses in results:
        status = "SOLVED" if success else "FAILED"
        print(f"{secret}: {status} in {guesses} guesses")

    avg_guesses = sum(g for _, _, g in results) / len(results)
    print(f"\nAverage: {avg_guesses:.2f} guesses")

    # Random test
    print("\n" + "=" * 60)
    print("RANDOM SECRET TEST")
    print("=" * 60 + "\n")

    random_secret = tuple(random.choices(COLORS, k=NUM_POSITIONS))
    solve_mastermind(random_secret)

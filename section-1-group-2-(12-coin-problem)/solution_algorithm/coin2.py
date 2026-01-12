from enum import Enum

class Result(Enum):
    LEFT_HEAVY = 1
    RIGHT_HEAVY = -1
    BALANCE = 0

_weighing_counter = [0]  # Use list to allow modification in nested scopes

def weigh(left, right, weights, weighing_num=None):
    """
    left, right: lists of coin names (strings)
    weights: dict {coin: weight}
    """
    if weighing_num is None:
        _weighing_counter[0] += 1
        weighing_num = _weighing_counter[0]
    
    lw = sum(weights[c] for c in left)
    rw = sum(weights[c] for c in right)
    
    print(f"\nWeighing {weighing_num}:")
    print(f"  Left side:  {left}  (total weight: {lw})")
    print(f"  Right side: {right} (total weight: {rw})")

    if lw > rw:
        result = Result.LEFT_HEAVY
        print(f"  Result: LEFT HEAVY (left side is heavier)")
    elif lw < rw:
        result = Result.RIGHT_HEAVY
        print(f"  Result: RIGHT HEAVY (right side is heavier)")
    else:
        result = Result.BALANCE
        print(f"  Result: BALANCE (both sides equal)")
    
    return result

def solve(weights):
    _weighing_counter[0] = 0  # Reset counter at start of solve
    print("=" * 60)
    print("Starting to solve the 12-coin problem...")
    print("=" * 60)
    
    def result(coin, direction):
        """Helper function to print and return the result"""
        print("\n" + "=" * 60)
        print(f"SOLUTION FOUND: Coin {coin} is {direction}")
        print("=" * 60)
        return (coin, direction)
    
    # WEIGHING 1
    W1 = weigh(
        ["A1","A2","A3","A4"],
        ["B1","B2","B3","B4"],
        weights
    )

    # -------------------------
    # CASE 1: W1 == BALANCE
    # -------------------------
    if W1 == Result.BALANCE:

        W2 = weigh(
            ["C1","C2","C3"],
            ["A1","A2","A3"],
            weights
        )

        # C4 case
        if W2 == Result.BALANCE:
            W3 = weigh(["C4"], ["A1"], weights)
            return result("C4", "heavier" if W3 == Result.LEFT_HEAVY else "lighter")

        # C1/C2/C3 heavy
        if W2 == Result.LEFT_HEAVY:
            W3 = weigh(["C1"], ["C2"], weights)
            if W3 == Result.LEFT_HEAVY:
                return result("C1", "heavier")
            elif W3 == Result.RIGHT_HEAVY:
                return result("C2", "heavier")
            else:
                return result("C3", "heavier")

        # C1/C2/C3 light
        if W2 == Result.RIGHT_HEAVY:
            W3 = weigh(["C1"], ["C2"], weights)
            if W3 == Result.LEFT_HEAVY:
                return result("C2", "lighter")
            elif W3 == Result.RIGHT_HEAVY:
                return result("C1", "lighter")
            else:
                return result("C3", "lighter")

    # -------------------------
    # CASE 2: W1 == LEFT_HEAVY
    # -------------------------
    if W1 == Result.LEFT_HEAVY:

        W2 = weigh(
            ["A3","B1","B2","B4"],
            ["C1","C2","B3","C4"],
            weights
        )

        # A1/A2/A4 heavy
        if W2 == Result.BALANCE:
            W3 = weigh(["A1"], ["A2"], weights)
            if W3 == Result.LEFT_HEAVY:
                return result("A1", "heavier")
            elif W3 == Result.RIGHT_HEAVY:
                return result("A2", "heavier")
            else:
                return result("A4", "heavier")

        # A3 heavy OR B3/C4 light
        if W2 == Result.LEFT_HEAVY:
            W3 = weigh(["B3"], ["C4"], weights)
            if W3 == Result.LEFT_HEAVY:
                return result("C4", "lighter")
            elif W3 == Result.RIGHT_HEAVY:
                return result("B3", "lighter")
            else:
                return result("A3", "heavier")

        # B1/B2/B4 light
        if W2 == Result.RIGHT_HEAVY:
            W3 = weigh(["B1"], ["B2"], weights)
            if W3 == Result.LEFT_HEAVY:
                return result("B2", "lighter")
            elif W3 == Result.RIGHT_HEAVY:
                return result("B1", "lighter")
            else:
                return result("B4", "lighter")

    # -------------------------
    # CASE 3: W1 == RIGHT_HEAVY
    # -------------------------
    if W1 == Result.RIGHT_HEAVY:

        W2 = weigh(
            ["B3","A1","A2","A4"],
            ["C1","C2","A3","C4"],
            weights
        )

        # B1/B2/B4 heavy
        if W2 == Result.BALANCE:
            W3 = weigh(["B1"], ["B2"], weights)
            if W3 == Result.LEFT_HEAVY:
                return result("B1", "heavier")
            elif W3 == Result.RIGHT_HEAVY:
                return result("B2", "heavier")
            else:
                return result("B4", "heavier")

        # B3 heavy OR A3/C4 light
        if W2 == Result.LEFT_HEAVY:
            W3 = weigh(["A3"], ["C4"], weights)
            if W3 == Result.LEFT_HEAVY:
                return result("C4", "lighter")
            elif W3 == Result.RIGHT_HEAVY:
                return result("A3", "lighter")
            else:
                return result("B3", "heavier")

        # A1/A2/A4 light
        if W2 == Result.RIGHT_HEAVY:
            W3 = weigh(["A1"], ["A2"], weights)
            if W3 == Result.LEFT_HEAVY:
                return result("A2", "lighter")
            elif W3 == Result.RIGHT_HEAVY:
                return result("A1", "lighter")
            else:
                return result("A4", "lighter")


# ---- Testing (optional) ----
# generate_test(...)
# def generate_test(fake_coin, direction):
#     weights = {}
#     for group in ["A","B","C"]:
#         for i in range(1,5):
#             weights[f"{group}{i}"] = 10

#     weights[fake_coin] += 1 if direction == "heavier" else -1
#     return weights

# # example runs
# weights = generate_test("A3", "heavier")
# print(solve(weights))
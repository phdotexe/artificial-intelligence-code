def ask(n):
    while True:
        r = input(f"Weighing {n} result (L = left heavy, R = right heavy, B = balanced): ").upper()
        if r in ("L","R","B"):
            return r
        print("Invalid input. Enter L, R, or B.")


print("12 Coin Problem Solver")
print("Coins: A B C D E F G H I J K L\n")

print("Weigh 1: A B C D  vs  E F G H")
w1 = ask(1)

# ================= CASE 1 =================
# FIRST WEIGH BALANCED → counterfeit in I,J,K,L
if w1 == "B":
    print("\nCounterfeit is among I J K L")

    print("Weigh 2: I J K  vs  A B C")
    w2 = ask(2)

    if w2 == "B":
        print("\nCounterfeit is L")
        print("Weigh 3: L vs A")
        w3 = ask(3)
        if w3 == "L":
            print("Result: L is HEAVIER")
        else:
            print("Result: L is LIGHTER")

    elif w2 == "L":
        print("\nWeigh 3: I vs J")
        w3 = ask(3)
        if w3 == "B":
            print("Result: K is LIGHTER")
        elif w3 == "L":
            print("Result: I is HEAVIER")
        else:
            print("Result: J is HEAVIER")

    else:  # w2 == R
        print("\nWeigh 3: I vs J")
        w3 = ask(3)
        if w3 == "B":
            print("Result: K is HEAVIER")
        elif w3 == "L":
            print("Result: J is LIGHTER")
        else:
            print("Result: I is LIGHTER")

# ================= CASE 2 =================
# FIRST WEIGH NOT BALANCED
else:
    left_heavy = (w1 == "L")
    print("\nCounterfeit is among A B C D E F G H")

    print("Weigh 2: A B E  vs  C D F")
    w2 = ask(2)

    # ---------- W2 BALANCED ----------
    if w2 == "B":
        print("\nCounterfeit is G or H")
        print("Weigh 3: G vs A")
        w3 = ask(3)

        if left_heavy:   # left was heavy in weigh 1
            if w3 == "B":
                print("Result: H is LIGHTER")
            elif w3 == "L":
                print("Result: G is HEAVIER (impossible in this branch) – check inputs")
            else:
                print("Result: G is LIGHTER")
        else:  # right heavy in weigh1
            if w3 == "B":
                print("Result: H is HEAVIER")
            elif w3 == "L":
                print("Result: G is HEAVIER")
            else:
                print("Result: G is LIGHTER (impossible in this branch) – check inputs")

    # ---------- W2 SAME DIRECTION AS W1 ----------
    elif (w2 == "L" and left_heavy) or (w2 == "R" and not left_heavy):
        print("\nSuspects are:")
        if left_heavy:
            print("A (heavy), B (heavy), or F (light)")
        else:
            print("A (light), B (light), or F (heavy)")

        print("Weigh 3: A vs B")
        w3 = ask(3)

        if w3 == "B":
            if left_heavy:
                print("Result: F is LIGHTER")
            else:
                print("Result: F is HEAVIER")

        elif w3 == "L":
            if left_heavy:
                print("Result: A is HEAVIER")
            else:
                print("Result: B is LIGHTER")

        else:  # R
            if left_heavy:
                print("Result: B is HEAVIER")
            else:
                print("Result: A is LIGHTER")

    # ---------- W2 OPPOSITE DIRECTION ----------
    else:
        print("\nSuspects are:")
        if left_heavy:
            print("C (heavy), D (heavy), or E (light)")
        else:
            print("C (light), D (light), or E (heavy)")

        print("Weigh 3: C vs D")
        w3 = ask(3)

        if w3 == "B":
            if left_heavy:
                print("Result: E is LIGHTER")
            else:
                print("Result: E is HEAVIER")

        elif w3 == "L":
            if left_heavy:
                print("Result: C is HEAVIER")
            else:
                print("Result: D is LIGHTER")

        else:  # R
            if left_heavy:
                print("Result: D is HEAVIER")
            else:
                print("Result: C is LIGHTER")

# Algorithm 2: Brute Force Nash Equilibrium Search

payoffs = {
    ('C', 'C'): (2, 2),
    ('C', 'D'): (0, 3),
    ('D', 'C'): (3, 0),
    ('D', 'D'): (1, 1)
}

strategies = ['C', 'D']

for a in strategies:
    for b in strategies:
        pa, pb = payoffs[(a, b)]

        better_for_a = any(payoffs[(alt, b)][0] > pa for alt in strategies)
        better_for_b = any(payoffs[(a, alt)][1] > pb for alt in strategies)

        if not better_for_a and not better_for_b:
            print("Nash Equilibrium:", (a, b))

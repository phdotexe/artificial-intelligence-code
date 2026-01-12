# Algorithm 1: Dominant Strategy Check

payoffs = {
    ('C', 'C'): (2, 2),
    ('C', 'D'): (0, 3),
    ('D', 'C'): (3, 0),
    ('D', 'D'): (1, 1)
}

# Check Player A
if payoffs[('D', 'C')][0] > payoffs[('C', 'C')][0] and \
   payoffs[('D', 'D')][0] > payoffs[('C', 'D')][0]:
    dominant_A = 'D'

# Check Player B
if payoffs[('C', 'D')][1] > payoffs[('C', 'C')][1] and \
   payoffs[('D', 'D')][1] > payoffs[('D', 'C')][1]:
    dominant_B = 'D'

print("Dominant Strategy Outcome:", (dominant_A, dominant_B))

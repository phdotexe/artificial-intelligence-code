import matplotlib.pyplot as plt
import time

choices = [('C', 'C'), ('C', 'D'), ('D', 'C'), ('D', 'D')]

payoffs = {
    ('C', 'C'): (2, 2),
    ('C', 'D'): (0, 3),
    ('D', 'C'): (3, 0),
    ('D', 'D'): (1, 1)
}

colors = {
    'C': 'green',   # Cooperation
    'D': 'red'      # Defection
}

plt.ion()

rounds = 3  # number of times the animation repeats

for _ in range(rounds):
    for choice in choices:
        plt.clf()
        a, b = choice
        pa, pb = payoffs[choice]

        plt.text(0.1, 0.6,
                 f"Player A: {a} (Payoff {pa})",
                 fontsize=14,
                 color=colors[a])

        plt.text(0.1, 0.4,
                 f"Player B: {b} (Payoff {pb})",
                 fontsize=14,
                 color=colors[b])

        plt.title("Prisoner's Dilemma Simulation", fontsize=16)
        plt.text(0.1, 0.2, "Green = Cooperate | Red = Defect", fontsize=10)

        plt.axis('off')
        plt.pause(1.5)

plt.ioff()
plt.show()

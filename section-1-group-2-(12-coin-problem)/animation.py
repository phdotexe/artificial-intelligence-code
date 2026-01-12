import matplotlib.pyplot as plt
import matplotlib.animation as animation
from enum import Enum

class Result(Enum):
    LEFT_HEAVY = 1
    RIGHT_HEAVY = -1
    BALANCE = 0

# --- Balance Beam Setup ---
fig, ax = plt.subplots()
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.axis("off")

beam, = ax.plot([-0.6, 0.6], [0, 0], linewidth=4)
text = ax.text(0, -0.6, "", ha="center", fontsize=12)

steps = []  # record weighings for animation

def weigh(left, right, weights, weighing_num):
    lw = sum(weights[c] for c in left)
    rw = sum(weights[c] for c in right)

    if lw > rw:
        result = Result.LEFT_HEAVY
    elif lw < rw:
        result = Result.RIGHT_HEAVY
    else:
        result = Result.BALANCE

    # record step for animation
    steps.append((weighing_num, left, right, lw, rw, result))
    return result

def animate(i):
    n, left, right, lw, rw, result = steps[i]

    if result == Result.LEFT_HEAVY:
        beam.set_ydata([0.2, -0.2])
        outcome = "Left heavier"
    elif result == Result.RIGHT_HEAVY:
        beam.set_ydata([-0.2, 0.2])
        outcome = "Right heavier"
    else:
        beam.set_ydata([0, 0])
        outcome = "Balanced"

    text.set_text(
        f"Weighing {n}\nLeft: {left} (wt={lw})\nRight: {right} (wt={rw})\nOutcome: {outcome}"
    )
    return beam, text

# --- Test Setup ---
def generate_test(fake_coin, direction):
    weights = {}
    for group in ["A","B","C"]:
        for i in range(1,5):
            weights[f"{group}{i}"] = 10
    weights[fake_coin] += 1 if direction == "heavier" else -1
    return weights

# Example run
weights = generate_test("A3", "heavier")
weigh(["A1","A2","A3","A4"], ["B1","B2","B3","B4"], weights, 1)
weigh(["A3","B1","B2","B4"], ["C1","C2","B3","C4"], weights, 2)
weigh(["B3"], ["C4"], weights, 3)

ani = animation.FuncAnimation(fig, animate, frames=len(steps), interval=2000, repeat=False)
plt.show()
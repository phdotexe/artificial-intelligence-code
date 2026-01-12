import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
        result = "LEFT_HEAVY"
    elif lw < rw:
        result = "RIGHT_HEAVY"
    else:
        result = "BALANCE"

    steps.append((weighing_num, left, right, lw, rw, result))
    return result

def animate(i):
    n, left, right, lw, rw, result = steps[i]

    if result == "LEFT_HEAVY":
        beam.set_ydata([0.2, -0.2])
        outcome = "Left heavier"
    elif result == "RIGHT_HEAVY":
        beam.set_ydata([-0.2, 0.2])
        outcome = "Right heavier"
    else:
        beam.set_ydata([0, 0])
        outcome = "Balanced"

    text.set_text(
        f"Weighing {n}\nLeft: {left} (wt={lw})\nRight: {right} (wt={rw})\nOutcome: {outcome}"
    )
    return beam, text

# --- Ineffective Brute Force Solver ---
def brute_force(weights):
    reference = "A1"
    weighing_num = 1
    for coin in weights.keys():
        if coin == reference:
            continue
        result = weigh([coin], [reference], weights, weighing_num)
        weighing_num += 1
        if result != "BALANCE":
            # Found counterfeit
            direction = "heavier" if result == "LEFT_HEAVY" else "lighter"
            print(f"SOLUTION FOUND: Coin {coin} is {direction}")
            break

# --- Test Setup ---
def generate_test(fake_coin, direction):
    weights = {}
    for group in ["A","B","C"]:
        for i in range(1,5):
            weights[f"{group}{i}"] = 10
    weights[fake_coin] += 1 if direction == "heavier" else -1
    return weights

weights = generate_test("C2", "lighter")
brute_force(weights)

ani = animation.FuncAnimation(fig, animate, frames=len(steps), interval=1500, repeat=False)
plt.show()
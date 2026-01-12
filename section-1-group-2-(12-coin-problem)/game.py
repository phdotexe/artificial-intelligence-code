import pygame
import sys
import math
import random

# ------------------ INIT ------------------
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("12 Coin Puzzle")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

COIN_RADIUS = 20
MAX_PER_PAN = 4
MAX_WEIGHS = 3

LEFT_PAN_POS = (250, 420)
RIGHT_PAN_POS = (550, 420)

TILT_AMOUNT = 20
TILT_SPEED = 2

# ------------------ RESET FUNCTION ------------------
def reset_game():
    global fake_coin, fake_type, weigh_count, weigh_result
    global game_phase, guess_result, message
    global left_offset, right_offset, left_target, right_target

    fake_coin = random.choice(ALL_COINS)
    fake_type = random.choice(["heavier", "lighter"])

    weigh_count = 0
    weigh_result = ""
    game_phase = "weighing"
    guess_result = ""
    message = ""

    left_offset = right_offset = 0
    left_target = right_target = 0

    x, y = 100, 80
    for c in coins:
        c["zone"] = "pool"
        c["selected"] = False
        c["pos"] = (x, y)
        x += 80
        if x > 600:
            x = 100
            y += 80

# ------------------ COINS ------------------
ALL_COINS = [
    "A1","A2","A3","A4",
    "B1","B2","B3","B4",
    "C1","C2","C3","C4"
]

fake_coin = random.choice(ALL_COINS)
fake_type = random.choice(["heavier", "lighter"])
print(fake_coin, fake_type)

def get_weight(label):
    if label == fake_coin:
        return 11 if fake_type == "heavier" else 9
    return 10

# ------------------ DRAW HELPERS ------------------
def draw_coin(x, y, label, selected):
    pygame.draw.circle(screen, (200,200,0), (x,y), COIN_RADIUS)
    border = (255,0,0) if selected else (0,0,0)
    pygame.draw.circle(screen, border, (x,y), COIN_RADIUS, 2)
    text = font.render(label, True, (0,0,0))
    screen.blit(text, (x-12, y-8))

def coin_clicked(pos, mouse):
    return math.hypot(pos[0]-mouse[0], pos[1]-mouse[1]) <= COIN_RADIUS

def draw_pan(cx, cy, label):
    pygame.draw.rect(screen, (180,180,180),
        (cx-120, cy-30, 240, 60), border_radius=10)
    screen.blit(font.render(label, True, (0,0,0)), (cx-45, cy-55))

# ------------------ CREATE COINS ------------------
coins = []
x, y = 100, 80
for label in ALL_COINS:
    coins.append({
        "label": label,
        "pos": (x,y),
        "selected": False,
        "zone": "pool"
    })
    x += 80
    if x > 600:
        x = 100
        y += 80

# ------------------ GAME STATE ------------------
weigh_count = 0
weigh_result = ""
message = ""
game_phase = "weighing"
guess_result = ""

left_offset = right_offset = 0
left_target = right_target = 0

# ------------------ MAIN LOOP ------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---- MOUSE ----
        if event.type == pygame.MOUSEBUTTONDOWN:
            for c in coins:
                if coin_clicked(c["pos"], event.pos):
                    c["selected"] = not c["selected"]

        # ---- KEYS ----
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_x:
                reset_game()

            if event.key == pygame.K_1:
                for c in coins:
                    if c["selected"]:
                        c["zone"] = "left"
                        c["selected"] = False

            if event.key == pygame.K_2:
                for c in coins:
                    if c["selected"]:
                        c["zone"] = "right"
                        c["selected"] = False

            if event.key == pygame.K_p:
                for c in coins:
                    if c["selected"]:
                        c["zone"] = "pool"
                        c["selected"] = False

            # ---- WEIGH ----
            if event.key == pygame.K_w and game_phase == "weighing":
                left = [c for c in coins if c["zone"] == "left"]
                right = [c for c in coins if c["zone"] == "right"]

                if (
                    len(left) == 0 or
                    len(left) != len(right) or
                    len(left) > MAX_PER_PAN
                ):
                    message = "Invalid weighing"
                    weigh_result = ""
                else:
                    lw = sum(get_weight(c["label"]) for c in left)
                    rw = sum(get_weight(c["label"]) for c in right)

                    if lw == rw:
                        weigh_result = "BALANCE"
                        left_target = right_target = 0
                    elif lw > rw:
                        weigh_result = "LEFT_HEAVY"
                        left_target = TILT_AMOUNT
                        right_target = -TILT_AMOUNT
                    else:
                        weigh_result = "RIGHT_HEAVY"
                        left_target = -TILT_AMOUNT
                        right_target = TILT_AMOUNT

                    weigh_count += 1
                    message = f"Weighing {weigh_count}/{MAX_WEIGHS}"

                    if weigh_count == MAX_WEIGHS:
                        game_phase = "guessing"

            # ---- GUESS ----
            if game_phase == "guessing":
                selected = [c for c in coins if c["selected"]]
                if len(selected) == 1:
                    if event.key == pygame.K_h:
                        guess_coin = selected[0]["label"]
                        guess_type = "heavier"
                    elif event.key == pygame.K_l:
                        guess_coin = selected[0]["label"]
                        guess_type = "lighter"
                    else:
                        continue

                    if guess_coin == fake_coin and guess_type == fake_type:
                        guess_result = "CORRECT 🎉"
                    else:
                        guess_result = f"WRONG ❌ ({fake_coin}, {fake_type})"

                    game_phase = "done"

    # ---- ANIMATION ----
    if left_offset < left_target:
        left_offset += TILT_SPEED
    elif left_offset > left_target:
        left_offset -= TILT_SPEED

    if right_offset < right_target:
        right_offset += TILT_SPEED
    elif right_offset > right_target:
        right_offset -= TILT_SPEED

    # ------------------ DRAW ------------------
    screen.fill((240,240,240))
    draw_pan(LEFT_PAN_POS[0], LEFT_PAN_POS[1]+left_offset, "LEFT PAN")
    draw_pan(RIGHT_PAN_POS[0], RIGHT_PAN_POS[1]+right_offset, "RIGHT PAN")

    pool_x, pool_y = 100, 80
    left_x = LEFT_PAN_POS[0] - 90
    right_x = RIGHT_PAN_POS[0] - 90

    for c in coins:
        if c["zone"] == "pool":
            c["pos"] = (pool_x, pool_y)
            pool_x += 80
            if pool_x > 600:
                pool_x = 100
                pool_y += 80
        elif c["zone"] == "left":
            c["pos"] = (left_x, LEFT_PAN_POS[1]+left_offset)
            left_x += 60
        else:
            c["pos"] = (right_x, RIGHT_PAN_POS[1]+right_offset)
            right_x += 60

        draw_coin(c["pos"][0], c["pos"][1], c["label"], c["selected"])

    # ---- UI ----
    screen.blit(font.render(f"Weighings: {weigh_count}/{MAX_WEIGHS}", True, (0,0,0)), (20,520))
    screen.blit(font.render("Press X to RESET", True, (0,0,0)), (620,520))

    if weigh_result:
        screen.blit(font.render(f"Result: {weigh_result}", True, (0,0,0)), (300,520))

    if game_phase == "guessing":
        screen.blit(font.render("Select one coin + H or L", True, (0,0,200)), (240,550))

    if game_phase == "done":
        screen.blit(font.render(guess_result, True, (0,150,0)), (260,300))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

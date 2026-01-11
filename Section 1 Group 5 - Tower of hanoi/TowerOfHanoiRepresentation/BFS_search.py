from collections import deque

def bfs_hanoi(n):
    # Initial and goal states
    start = (tuple(range(n, 0, -1)), (), ())
    goal = ((), (), tuple(range(n, 0, -1)))

    queue = deque([start])
    print(queue)
    visited = {start}
    parent = {start: None}
    move = {}

    while queue:
        state = queue.pop()

        if state == goal:
            break

        for i in range(3):          # source peg
            for j in range(3):      # destination peg
                if i == j:
                    continue

                src = list(state[i])

                dst = list(state[j])
                if not src:
                    continue

                disk = src[-1]

                if dst and dst[-1] < disk:
                    continue

                # perform move
                src.pop()
                dst.append(disk)

                new_state = list(state)
                new_state[i] = tuple(src)
                new_state[j] = tuple(dst)
                new_state = tuple(new_state)

                if new_state not in visited:
                    visited.add(new_state)
                    parent[new_state] = state
                    move[new_state] = (disk, i, j)
                    queue.append(new_state)

    # reconstruct path
    path = []
    current = goal
    while parent[current] is not None:
        path.append(move[current])
        current = parent[current]

    path.reverse()
    return path

moves = bfs_hanoi(3)

for disk, src, dst in moves:
    print(f"Move disk {disk} from peg {src} to peg {dst}")

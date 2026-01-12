import heapq
import random
import pygame

GOAL = tuple(range(1, 16)) + (0,)

def get_neighbors(state):
    """Return valid neighbor states reachable by sliding the empty tile.

    Args:
        state (tuple): Current puzzle state as a 16-element tuple (0 is empty).

    Returns:
        list: A list of tuples ``(neighbor_state, move)`` where ``move`` is
              one of 'U', 'D', 'L', 'R'.
    """
    state = list(state)
    idx = state.index(0)
    row, col = idx // 4, idx % 4
    neighbors = []
    for dr, dc, move in [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 4 and 0 <= new_col < 4:
            new_idx = new_row * 4 + new_col
            new_state = state[:]
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            neighbors.append((tuple(new_state), move))
    return neighbors

def manhattan_distance(state):
    """Compute the Manhattan distance heuristic for a puzzle state.

    The heuristic is the sum over tiles of the distance (rows + cols)
    from their current position to their goal position.

    Args:
        state (tuple): Current puzzle state as a 16-element tuple (0 is empty).

    Returns:
        int: The total Manhattan distance.
    """
    distance = 0
    for i in range(16):
        if state[i] == 0:
            continue
        goal_idx = state[i] - 1
        curr_row, curr_col = i // 4, i % 4
        goal_row, goal_col = goal_idx // 4, goal_idx % 4
        distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance

def solve_astar(start):   
    """Solve the 15-puzzle using the A* search algorithm with Manhattan
    distance heuristic.

    Args:
        start (tuple): Start puzzle state as a 16-element tuple (0 is empty).

    Returns:
        tuple: ``(path, nodes_explored)`` where ``path`` is a list of moves
               ('U','D','L','R') from start to goal, or ``None`` if no
               solution found; ``nodes_explored`` is an int.
    """
    frontier = [(manhattan_distance(start), 0, start, [])]
    visited = set()
    nodes_explored = 0
    while frontier:
        _, g, current, path = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1
        if current == GOAL:
            return path, nodes_explored
        for neighbor, move in get_neighbors(current):
            if neighbor not in visited:
                h = manhattan_distance(neighbor)
                heapq.heappush(frontier, (g + 1 + h, g + 1, neighbor, path + [move]))
    return None, nodes_explored

def solve_dfs(start, max_depth=50):
    """Attempt to solve the 15-puzzle using depth-first search.

    This is a basic DFS with a depth limit to avoid infinite exploration.

    Args:
        start (tuple): Start puzzle state as a 16-element tuple (0 is empty).
        max_depth (int): Maximum search depth (inclusive).

    Returns:
        tuple: ``(path, nodes_explored)`` where ``path`` is a list of moves
               if a solution is found, otherwise ``None``; ``nodes_explored``
               is an int of how many nodes were visited.
    """
    stack = [(start, [], 0)]
    visited = set()
    nodes_explored = 0
    while stack:
        current, path, depth = stack.pop()
        if current in visited or depth > max_depth:
            continue
        visited.add(current)
        nodes_explored += 1
        if current == GOAL:
            return path, nodes_explored
        for neighbor, move in get_neighbors(current):
            if neighbor not in visited:
                stack.append((neighbor, path + [move], depth + 1))
    return None, nodes_explored

def scramble_puzzle(moves=50):
    """Return a scrambled puzzle state by applying random valid moves.

    Args:
        moves (int): Number of random moves to apply starting from the goal.

    Returns:
        tuple: A new puzzle state as a 16-element tuple.
    """
    state = list(GOAL)
    for _ in range(moves):
        neighbors = get_neighbors(tuple(state))
        state = list(random.choice(neighbors)[0])
    return tuple(state)

def print_board(state):
    """Print the puzzle state to stdout in a 4x4 grid format.

    Args:
        state (tuple): Current puzzle state as a 16-element tuple (0 is empty).
    """
    for i in range(0, 16, 4):
        print(' '.join(f'{state[j]:2}' if state[j] != 0 else ' .' for j in range(i, i + 4)))
    print()

# def animate_pygame(start, solution, algorithm_name):
#     """Animate the puzzle solution using Pygame and advance on mouse clicks.

#     Args:
#         start (tuple): Start puzzle state as a 16-element tuple (0 is empty).
#         solution (list): List of moves ('U','D','L','R') to apply.
#         algorithm_name (str): Name to display in the window title.
#     """
#     pygame.init()
#     screen = pygame.display.set_mode((400, 450))
#     pygame.display.set_caption(f"15 Puzzle - {algorithm_name} (Click for next step)")
#     font = pygame.font.Font(None, 36)
#     info_font = pygame.font.Font(None, 24)
#     clock = pygame.time.Clock()
#     current = start
#     step = 0
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.MOUSEBUTTONDOWN and step < len(solution):
#                 neighbors = get_neighbors(current)
#                 for next_state, move in neighbors:
#                     if move == solution[step]:
#                         current = next_state
#                         break
#                 step += 1
#         screen.fill((200, 200, 200))
#         for i in range(16):
#             row, col = i // 4, i % 4
#             x, y = col * 100, row * 100
#             if current[i] == 0:
#                 pygame.draw.rect(screen, (100, 100, 100), (x, y, 100, 100))
#             else:
#                 pygame.draw.rect(screen, (255, 255, 255), (x, y, 100, 100))
#                 pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 100), 2)
#                 text = font.render(str(current[i]), True, (0, 0, 0))
#                 text_rect = text.get_rect(center=(x + 50, y + 50))
#                 screen.blit(text, text_rect)
#         info_text = info_font.render(f"Step: {step}/{len(solution)}", True, (0, 0, 0))
#         screen.blit(info_text, (10, 410))
#         pygame.display.flip()
#         clock.tick(60)
#     pygame.quit()

def animate_pygame(start, solution, algorithm_name):
    """Animate the puzzle solution using Pygame with automatic progression.

    Args:
        start (tuple): Start puzzle state as a 16-element tuple (0 is empty).
        solution (list): List of moves ('U','D','L','R') to apply.
        algorithm_name (str): Name to display in the window title.
    """
    pygame.init()
    screen = pygame.display.set_mode((400, 450))
    pygame.display.set_caption(f"15 Puzzle - {algorithm_name}")
    font = pygame.font.Font(None, 36)
    info_font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    current = start
    step = 0
    running = True
    
    # Animation timing
    move_delay = 500  # milliseconds between moves
    last_move_time = pygame.time.get_ticks()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Auto-advance to next step
        current_time = pygame.time.get_ticks()
        if step < len(solution) and current_time - last_move_time >= move_delay:
            neighbors = get_neighbors(current)
            for next_state, move in neighbors:
                if move == solution[step]:
                    current = next_state
                    break
            step += 1
            last_move_time = current_time
        
        # Draw the puzzle
        screen.fill((200, 200, 200))
        for i in range(16):
            row, col = i // 4, i % 4
            x, y = col * 100, row * 100
            if current[i] == 0:
                pygame.draw.rect(screen, (100, 100, 100), (x, y, 100, 100))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, 100, 100))
                pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 100), 2)
                text = font.render(str(current[i]), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + 50, y + 50))
                screen.blit(text, text_rect)
        
        # Draw step counter
        info_text = info_font.render(f"Step: {step}/{len(solution)}", True, (0, 0, 0))
        screen.blit(info_text, (10, 410))
        
        # Show completion message
        if step >= len(solution):
            complete_text = info_font.render("Complete! Close window to exit.", True, (0, 128, 0))
            screen.blit(complete_text, (10, 430))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    
def main():
    """Simple command-line interface to scramble and solve the 15-puzzle.

    Prompts the user to choose A* or DFS, scrambles a puzzle, attempts to
    solve it, and optionally animates the solution.
    """
    while True:
        print("\n1. A*  2. DFS  3. Exit")
        choice = input("Choose: ").strip()
        if choice == '3':
            break
        if choice not in ['1', '2']:
            continue
        start_state = scramble_puzzle(50)
        print("\nInitial State:")
        print_board(start_state)
        if choice == '1':
            solution, nodes = solve_astar(start_state)
            algorithm_name = "A*"
        else:
            solution, nodes = solve_dfs(start_state, 20)
            algorithm_name = "DFS"
        if solution:
            print(f"Solution: {len(solution)} moves, {nodes} nodes")
            if input("Animate? (y/n): ").strip().lower() == 'y':
                animate_pygame(start_state, solution, algorithm_name)
        else:
            print(f"No solution ({nodes} nodes explored)")

if __name__ == "__main__":
    main()
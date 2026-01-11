import random

def monty_hall_simulation(num_simulations=10000):
    """
    Simulates the Monty Hall problem.
    Returns the win rates for sticking vs. switching.
    """
    stick_wins = 0
    switch_wins = 0
    
    for _ in range(num_simulations):
        # Randomly place the car behind one of the three doors (0, 1, or 2)
        car_door = random.randint(0, 2)
        
        # Contestant randomly picks a door
        contestant_pick = random.randint(0, 2)
        
        # Host opens a door with a goat (not the car, not the contestant's pick)
        possible_doors = [0, 1, 2]
        possible_doors.remove(contestant_pick)
        if car_door in possible_doors:
            possible_doors.remove(car_door)
        # If car is behind contestant's pick, host can open either remaining door
        host_opens = random.choice(possible_doors)
        
        # The remaining door after host opens one
        remaining_doors = [0, 1, 2]
        remaining_doors.remove(contestant_pick)
        remaining_doors.remove(host_opens)
        switch_pick = remaining_doors[0]
        
        # Check wins
        if contestant_pick == car_door:
            stick_wins += 1
        if switch_pick == car_door:
            switch_wins += 1
    
    stick_rate = stick_wins / num_simulations
    switch_rate = switch_wins / num_simulations
    
    return stick_rate, switch_rate

# Run the simulation
stick_win_rate, switch_win_rate = monty_hall_simulation()

print(f"After 10,000 simulations:")
print(f"Win rate if sticking: {stick_win_rate:.3f} (≈ 1/3)")
print(f"Win rate if switching: {switch_win_rate:.3f} (≈ 2/3)")
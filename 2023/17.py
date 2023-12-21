# https://adventofcode.com/2023/day/17

def build_initial_cost(cost):
	return {'U': {0: cost}, 'D': {0: cost}, 'L': {0: cost}, 'R': {0: cost}}

def opposite_direction(direction):
	if direction == 'L': return 'R'
	if direction == 'R': return 'L'
	if direction == 'U': return 'D'
	if direction == 'D': return 'U'
	return None

def add_cost(cost_map, min_initial_move, pos, direction, movement, cost):
	added = False
	for ite_direction, ite_costs in cost_map[pos].items():
		if ite_direction == direction:
			skip = False
			for ite_movement in range(0 if min_initial_move == 1 else 1, movement):
				if ite_movement in ite_costs and cost >= ite_costs[ite_movement]:
					skip = True
					break
			if skip:
				continue
			if movement not in ite_costs or cost < ite_costs[movement]:
				ite_costs[movement] = cost
				added = True
		elif ite_direction != opposite_direction(direction):
			if 0 not in ite_costs or cost < ite_costs[0]:
				ite_costs[0] = cost
				added = True

				# for ite_movement in range(1, 3 + 1):
				# 	if ite_movement in ite_costs and cost <= ite_costs[ite_movement]:
				# 		ite_costs.pop(ite_movement)
	return added

def calculate_min_cost(costs):
	min_cost = None
	for direction_costs in costs.values():
		for cost in direction_costs.values():
			if min_cost == None or cost < min_cost:
					min_cost = cost
	return min_cost

def my_star(grid, start, end, min_initial_move, max_moves):
	global DEBUG
	INFINITY = float('inf')

	NEIGHBORS_DELTAS = { 'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

	open_set = {start}
	came_from = {}

	cost_map = {}
	cost_map[start] = build_initial_cost(0)

	while open_set:
		current = min(open_set, key=lambda pos: calculate_min_cost(cost_map[pos]))
		if DEBUG: print('current', current, 'cost', cost_map[current])
		if current == end:
			return calculate_min_cost(cost_map[current])

		open_set.remove(current)
		for direction, neighbor_delta in NEIGHBORS_DELTAS.items():
			current_direction_costs = cost_map[current][direction]
			for current_movement, current_cost in current_direction_costs.items():
				if current_movement == max_moves or current_cost == INFINITY:
					continue

				movement = min_initial_move if current_movement == 0 else 1
				neighbor = (current[0] + neighbor_delta[0] * movement, current[1] + neighbor_delta[1] * movement)
				if neighbor[0] < 0 or neighbor[0] >= len(grid) or neighbor[1] < 0 or neighbor[1] >= len(grid[0]):
					continue

				neighbor_cost = current_cost
				for move in range(1, movement + 1):
					neighbor_cost += grid[current[0] + neighbor_delta[0] * move][current[1] + neighbor_delta[1] * move]

				if DEBUG: print('evaluating neighbor', neighbor, direction, current_movement + movement, neighbor_cost, 'previously', cost_map.get(neighbor))
				if neighbor not in cost_map:
					cost_map[neighbor] = build_initial_cost(neighbor_cost)
					cost_map[neighbor][direction] = {current_movement + movement: neighbor_cost}
					cost_map[neighbor][opposite_direction(direction)] = {0: INFINITY}
					if DEBUG: print('first neighbor!', cost_map[neighbor])
				elif add_cost(cost_map, min_initial_move, neighbor, direction, current_movement + movement, neighbor_cost):
					if DEBUG: print('updated neighbor!', cost_map[neighbor])
				else:
					if DEBUG: print('bad neighbor...')
					continue
				if neighbor not in open_set:
					open_set.add(neighbor)
	return None

def solve_1(filename):
	file = open(filename, 'r')
	grid = [[int(char) for char in line.strip()] for line in file.readlines()]

	heat_loss = my_star(grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1), 1, 3)
	print(filename, 'heat_loss', heat_loss)

def solve_2(filename):
	file = open(filename, 'r')
	grid = [[int(char) for char in line.strip()] for line in file.readlines()]

	heat_loss = my_star(grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1), 4, 10)
	print(filename, 'heat_loss_ultra', heat_loss)

DEBUG = False

solve_1('17_sample.txt') # 102
solve_1('17_input.txt') # 684

solve_2('17_sample.txt') # 94
solve_2('17_sample2.txt') # 71
solve_2('17_input.txt') # 822

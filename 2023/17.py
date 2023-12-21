# https://adventofcode.com/2023/day/17

from copy import deepcopy

def calculate_neighbors(grid, point):
	neighbors = {}
	if point[0] > 0:
		neighbors['U'] = (point[0] - 1, point[1])
	if point[0] < len(grid) - 1:
		neighbors['D'] = (point[0] + 1, point[1])
	if point[1] > 0:
		neighbors['L'] = (point[0], point[1] - 1)
	if point[1] < len(grid[0]) - 1:
		neighbors['R'] = (point[0], point[1] + 1)
	return neighbors

def build_initial_cost(cost):
	return {'U': {0: cost}, 'D': {0: cost}, 'L': {0: cost}, 'R': {0: cost}}

def opposite_direction(direction):
	if direction == 'L': return 'R'
	if direction == 'R': return 'L'
	if direction == 'U': return 'D'
	if direction == 'D': return 'U'
	return None

def add_cost(cost_map, pos, direction, movement, cost):
	added = False
	for ite_direction, ite_costs in cost_map[pos].items():
		if ite_direction == direction:
			skip = False
			for ite_movement in range(0, movement):
				if ite_movement in ite_costs and cost >= ite_costs[ite_movement]:
					skip = True
					break
			if skip:
				continue
			if movement not in ite_costs or cost < ite_costs[movement]:
				ite_costs[movement] = cost
				added = True
			for ite_movement in range(movement + 1, 4):
				if ite_movement in ite_costs and cost <= ite_costs[ite_movement]:
					ite_costs.pop(ite_movement)
					added = True
		else: # ite_direction != direction:
			if opposite_direction(direction) == ite_direction:
				continue
			if 0 not in ite_costs or cost < ite_costs[0]:
				ite_costs[0] = cost
				added = True

				for ite_movement in range(1, 4):
					if ite_movement in ite_costs and cost <= ite_costs[ite_movement]:
						ite_costs.pop(ite_movement)
	return added

def calculate_min_cost(costs):
	min_cost = None
	for direction_costs in costs.values():
		for cost in direction_costs.values():
			if min_cost == None or cost < min_cost:
					min_cost = cost
	return min_cost

def my_star(grid, start, end, min_moves, max_moves):
	INFINITY = float('inf')

	open_set = {start}
	came_from = {}

	cost_map = {}
	cost_map[start] = build_initial_cost(0)

	while open_set:
		current = min(open_set, key=lambda pos: calculate_min_cost(cost_map[pos]))
		# print('current', current, 'cost', cost_map[current])
		if current == end:
			return calculate_min_cost(cost_map[current])

		open_set.remove(current)
		for direction, neighbor_ in calculate_neighbors(grid, current).items():
			current_direction_costs = cost_map[current][direction]
			for current_movement, current_cost in current_direction_costs.items():
				if current_movement == max_moves or current_cost == INFINITY:
					continue

				neighbor_cost = None
				neighbor = deepcopy(neighbor_)
				movement = 1
				if current_movement == 0:
					di = (neighbor[0] - current[0])
					dj = (neighbor[1] - current[1])
					neighbor = (current[0] + di * min_moves, current[1] + dj * min_moves)
					if neighbor[0] < 0 or neighbor[0] >= len(grid) or neighbor[1] < 0 or neighbor[1] >= len(grid[0]):
						continue
					movement = min_moves
					neighbor_cost = current_cost
					for move in range(1, min_moves + 1):
						neighbor_cost += grid[current[0] + move * di][current[1] + move * dj]
				else:
					neighbor_cost = current_cost + grid[neighbor[0]][neighbor[1]]

				# print('evaluating neighbor', neighbor, direction, current_movement + movement, neighbor_cost, 'previously', cost_map.get(neighbor))
				if neighbor not in cost_map:
					cost_map[neighbor] = build_initial_cost(neighbor_cost)
					cost_map[neighbor][direction] = {current_movement + movement: neighbor_cost}
					cost_map[neighbor][opposite_direction(direction)] = {0: INFINITY}
					# print('first neighbor!', cost_map[neighbor])
				elif add_cost(cost_map, neighbor, direction, current_movement + movement, neighbor_cost):
					# print('updated neighbor!', cost_map[neighbor])
					pass
				else:
					# print('bad neighbor...')
					continue
				if neighbor not in open_set:
					open_set.add(neighbor)
	return None

def solve_1(filename):
	file = open(filename, 'r')
	grid = [[int(char) for char in line.strip()] for line in file.readlines()]
	# for row in grid: print(row)

	heat_loss = my_star(grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1), 1, 3)
	print(filename, 'heat_loss', heat_loss)

def solve_2(filename):
	file = open(filename, 'r')
	grid = [[int(char) for char in line.strip()] for line in file.readlines()]
	# for row in grid: print(row)

	heat_loss = my_star(grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1), 4, 10)
	print(filename, 'heat_loss_ultra', heat_loss)

solve_1('17_sample.txt') # 102
solve_1('17_input.txt') # 684

solve_2('17_sample.txt') # 94
solve_2('17_sample2.txt') # 71
solve_2('17_input.txt') # ? < 824

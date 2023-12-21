# https://adventofcode.com/2023/day/17

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
		else:
			if 0 not in ite_costs or cost < ite_costs[0]:
				ite_costs[0] = cost
				added = True
			for ite_movement, ite_cost in dict(ite_costs).items():
				if cost < ite_cost:
					ite_costs.pop(ite_movement)
					added = True
	return added

def calculate_min_cost(costs):
	min_cost = None
	for direction_costs in costs.values():
		for cost in direction_costs.values():
			if min_cost == None or cost < min_cost:
					min_cost = cost
	return min_cost

def my_star(grid, start, end):
	INFINITY = float('inf')

	open_set = {start}
	came_from = {}

	cost_map = {}
	cost_map[start] = build_initial_cost(0)

	while open_set:
		current = min(open_set, key=lambda pos: calculate_min_cost(cost_map[pos]))
		print('current', current, 'cost', cost_map[current])
		if current == end:
			return calculate_min_cost(cost_map[current])

		open_set.remove(current)
		for direction, neighbor in calculate_neighbors(grid, current).items():
			current_direction_costs = cost_map[current][direction]
			for current_movement, current_cost in current_direction_costs.items():
				if current_movement == 3:
					continue

				neighbor_cost = current_cost + grid[neighbor[0]][neighbor[1]]
				print('evaluating neighbor', neighbor, direction, current_movement + 1, neighbor_cost, 'previously', cost_map.get(neighbor))
				if neighbor not in cost_map:
					print('first neighbor!')
					cost_map[neighbor] = build_initial_cost(neighbor_cost)
					cost_map[neighbor][direction] = {current_movement + 1: neighbor_cost}
				elif add_cost(cost_map, neighbor, direction, current_movement + 1, neighbor_cost):
					print('updated neighbor!')
					pass
				else:
					print('bad neighbor...')
					continue
				if neighbor not in open_set:
					open_set.add(neighbor)

	print('oops...')
	return None

def solve_1(filename):
	file = open(filename, 'r')
	grid = [[int(char) for char in line.strip()] for line in file.readlines()]
	for row in grid: print(row)

	heat_loss = my_star(grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1))
	print(filename, 'heat_loss', heat_loss)

solve_1('17_sample.txt')
# solve_1('17_input.txt')

# 680 < answer < 701

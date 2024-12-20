# https://adventofcode.com/2024/day/20

def parse_input(filename):
	file = open(filename, 'r')
	grid = []
	start = None
	end = None
	for i, line in enumerate(file.readlines()):
		grid.append(line.strip())
		if 'S' in line:
			start = (i, line.index('S'))
		if 'E' in line:
			end = (i, line.index('E'))
	return grid, start, end

def print_grid(grid):
	for line in grid:
		for char in line:
			print(char, end='')
		print()

# DELTAS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
# def neighbors(pos, step = 1):
# 	return [(pos[0] + delta[0] * step, pos[1] + delta[1] * step) for delta in DELTAS]

def neighbors(pos, step = 1):
	ns = []
	for di in range(-step, step + 1):
		max_dj = step - abs(di)
		for dj in range(-max_dj, max_dj + 1):
			ns.append((pos[0] + di, pos[1] + dj))
	return ns

def is_within_bounds(grid, pos):
	return pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[0])		

def solve(filename, cheat_length, threshold):
	grid, start, end = parse_input(filename)
	# print_grid(grid)
	# print(start, end)

	pos = start
	picos = 0
	pos_picos = {start: 0}
	while pos != end:
		picos += 1
		for n in neighbors(pos):
			if not is_within_bounds(grid, n):
				continue
			if n in pos_picos:
				continue
			if grid[n[0]][n[1]] != '#':
				pos = n
				pos_picos[n] = picos
				break
	# print(pos_picos)

	cheats = 0
	for pos, picos in pos_picos.items():
		for n in neighbors(pos, cheat_length):
			if n not in pos_picos:
				continue
			shortcut = pos_picos[n] - picos - (abs(pos[0] - n[0]) + abs(pos[1] - n[1]))
			if shortcut >= threshold:
				# print('shortcut', pos, picos, n, pos_picos[n], shortcut)
				cheats += 1
	print('cheats', cheats)

solve('20_sample.txt', 2, 10) # 10
solve('20_input.txt', 2, 100) # 1459

solve('20_sample.txt', 20, 50) # 285
solve('20_input.txt', 20, 100) # 1016066

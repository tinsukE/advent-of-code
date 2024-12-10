# https://adventofcode.com/2024/day/10

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()

	top_map = []
	for line in lines:
		top_map.append([int(char) for char in line.strip()])

	heads = []
	for i, row in enumerate(top_map):
		for j, height in enumerate(row):
			if height == 0:
				heads.append((i, j))
	return top_map, heads

def is_within_bounds(area_map, pos):
	return pos[0] >= 0 and pos[0] < len(area_map) and pos[1] >= 0 and pos[1] < len(area_map[0])

DELTAS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
def score(top_map, pos, height, heads):
	if top_map[pos[0]][pos[1]] == 9:
		if heads != None and pos in heads:
			return 0
		if heads != None:
			heads.add(pos)
		return 1

	sum_score = 0
	for delta in DELTAS:
		new_pos = (pos[0] + delta[0], pos[1] + delta[1])
		if not is_within_bounds(top_map, new_pos):
			continue
		if top_map[new_pos[0]][new_pos[1]] == height + 1:
			sum_score += score(top_map, new_pos, height + 1, heads)
	return sum_score

def solve(filename):
	top_map, heads = parse_input(filename)
	sum_score = sum(score(top_map, head, 0, set()) for head in heads)
	print('sum_score', sum_score)
	sum_score_2 = sum(score(top_map, head, 0, None) for head in heads)
	print('sum_score_2', sum_score_2)

solve('10_sample.txt') # 36  81
solve('10_input.txt')  # 688 1459

# https://adventofcode.com/2024/day/4

def parse_input(filename):
	file = open(filename, 'r')
	lines = [line.strip() for line in file.readlines()]
	return lines

def is_within_bounds(puzzle, pos):
	return pos[0] >= 0 and pos[0] < len(puzzle) and pos[1] >= 0 and pos[1] < len(puzzle[0])

def is_match(puzzle, word, pos, delta):
	if not is_within_bounds(puzzle, pos):
		return False

	if (puzzle[pos[0]][pos[1]] == word[0]):
		if len(word) == 1:
			return True

		new_pos = (pos[0] + delta[0], pos[1] + delta[1])
		if not is_within_bounds(puzzle, new_pos):
			return False

		return is_match(puzzle, word[1:], new_pos, delta)

	return False

def count_xmas_matches(puzzle, pos):
	deltas = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
	return sum(is_match(puzzle, 'XMAS', pos, delta) for delta in deltas)

def solve(filename):
	puzzle = parse_input(filename)

	all_pos = ((row, col) for row in range(len(puzzle)) for col in range(len(puzzle[row])))
	matches = sum(count_xmas_matches(puzzle, (row, col)) for (row, col) in all_pos)

	print("matches", matches)

def is_x_mas_match(puzzle, pos):
	return (is_match(puzzle, 'MAS', (pos[0] - 1, pos[1] - 1) , (1, 1)) or \
		is_match(puzzle, 'MAS', (pos[0] + 1, pos[1] + 1) , (-1, -1))) and \
		(is_match(puzzle, 'MAS', (pos[0] + 1, pos[1] - 1) , (-1, 1)) or \
		is_match(puzzle, 'MAS', (pos[0] - 1, pos[1] + 1) , (1, -1)))

def solve_2(filename):
	puzzle = parse_input(filename)

	all_pos = ((row, col) for row in range(len(puzzle)) for col in range(len(puzzle[row])))
	matches = sum(is_x_mas_match(puzzle, (row, col)) for (row, col) in all_pos)

	print("matches", matches)


solve('04_sample.txt') # 18
solve('04_input.txt') # 2718

solve_2('04_sample.txt') # 9
solve_2('04_input.txt') # 2046

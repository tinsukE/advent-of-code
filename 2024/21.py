# https://adventofcode.com/2024/day/21

from functools import cache

NUM_KEYPAD = ( \
	('7', '8', '9'), \
	('4', '5', '6'), \
	('1', '2', '3'), \
	(None, '0', 'A'), \
)
NUM_START = (3, 2)
NUM_POS = {}
for i in range(len(NUM_KEYPAD)):
	for j in range(len(NUM_KEYPAD[0])):
		NUM_POS[NUM_KEYPAD[i][j]] = (i, j)

DIR_KEYPAD = ( \
	(None, '^', 'A'), \
	('<', 'v', '>'), \
)
DIR_START = (0, 2)
DIR_POS = {}
for i in range(len(DIR_KEYPAD)):
	for j in range(len(DIR_KEYPAD[0])):
		DIR_POS[DIR_KEYPAD[i][j]] = (i, j)

def parse_input(filename):
	file = open(filename, 'r')
	return [line.strip() for line in file.readlines()]

@cache
def presses_to_move(directions, positions):
	if len(directions) == 0:
		return 0, positions

	if len(positions) == 0:
		# print('cost', len(directions))
		return len(directions), positions

	pos = positions[0]
	new_pos = DIR_POS[directions[0]]
	
	vertical = ('v' if new_pos[0] > pos[0] else '^') * abs(new_pos[0] - pos[0])
	horizontal = ('>' if new_pos[1] > pos[1] else '<') * abs(new_pos[1] - pos[1])

	sequences = None
	# mind the gap
	if pos[1] == 0 and new_pos[0] == 0:
		sequences = [horizontal + vertical + 'A']
	elif pos[0] == 0 and new_pos[1] == 0:
		sequences = [vertical + horizontal + 'A']
	else:
		sequences = [vertical + horizontal + 'A', horizontal + vertical + 'A']

	min_presses = None
	min_presses_positions = None
	for sequence in sequences:
		presses, new_dir_pos = presses_to_move(sequence, positions[1:])
		new_dir_pos = tuple([new_pos]) + new_dir_pos

		rest_presses, new_dir_pos = presses_to_move(directions[1:], new_dir_pos)
		presses += rest_presses
		if min_presses is None or presses < min_presses:
			min_presses = presses
			min_presses_positions = new_dir_pos

	return min_presses, min_presses_positions

def presses_to_input(code, pos, dir_pos = tuple([DIR_START, DIR_START])):
	if len(code) == 0:
		return 0

	new_pos = NUM_POS[code[0]]

	vertical = ('v' if new_pos[0] > pos[0] else '^') * abs(new_pos[0] - pos[0])
	horizontal = ('>' if new_pos[1] > pos[1] else '<') * abs(new_pos[1] - pos[1])

	sequences = None
	# mind the gap
	if pos[1] == 0 and new_pos[0] == 3:
		sequences = [horizontal + vertical + 'A']
	elif pos[0] == 3 and new_pos[1] == 0:
		sequences = [vertical + horizontal + 'A']
	else:
		sequences = [vertical + horizontal + 'A', horizontal + vertical + 'A']

	min_presses = None
	for sequence in sequences:
		presses, new_dir_pos = presses_to_move(sequence, dir_pos)
		presses += presses_to_input(code[1:], new_pos, new_dir_pos)
		if min_presses is None or presses < min_presses:
			min_presses = presses

	return min_presses

def solve(filename, keypad_count):
	codes = parse_input(filename)
	# print(codes)

	complexities = 0
	for code in codes:
		presses = presses_to_input(code, pos = NUM_START, dir_pos = (DIR_START,) * keypad_count)
		numeric = int(code[0:-1])
		complexities += presses * numeric
	print('complexities', complexities)

solve('21_sample.txt', 2) # 126384
solve('21_input.txt', 2) # 157230

solve('21_input.txt', 25) # 195969155897936

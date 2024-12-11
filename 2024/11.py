# https://adventofcode.com/2024/day/11

def parse_input(filename):
	file = open(filename, 'r')
	line = file.readline().strip()
	return [int(number) for number in line.split(" ")]

def solve(filename, blinks):
	stones = parse_input(filename)

	for _ in range(blinks):
		# print(stones)
		i = 0
		while i < len(stones):
			stone = stones[i]
			if stone == 0:
				stones[i] = 1
			else:
				stone_str = str(stone)
				stone_len = len(stone_str)
				if stone_len % 2 == 0:
					stones[i] = int(stone_str[0:int(stone_len / 2)])
					stones.insert(i + 1, int(stone_str[int(stone_len / 2):]))
					i += 1
				else:
					stones[i] *= 2024
			i += 1


	print("stones", len(stones))

solve('11_sample.txt', 25)
solve('11_input.txt', 25)

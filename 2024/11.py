# https://adventofcode.com/2024/day/11

from functools import cache

def parse_input(filename):
	file = open(filename, 'r')
	line = file.readline().strip()
	return [int(number) for number in line.split(" ")]

@cache
def count_stones(stone, blinks):
	if blinks == 0:
		return 1
	if stone == 0:
		return count_stones(1, blinks - 1)
	stone_str = str(stone)
	stone_len = len(stone_str)
	if stone_len % 2 == 0:
		left = int(stone_str[0:int(stone_len / 2)])
		right = int(stone_str[int(stone_len / 2):])
		return count_stones(left, blinks - 1) + count_stones(right, blinks - 1)
	return count_stones(stone * 2024, blinks - 1)

def solve(filename, blinks):
	stones = parse_input(filename)
	print(sum([count_stones(stone, blinks) for stone in stones]))

solve('11_sample.txt', 25)	# 55312
solve('11_input.txt', 25)   # 193269

solve('11_sample.txt', 75)	# 65601038650482
solve('11_input.txt', 75)   # 193269

# https://adventofcode.com/2024/day/14

import math

def parse_input(filename):
	file = open(filename, 'r')

	robots = []
	for line in file.readlines():
		p, v = line.strip().split(' ')
		p = [int(n) for n in p.split('=')[1].split(',')]
		v = [int(n) for n in v.split('=')[1].split(',')]
		robots.append((p, v))

	return robots

def move_robot(robot, w, h, times):
	return ((robot[0][0] + robot[1][0] * times) % w, (robot[0][1] + robot[1][1] * times) % h)

def print_area(positions, w, h):
	positions = set(positions)
	for y in range(h):
		for x in range(w):
			if (x, y) in positions:
				print('*', end='')
			else:
				print(' ', end='')
		print('\n')

def solve(filename, w, h, seconds = 100):
	robots = parse_input(filename)
	# print(robots)

	positions = [move_robot(robot, w, h, seconds) for robot in robots]
	# print(positions)

	hw = math.floor(w / 2)
	hh = math.floor(h / 2)
	top_left = sum(pos[0] < hw and pos[1] < hh for pos in positions)
	top_right = sum(pos[0] > hw and pos[1] < hh for pos in positions)
	bottom_left = sum(pos[0] < hw and pos[1] > hh for pos in positions)
	bottom_right = sum(pos[0] > hw and pos[1] > hh for pos in positions)
	print('safety factor', top_left * top_right * bottom_left * bottom_right)

	return positions

solve('14_sample.txt', 11, 7)	# 12
solve('14_input.txt', 101, 103)	# 218619120

positions = solve('14_input.txt', 101, 103, 7055)
print_area(positions, 101, 103)

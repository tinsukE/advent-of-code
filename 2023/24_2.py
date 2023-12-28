# https://adventofcode.com/2023/day/24

import decimal
import numpy as np

decimal.getcontext().prec = 100

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	hailstones = []
	for line in [line.strip() for line in lines]:
		pos, vel = line.split(' @ ')
		pos = [decimal.Decimal(value) for value in pos.split(', ')]
		vel = [decimal.Decimal(value) for value in vel.split(', ')]
		hailstones.append((pos, vel))
	return hailstones

def advance_by(hail, t):
	pos, vel = hail
	return [pos[0] + vel[0] * t, pos[1] + vel[1] * t, pos[2] + vel[2] * t]

def intify(v):
	gcd = np.gcd.reduce(v)
	return np.divide(v, [gcd, gcd, gcd])

def normal(a, b, c):
	return np.cross(np.subtract(b, a), np.subtract(c, a))

def normalized(v):
	return v / np.linalg.norm(v)

def get_contact_point(normal, plane_dot, a1, a2):
	direction_a = np.subtract(a2, a1)
	normalized_direction_a = normalized(direction_a)

	return np.add(a1, normalized_direction_a * np.dot(normal, np.subtract(plane_dot, a1)) / np.dot(normal, normalized_direction_a))

# https://stackoverflow.com/a/74576891
def intersect_line_line(a1, a2, b1, b2):
    direction_a = np.subtract(a1, a2)
    direction_b = np.subtract(b1, b2)
    line = np.cross(direction_a, direction_b);
    cross_line_a = np.cross(line, direction_a);
    cross_line_b = np.cross(line, direction_b);

    return [get_contact_point(cross_line_a, a1, b1, b2), get_contact_point(cross_line_b, b1, a1, a2)]

def solve(filename):
	hailstones = parse_input(filename)

	# https://math.stackexchange.com/a/2789339
	B1 = hailstones[1][0]
	B2 = advance_by(hailstones[1], 1)
	print('B', B1, B2)
	C1 = hailstones[2][0]
	C2 = advance_by(hailstones[2], 1)
	print('C', C1, C2)

	def trace_line_at(t):
		A = advance_by(hailstones[0], t)
		normal1 = normal(A, B1, B2)
		normal2 = normal(A, C1, C2)
		if DEBUG: print('normals', normal1, normal2)
		direction = np.cross(normal1, normal2)
		if DEBUG: print('direction', direction)
		if direction[0] == 0 and direction[1] == 0 and direction[2] == 0:
			raise ValueError('Direction is 0, 0, 0')

		A1 = A + direction * 10000
		if DEBUG: print('A', A, A1)

		error = None
		for i, hail in enumerate(hailstones):
			x = intersect_line_line(A, A1, hail[0], advance_by(hail, 10))
			error = abs(x[0][0] - x[1][0]) + abs(x[0][1] - x[1][1]) + abs(x[0][2] - x[1][2])
			if error > EPSILON:
				if DEBUG or i != 3:
					print('failed at', i, 'error', error)
				break
		return (direction, error)

	current_t = 1
	delta_t = 1
	last_error = float('inf')
	min_t, max_t = None, None
	while True:
		direction, error = trace_line_at(current_t)
		if error < EPSILON:
			print('found the sucker!', current_t, direction)
			break
		if error < last_error:
			delta_t *= 10
			current_t += delta_t
			last_error = error
		else:
			min_t = current_t - delta_t
			max_t = current_t
			break
	if DEBUG: print('t is within', min_t, max_t)

	def binary_search(lower_t, upper_t):
		if DEBUG: print('searching within', lower_t, upper_t)
		lower_t_dir, lower_t_error = trace_line_at(lower_t)
		if lower_t_error < EPSILON:
			return lower_t, lower_t_dir
		upper_t_dir, upper_t_error = trace_line_at(upper_t)
		if upper_t_error < EPSILON:
			return upper_t, upper_t_dir

		if upper_t - lower_t < 2:
			raise ValueError('this should not happen')

		mid_t = lower_t + (upper_t - lower_t) // 2
		_, mid_t_error = trace_line_at(mid_t)
		_, mid_t_minus_1_error = trace_line_at(mid_t - 1)
		if DEBUG: print('errors', lower_t_error, mid_t_error, upper_t_error)

		if mid_t_minus_1_error < mid_t_error:
			return binary_search(lower_t, mid_t)
		else:
			return binary_search(mid_t, upper_t)

	t, direction = binary_search(1, max_t)
	direction = intify(direction)
	print(t, direction)

	A = advance_by(hailstones[0], t)
	origin = A - (direction * t)

	origin_sum = np.sum(origin)
	print(filename, 'origin_sum', origin_sum)

DEBUG = False
EPSILON = 0.001

solve('24_sample.txt')
solve('24_input.txt')

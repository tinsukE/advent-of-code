# https://adventofcode.com/2025/day/8

from collections import defaultdict

def parse_input(filename):
	file = open(filename, 'r')
	boxes = []
	for line in [line.strip() for line in file.readlines()]:
		boxes.append(tuple([int(num) for num in line.split(',')]))
	return boxes

def solve_1(filename, max_connections):
	boxes = parse_input(filename)

	distances = defaultdict(set)
	for i, box_a in enumerate(boxes):
		for box_b in boxes[i + 1:]:
			distance = (box_a[0] - box_b[0]) ** 2 + (box_a[1] - box_b[1]) ** 2 +  (box_a[2] - box_b[2]) ** 2
			distances[distance].add((box_a, box_b))
	distances = dict(sorted(distances.items()))

	circuits = []
	num_connections = 0

	while max_connections < 0 or num_connections < max_connections:
		lowest_distance = next(iter(distances))
		connections = distances[lowest_distance]
		connection = connections.pop()
		if len(connections) == 0:
			distances.pop(lowest_distance)

		# check box left and right
		box_a = connection[0]
		box_b = connection[1]
		circuit_a = next((x for x in circuits if box_a in x), None)
		circuit_b = next((x for x in circuits if box_b in x), None)

		num_connections += 1

		if circuit_a and circuit_a == circuit_b:
			# same circuit
			continue
		elif circuit_a and circuit_b:
			# join circuits
			circuit_a.update(circuit_b)
			circuits.remove(circuit_b)
			print
		elif circuit_a:
			# add box_b to circuit_a
			circuit_a.add(box_b)
		elif circuit_b:
			# add box_a to circuit_b
			circuit_b.add(box_a)
		else:
			# new circuit
			circuits.append(set([box_a, box_b]))

		if len(circuits[0]) == len(boxes):
			print("hallelujah!!!!", box_a[0] * box_b[0])
			return

	circuits.sort(key=lambda circuit: -len(circuit))
	print('product', len(circuits[0]) * len(circuits[1]) * len(circuits[2]))

solve_1('08_sample.txt', 10) # 40
solve_1('08_input.txt', 1000) # 121770

solve_1('08_sample.txt', -1) # 25272
solve_1('08_input.txt', -1) # 7893123992

# https://adventofcode.com/2023/day/24

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	hailstones = []
	for line in [line.strip() for line in lines]:
		pos, vel = line.split(' @ ')
		pos = tuple([int(value) for value in pos.split(', ')])
		vel = tuple([int(value) for value in vel.split(', ')])
		hailstones.append((pos, vel))
	return hailstones

def advance_by(hail, t):
	pos, vel = hail
	return (pos[0] + vel[0] * t, pos[1] + vel[1] * t, pos[2] + vel[2] * t)

def solve(filename):
	global DEBUG
	hailstones = parse_input(filename)
	if DEBUG:
		for hail in hailstones: print(hail)

	min_x, max_x = None, None
	min_y, max_y = None, None
	min_z, max_z = None, None
	for hail in hailstones:
		# pos_at_1 = advance_by(hail, 1)
		pos_at_1 = hail[0]
		if hail[1][0] > 0:
			max_x = pos_at_1[0] if max_x == None or pos_at_1[0] > max_x else max_x
		if hail[1][0] < 0:
			min_x = pos_at_1[0] if min_x == None or pos_at_1[0] < min_x else min_x
		if hail[1][1] > 0:
			max_y = pos_at_1[1] if max_y == None or pos_at_1[1] > max_y else max_y
		if hail[1][1] < 0:
			min_y = pos_at_1[1] if min_y == None or pos_at_1[1] < min_y else min_y
		if hail[1][2] > 0:
			max_z = pos_at_1[2] if max_z == None or pos_at_1[2] > max_z else max_z
		if hail[1][2] < 0:
			min_z = pos_at_1[2] if min_z == None or pos_at_1[2] < min_z else min_z
		pass

	if DEBUG:
		print('rock throw must be within:')
		print(min_x, '<= x <=', max_x)
		print(min_y, '<= y <=', max_y)
		print(min_z, '<= z <=', max_z)

	# hailstones_over_time = []
	# for t in range(1, len(hailstones) + 1):
	# 	hailstones_at_t = {}
	# 	for hail in hailstones:
	# 		pos_at_t = advance_by(hail, t)
	# 		if DEBUG and pos_at_t in hailstones_at_t: raise ValueError("Conflict!")
	# 		hailstones_at_t[pos_at_t] = hail
	# 	hailstones_over_time.append(hailstones_at_t)

	# if DEBUG:
	# 	print('hailstones_over_time')
	# 	for t, hails in enumerate(hailstones_over_time):
	# 		print(t + 1, hails)

	# for hail1 in hailstones:
	# 	for hail2 in hailstones:
	# 		if hail1 == hail2:
	# 			continue

	# 		pos1 = advance_by(hail1, 1)
	# 		pos2 = advance_by(hail2, 2)

	# 		delta = (pos2[0] - pos1[0], pos2[1] - pos1[1], pos2[2] - pos1[2])
	# 		origin = ((pos1[0] - delta[0], pos1[1] - delta[1], pos1[2] - delta[2]), delta)

	# 		if DEBUG and (advance_by(origin, 1) != pos1 or advance_by(origin, 2) != pos2): raise ValueError("FCK")

	# 		# matched_hails = {hail1, hail2}
	# 		found = True
	# 		for t in range(3, len(hailstones) + 1):
	# 			target = advance_by(origin, t)
	# 			hail_t = hailstones_over_time[t - 1].get(target)
	# 			# if hail_t == None or hail_t in matched_hails:
	# 			# 	break
	# 			# matched_hails.add(hail_t)
	# 			if hail_t == None:
	# 				found = False
	# 				break
	# 		# if len(matched_hails) == len(hailstones):
	# 		if found:
	# 			print('EUREKA', origin)

DEBUG = True
solve('24_sample.txt')
# solve('24_input.txt')

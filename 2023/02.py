# https://adventofcode.com/2023/day/2

file = open('02.in', 'r')
sum_possible_ids = 0
sum_power = 0
for line in file.readlines():
	game, cubes = line.split(':')

	game_id = int(game.split(' ')[1])
	print('game_id', game_id)

	cubes_samples = cubes.split(';')
	print('cubes_samples', cubes_samples)

	max_red = 0
	max_green = 0
	max_blue = 0
	for cubes_sample in cubes_samples:
		color_samples = cubes_sample.split(',')
		# print('color_samples', color_samples)
		for color_sample in color_samples:
			count, color = color_sample.strip().split(' ')
			count = int(count)
			# print(count, color)
			if color == 'red':
				max_red = count if count > max_red else max_red
			elif color == 'green':
				max_green = count if count > max_green else max_green
			elif color == 'blue':
				max_blue = count if count > max_blue else max_blue
	print('game_id', game_id, 'max_red', max_red, 'max_blue', max_blue, 'max_green', max_green)
	if max_red <= 12 and max_green <= 13 and max_blue <= 14:
		sum_possible_ids += int(game_id)
	sum_power += max_red * max_green * max_blue

print('sum_possible_ids', sum_possible_ids)
print('sum_power', sum_power)
# https://adventofcode.com/2024/day/9

def parse_input(filename):
	file = open(filename, 'r')
	line = [int(char) for char in file.readline().strip()]

	disk = []
	disk += line[0] * [0]

	i = 1
	file_id = 1
	while i < len(line):
		disk += line[i] * [None]
		disk += line[i + 1] * [file_id]
		i += 2
		file_id += 1

	return disk

def checksum(disk):
	checksum = 0
	i = 0
	while i < len(disk) and disk[i] != None:
		checksum += i * disk[i]
		i += 1
	return checksum

def solve(filename):
	disk = parse_input(filename)

	i = 0
	j = len(disk) - 1
	while i < j:
		if disk[i] != None:
			i += 1
			continue

		while i < j and disk[j] == None:
			j -= 1
		if i >= j:
			break

		disk[i] = disk[j]
		disk[j] = None
		i += 1

	disk_checksum = checksum(disk)
	print('disk_checksum', disk_checksum)

def parse_input_2(filename):
	file = open(filename, 'r')
	line = [int(char) for char in file.readline().strip()]

	files = []
	files.append([0, line[0], 0])

	free = []

	i = 1
	file_id = 1
	disk_len = line[0]
	while i < len(line):
		if line[i] > 0:
			free.append([disk_len, line[i]])
			disk_len += line[i]
		files.append([disk_len, line[i+1], file_id])
		disk_len += line[i+1]
		i += 2
		file_id += 1

	return files, free

def solve_2(filename):
	files, free_space = parse_input_2(filename)

	for file in reversed(files):
		for j, free in enumerate(free_space):
			if free[0] > file[0]:
				break
			if free[1] < file[1]:
				continue
			file[0] = free[0]
			if free[1] == file[1]:
				del free_space[j]
			else:
				free[0] += file[1]
				free[1] -= file[1]
			break

	checksum = 0
	for file in files:
		for i in range(file[1]):
			checksum += (file[0] + i) * file[2]
	print('checksum', checksum)

solve('09_sample.txt')	# 1928
solve('09_input.txt')	# 6288707484810

solve_2('09_sample.txt')	# 2858
solve_2('09_input.txt')		# 6311837662089

# https://adventofcode.com/2023/day/6

file = open('06.in', 'r')
lines = file.readlines()
times = [int(time) for time in lines[0].strip().split(':')[1].strip().split()]
distances = [int(distance) for distance in lines[1].strip().split(':')[1].strip().split()]

product = 1
for time, distance in zip(times, distances):
	sum_possibilities = 0
	for charge in range(time):
		if charge * (time - charge) > distance:
			sum_possibilities += 1
	product *= sum_possibilities
print('product', product)

file = open('06.in', 'r')
lines = file.readlines()
time = int(''.join(lines[0].strip().split(':')[1].strip().split()))
distance = int(''.join(lines[1].strip().split(':')[1].strip().split()))
print(time, distance)

sum_possibilities = 0
for charge in range(time):
	if charge * (time - charge) > distance:
		sum_possibilities += 1
print('sum_possibilities', sum_possibilities)
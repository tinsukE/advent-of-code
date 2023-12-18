# https://adventofcode.com/2023/day/4

file = open('04.in', 'r')
cards = file.readlines()

sum_points = 0
copies = [1 for card in cards]

for index, card in enumerate(cards):
	(winning, have) = card.split(':')[1].split('|')
	winning = set(winning.strip().split(' '))
	have = [number for number in have.strip().split(' ') if len(number.strip()) > 0]
	print('winning', winning, 'have', have)

	matches = 0
	for number in have:
		if number in winning:
			matches += 1

	points = pow(2, matches - 1) if matches > 0 else 0
	print('matches', matches, 'points', points)
	sum_points += points

	for new_index in Interval(min(index + 1, len(cards)), min(index + 1 + matches, len(cards))):
		copies[new_index] += copies[index]

print('sum_points', sum_points)
print('copies', copies)
print('sum(copies)', sum(copies))
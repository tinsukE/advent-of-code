# https://adventofcode.com/2023/day/7

from dataclasses import dataclass, field
from enum import Enum

class Rank(Enum):
	HIGH_CARD = 1
	ONE_PAIR = 2
	TWO_PAIR = 3
	THREE_OF_A_KIND = 4
	FULL_HOUSE = 5
	FOUR_OF_A_KIND = 6
	FIVE_OF_A_KIND = 7

CARD_STRENGTH = {
	'2': 0,
	'3': 1,
	'4': 2,
	'5': 3,
	'6': 4,
	'7': 5,
	'8': 6,
	'9': 7,
	'T': 8,
	'J': 9,
	'Q': 10,
	'K': 11,
	'A': 12,
}

@dataclass
class Hand:
	cards: str
	bid: int
	rank: Rank = field(init=False)

	def __post_init__(self):
		self.rank = Hand.calculate_rank(self.cards)

	def __lt__(self, other):
		rank_diff = self.rank.value - other.rank.value
		if rank_diff == 0:
			for index in range(len(self.cards)):
				if self.cards[index] == other.cards[index]:
					continue
				else:
					return CARD_STRENGTH[self.cards[index]] < CARD_STRENGTH[other.cards[index]]
			return False
		else:
			return rank_diff < 0

	def calculate_rank(cards):
		cards_accumulator = {}
		for card in cards:
			if card not in cards_accumulator:
				cards_accumulator[card] = 1
			else:
				cards_accumulator[card] += 1
		cards_repetition = list(cards_accumulator.values())
		if 5 in cards_repetition:
			return Rank.FIVE_OF_A_KIND
		elif 4 in cards_repetition:
			return Rank.FOUR_OF_A_KIND
		elif 3 in cards_repetition and 2 in cards_repetition:
			return Rank.FULL_HOUSE
		elif 3 in cards_repetition:
			return Rank.THREE_OF_A_KIND
		elif cards_repetition.count(2) == 2:
			return Rank.TWO_PAIR
		elif 2 in cards_repetition:
			return Rank.ONE_PAIR
		else:
			return Rank.HIGH_CARD

file = open('07.in', 'r')
lines = file.readlines()

hands = [Hand(line.strip().split()[0], int(line.strip().split()[1])) for line in lines]
hands.sort()
print(hands)
winnings = 0
for rank, hand in enumerate(hands):
	winnings += (rank + 1) * hand.bid
print('winnings', winnings)

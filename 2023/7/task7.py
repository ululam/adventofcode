import collections
from functools import cmp_to_key

# alphabet = "AKQJT98765432"        # Part1 Alphabet
alphabet = "AKQT98765432J"          # Part2 Alphabet
order = {c: alphabet.index(c) for c in alphabet}
factor = len(alphabet) + 1
# Big enough not to have intersection
PAIR = factor ** 7
TWO_PAIRS = factor ** 8
TRIPLES = factor ** 9
FULL = factor ** 10
QUAD = factor ** 11
FIVES = factor ** 12

def compare(a, b):
    return -(rank2(a[0]) - rank2(b[0]))

# Rank for Part2
def rank2(cards) -> (int, str):
    if "J" not in cards:
        return rank(cards)

    counts = collections.Counter(cards)
    if len(counts) == 1:    # All Jacks
        return rank(cards)

    max_comb_rank = max([combination_rank(cards.replace("J", char)) for char in counts if char != "J"])
    return max_comb_rank + high_card_rank(cards)

# Rank for Part1
def rank(cards) -> int:
    return combination_rank(cards) + high_card_rank(cards)

def combination_rank(cards):
    c = collections.Counter(list(cards))
    mc = c.most_common(5)
    top = mc[0]
    if top[1] == 5: return FIVES
    if top[1] == 4: return QUAD
    if top[1] == 3:
        if mc[1][1] == 2: return FULL
        return TRIPLES
    if top[1] == 2:
        if mc[1][1] == 2: return TWO_PAIRS
        return PAIR
    return 0

def high_card_rank(cards):
    return sum([value(c) * (len(alphabet) ** (5 - i)) for i, c in enumerate(cards)])

def value(card):
    return len(alphabet) - order[card]

def solve(f):
    cards_bids = [(line.split()[0], int(line.split()[1])) for line in f]
    cards_bids = sorted(cards_bids, key=cmp_to_key(compare))
    return sum([(len(cards_bids) - i) * v[1] for i, v in enumerate(cards_bids)])

with open("7.input") as f:
# with open("test7.txt") as f:
    print(solve(f))

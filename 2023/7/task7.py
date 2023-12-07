import collections
from functools import cmp_to_key

alphabet = "AKQJT98765432"
factor = len(alphabet) + 1
PAIR = factor ** 7
TWO_PAIRS = factor ** 8
TRIPLES = factor ** 9
FULL = factor ** 10
QUAD = factor ** 11
FIVES = factor ** 12

class Solution:
    def __init__(self) -> None:
        self.order = {c: alphabet.index(c) for c in alphabet}

    def compare(self, a, b):
        return -(self.rank(a[0])[0] - self.rank(b[0])[0])  # ???

    def rank(self, cards) -> (int, str):
        c = collections.Counter(list(cards))
        mc = c.most_common(5)
        top = mc[0]
        if top[1] == 5:
            # Five
            return FIVES + self.value(top[0]), "Five"
        top2 = mc[1]
        if top[1] == 4:
            # 4
            return QUAD + self.power(2) * self.value(top[0]) + self.value(top2[0]), "Quads"
        if top[1] == 3:
            if top2[1] == 2:
                # 3+2
                return FULL + self.power(2) * self.value(top[0]) + self.value(top2[0]), "Full"
            # 3
            leftover = sorted(cards.replace(top[0], ""))
            return TRIPLES + self.power(3) * self.value(top[0]) + self.power(2) * self.value(leftover[0]) + self.value(leftover[1]), "Triple"
        if top[1] == 2:
            if top2[1] == 2:
                # Two pairs. Find the top pair
                pairs = self.sort(top[0] + top2[0])
                return TWO_PAIRS + self.power(3) * self.value(pairs[0]) + self.power(2) * self.value(pairs[1]) + self.value(mc[2][0]), "Two pairs"
            else:
                # pair
                leftover = sorted(cards.replace(top[0], ""))
                return PAIR + self.power(4) * self.value(top[0]) + self.power(3) * self.value(leftover[0]) + self.power(2) * self.value(leftover[1]) + self.value(leftover[2]), "Pair"
        else:
            # High card
            sum = 0
            for i, c in enumerate(self.sort(cards)):
                factor = self.power((len(cards) - i))
                sum += factor * self.value(c)
            return sum, "High Card"

    def power(self, n):
        return len(alphabet) ** n

    def value(self, card):
        return len(self.order) - self.order[card]

    def sort(self, cards) -> list:
        return sorted(list(cards), key=lambda char: self.order[char])

    def part1(self, f):
        cards_bids = [(line.split()[0], int(line.split()[1])) for line in f]
        res = 0
        cards_bids = sorted(cards_bids, key=cmp_to_key(self.compare))
        for c in cards_bids:
            print("".join(self.sort(c[0])) + f"\t\t%{c[1]}")
        for i, v in enumerate(cards_bids):
            res += (i+1) * v[1]
        print(res)

def p(c):
    s = Solution()
    r = s.rank(c)
    print(f"{c} -> {r}")

# with open("7.input") as f:
with open("test7.txt") as f:
#     s = Solutioкn()z
    Solution().part1(f)


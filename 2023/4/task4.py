def to_numbers(s: str) -> list[int]:
    return [int(n) for n in s.strip().split(" ") if n]

def get_winning_cards_count(s: str) -> int:
    left, right = s.split(":")[1].split("|")
    left, right = to_numbers(left), to_numbers(right)
    return len([n for n in right if n in set(left)])

def get_line_points(s: str) -> int:
    count = get_winning_cards_count(s)
    return 1 << count - 1 if count else 0

def part1(f):
    print(sum([get_line_points(line.strip()) for line in f]))

def part2(f):
    from collections import defaultdict
    bonuses, cards_sum = defaultdict(int), 0
    for card, line in enumerate(f, 1):
        cards_number = bonuses[card] + 1
        cards_sum += cards_number
        # Each winning number adds bonus card to incremental level. That gonna be "cards_sum" extra cards
        for i in range(get_winning_cards_count(line)):
            bonuses[card+i+1] += cards_number
    print(cards_sum)

# with open("test4.txt") as f:
with open("4.input") as f:
    # part1(f)
    part2(f)

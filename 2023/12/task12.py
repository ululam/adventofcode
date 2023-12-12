# Use backtracking to find all variants
# Rely on memoization to squash n! into something close to O(n^2) + O(n^2) memory

def solve_line(s: str, factor) -> int:
    pattern, counts = s.split()
    counts = [int(c) for c in counts.split(",")]
    pattern = "?".join([pattern] * factor)
    counts = counts * factor
    return solve_pattern2(list(pattern), counts)


cache = {}
def solve_pattern2(pattern: list, counts: list[int]) -> int:
    a_key = "".join(pattern) + "__".join([str(c) for c in counts])
    if a_key in cache:
        return cache[a_key]

    group_started = False
    pattern = pattern[:]
    counts = counts[:]
    if counts and counts[0] == 0:
        counts = counts[1:]

    for i in range(len(pattern)):
        if pattern[i] == "#":
            group_started = True
            if not counts or counts[0] <= 0:
                return cache_and_return(a_key, 0)
            counts[0] -= 1
        elif pattern[i] == ".":
            if not group_started:
                continue
            if counts and counts[0] != 0:
                return cache_and_return(a_key, 0)
            counts = counts[1:]
            group_started = False
        else:        # "?"
            chars = []
            if (group_started and counts[0] == 0) or not group_started:
                # We are ok to add dot here
                chars.append(".")
            if (group_started and counts[0] > 0) or not group_started:
                chars.append("#")
            res = 0
            for c in chars:
                pattern[i] = c
                res += solve_pattern2(pattern[i:], counts)
            return cache_and_return(a_key, res)

    res = 0 if counts and sum(counts) > 0 else 1
    return cache_and_return(a_key, res)


def cache_and_return(key: str, value: int) -> int:
    cache[key] = value
    return value

def solve(f, factor: int = 1):
    from time import time
    start_time = time()
    total = sum([solve_line(line, factor) for line in f])
    print(f"Answer is: {total}")
    print(f"It took {'%.2f'%(time() - start_time)} seconds")


# with open("test12.txt") as f:
with open("12.input") as f:
    solve(f, 5)

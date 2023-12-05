from collections import defaultdict
from time import time

class Seeder:
    def __init__(self):
        self.seeds = None
        self.paths = defaultdict(list)
        self.mappings = {}
        self.paths_to_location = []
        self.seed_ranges = None
        self.min_location = -1

    def find_path_to_location(self, start: str):
        res = []
        for next in self.paths[start]:
            if next == "location":
                return ["location"]
            tail = self.find_path_to_location(next)
            if tail:
                return [next] + tail
        return res

    def read_seeds(self, seed_line: str):
        self.seeds = [int(n) for n in seed_line.split(":")[1].split(" ") if n]

    def read_map(self, lines):
        from_type, to_type = lines[0].split(" ")[0].split("-to-")
        self.paths[from_type].append(to_type)
        tuples = []
        for line in lines[1:]:
            t = [int(v) for v in line.split(" ")]
            tuples.append(t)
        self.mappings[f"{from_type}-to-{to_type}"] = sorted(tuples, key=lambda t: t[1])

    def get_mapping(self, key: int, map_name: str):
        mapping = self.mappings.get(map_name)
        for dest, source, range in mapping:
            if source <= key < source + range:
                return dest + (key - source)
        return key

    def binary_search_mapping(self, key: int, map_name: str):
        mapping = self.mappings.get(map_name)
        l, r = -1, len(mapping)
        while r - l > 1:
            mid = l + ((r - l) >> 1)
            dest, source, range = mapping[mid]
            if key < source:
                r = mid
            else:
                l = mid
        dest, source, range = mapping[l]
        if source <= key < source + range:
            return dest + (key - source)
        return key

    def read_input(self, f):
        lines = []
        for line in f:
            line = line.strip()
            if line.startswith("seeds"):
                self.read_seeds(line)
                continue
            if not line:          # Empty line
                if lines:
                    self.read_map(lines)
                    lines.clear()
                continue
            lines.append(line)
        if lines:       # Don't forget to read the remainder
            self.read_map(lines)

    def solution(self, f, seed_provider):
        self.read_input(f)
        paths_to_location = self.find_path_to_location("seed")
        self.min_location = float('inf')
        for seed in seed_provider():
            val, prev_el = seed, "seed"
            for el in paths_to_location:
                # val, prev_el = self.get_mapping(val, f"{prev_el}-to-{el}"), el
                val, prev_el = self.binary_search_mapping(val, f"{prev_el}-to-{el}"), el
            self.min_location = min(self.min_location, val)
        print(self.min_location)

    def get_seeds1(self):
        return self.seeds

    def seeds_to_ranges(self):
        self.seed_ranges = []
        summa = 0
        for i in range(0, len(self.seeds), 2):
            start, length = self.seeds[i], self.seeds[i+1]
            summa += length
            self.seed_ranges.append([start, start+length])
        print(f"Total seeds: {summa}")
        print(f"Total ranges: {len(self.seed_ranges)}")

    def seeds_count(self, ranges=None):
        ranges = ranges if ranges else self.seed_ranges
        return sum([t[1]-t[0] for t in ranges])

    def get_seeds2(self):
        count = 0
        if not self.seed_ranges:
            self.seeds_to_ranges()
        start_time = time()
        self.seed_ranges = sorted(self.seed_ranges, key=lambda r: r[1]-r[0])
        for r in self.seed_ranges:
            print(f"{r} ({round((r[1] - r[0])/1_000_000)}M), ttp ~ {(r[1] - r[0])/200_000} s")

        ranges = self.seed_ranges[:5]
        # ranges = self.seed_ranges[5:8]
        # ranges = self.seed_ranges[8:]
        print(f"============ RUNNING FOR {ranges} ============")
        for start, end in ranges:
            print(f"> Starting [{start}, {end}] ({round((end-start)/1_000_000)}M), ttp ~ {(end-start)/200_000} s")
            range_count = 0
            for v in range(start, end):
                count += 1
                range_count += 1
                if count % 10_000_000 == 0:
                    elapsed = time() - start_time   # seconds
                    speed = count/elapsed
                    eta = (self.seeds_count(ranges) - count) / speed
                    eta_range = (end - start - range_count) / speed
                    print(f"\tProcessed {count} in {round(100*elapsed)/100}s, {round(0.001*speed)}k per sec, remaining = {round(eta/60)} mins, remaning_range = {round(eta_range)}s")
                yield v
            print(f"*** [{start}, {end}] --min--> {self.min_location}")

    def part1(self, f):
        self.solution(f, self.get_seeds1)

    def part2(self, f):
        self.solution(f, self.get_seeds2)

# with open("test5.txt") as f:
with open("5.input") as f:
    # Seeder().part1(f)
    Seeder().part2(f)

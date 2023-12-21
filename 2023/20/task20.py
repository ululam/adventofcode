import math
from collections import deque, defaultdict
from enum import Enum


class Pulse(Enum):
    HIGH = "high"
    LOW = "low"

    def __str__(self) -> str:
        return self.value


class E:
    def __init__(self, e_type: str = None, name: str = None, output: list = None) -> None:
        self.e_type = e_type
        self.name = name
        self.output = output if output else []

    def __str__(self) -> str:
        return f"{self.e_type if self.e_type else ''}{self.name} -> {self.output}"

    def __repr__(self) -> str:
        return self.__str__()

    def process(self, pulse: Pulse, from_name: str) -> (Pulse | None, list[str]):
        return None, self.output

    def status(self) -> str:
        return ""

    @staticmethod
    def create(definition):
        tp_out = definition.split(" -> ")
        e_type = None
        name = tp_out[0]
        if not tp_out[0][0].isalpha():
            e_type = tp_out[0][0]
            name = tp_out[0][1:]
        output = tp_out[1].split(", ")

        if name == "broadcaster":
            return Broadcaster(e_type, name, output)
        if e_type == "%":
            return FF(name, output)
        if e_type == "&":
            # Input to be filled later
            return Con([], name, output)

class Broadcaster(E):
    def process(self, pulse: Pulse, from_name: str):
        return Pulse.LOW, self.output

# XOR with itself
class FF(E):
    def __init__(self, name: str = None, output: list = None) -> None:
        super().__init__("%", name, output)
        self.on = False

    def process(self, pulse: Pulse, from_name: str) -> (Pulse | None, list[str]):
        if pulse == Pulse.HIGH:
            return None, []
        if not self.on:
            self.on = True
            return Pulse.HIGH, self.output
        self.on = False
        return Pulse.LOW, self.output

    def status(self) -> str:
        return f"{self.on}"

# Barrier (NAND)
# High & all others are high -> low
# Low or any of others (except from) is low -> high
class Con(E):
    def __init__(self, input: list[str], name: str = None, output: list = None) -> None:
        super().__init__("&", name, output)
        self.input = None
        self.memory = None
        self.set_input(input)

    def set_input(self, input):
        self.input = input
        self.memory = {k: Pulse.LOW for k in input}

    def process(self, pulse: Pulse, from_name: str) -> (Pulse | None, list[str]):
        self.memory[from_name] = pulse
        for v in self.memory.values():
            if v == Pulse.LOW:
                return Pulse.HIGH, self.output
        return Pulse.LOW, self.output

    def status(self) -> str:
        return ",".join(f"{k}->{self.memory[k]}" for k in sorted(self.input))

class Output(E):
    pass

class Universe:
    def __init__(self, mapping: dict[str, E]) -> None:
        self.mapping = mapping
        self.queue = deque()
        self.pulses_count = {Pulse.LOW: 0, Pulse.HIGH: 0}
        self.cycles = {k: 0 for k in ['rz', 'lf', 'br', 'fk']}

    def push_button(self, buttons_pressed):
        q = self.queue
        q.append(("button", Pulse.LOW, "broadcaster"))

        # ['rz', 'lf', 'br', 'fk'] -> lb -> rx
        while q:
            from_name, pulse, to_name = q.popleft()
            self.pulses_count[pulse] += 1
            if to_name == "lb" and pulse == Pulse.HIGH:
                print(f"Found {from_name}")
                self.cycles[from_name] = buttons_pressed

            e = self.mapping.get(to_name)
            if not e:
                continue
            # print(f"{from_name} -{pulse}-> {name}")
            pulse, output = e.process(pulse, from_name)
            if output:
                for out in output:
                    q.append((to_name, pulse, out))
        return self.pulses_count, self.status()

    # Just a helper method to understand tail connections
    def build_reverse(self):
        visited = set()

        def talk_to_me(signal, name):
            if name in visited:
                return
            visited.add(name)
            print(f"We need to get {signal} at {name}")
            res = []
            for k, v in self.mapping.items():
                if name in v.output:
                    res.append(k)
            print(f"To get there, we need to receive {signal} from {res}")
            for r in res:
                talk_to_me(signal, r)

        talk_to_me(Pulse.LOW, "rx")

    @staticmethod
    def create(f):
        mapping = {}
        for line in f:
            e = E.create(line.strip())
            mapping[e.name] = e
        o = Output("[X]", "output")
        mapping[o.name] = o
        for e in mapping.values():
            if isinstance(e, Con):
                input = []
                for other in mapping.values():
                    if e.name in other.output:
                        input.append(other.name)
                e.set_input(input)
        return Universe(mapping)

    def status(self) -> int:
        state = " | ".join([f"{k} => {self.mapping[k].status()}" for k in sorted(self.mapping.keys())])
        # print(state)
        return hash(state)

# with open("test20.txt") as f:
# with open("test20.1.txt") as f:
with open("20.input") as f:
    u = Universe.create(f)
    # u.build_reverse)
    button_presses = 0
    while True:
        button_presses += 1
        counts, status = u.push_button(button_presses)
        if all(u.cycles.values()):
            break
    print(u.cycles)
    # total = counts[Pulse.LOW] * counts[Pulse.HIGH]
    # print(f"Answer 1 is: {total}")
    print(f"Answer 2 is: {math.lcm(*u.cycles.values())}")

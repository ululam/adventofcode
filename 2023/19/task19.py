VALUE_RANGE = (1, 4000) # Left included, right excluded
ALL_ACCEPTED = {name: VALUE_RANGE for name in list("xmas")}

class Rule:
    def __init__(self, name: str, body: str) -> None:
        self.name = name
        self.body = body
        if ":" in body:
            self.condition, self.action = body.split(":")
            self.more_than = ">" in self.condition
            self.var, threshold = self.condition.split(">") if self.more_than else self.condition.split("<")
            self.threshold = int(threshold)
        else:
            self.var = "*"
            self.condition = ""
            self.more_than = False
            self.threshold = float('inf')
            self.action = body
        if self.more_than:
            self.fun = lambda v: self.action if v > self.threshold else None
        else:
            self.fun = lambda v: self.action if v < self.threshold else None

    def applicable(self, var: str):
        return self.var == "*" or self.var == var

    def apply(self, part: dict[str, int]) -> str:
        if self.var == "*":
            return self.action
        value = part.get(self.var)
        if not value:
            return None
        return self.fun(value)

    def __str__(self) -> str:
        return self.name + "{" + self.body + "}"

class RulePart2:
    def __init__(self, name: str, body: str, inversed: str = None) -> None:
        self.name = name
        self.body = body
        self.inversed = inversed
        self.cond_list = []
        if ":" in body:
            self.condition, self.action = body.split(":")
            self.cond_list = self.condition.split(" and ")
        else:
            self.var = "*"
            self.condition = "1=1"
            self.more_than = False
            self.threshold = float('inf')
            self.action = body

    def inverse(self):
        if self.inversed:
            return self.inversed
        body = list(self.body)
        for i in range(len(body)):
            if body[i] == ">":
                if body[i+1] == "=":
                    body[i] = "<"
                    body[i+1] = ""
                else:
                    body[i] = "<="
            elif body[i] == "<":
                if body[i + 1] == "=":
                    body[i] = ">"
                    body[i + 1] = ""
                else:
                    body[i] = ">="
        rule = RulePart2(None, "".join(body), self.body)
        return rule

    def get_apply_to_ranges(self):
        res = ALL_ACCEPTED.copy()
        if self.var != "*":
            if self.more_than:
                res[self.var] = (self.threshold + 1, VALUE_RANGE[1])
            else:
                res[self.var] = (VALUE_RANGE[0], self.threshold - 1)
        return res

    def __str__(self) -> str:
        return self.name + "{" + self.body + "}"


def read_rules(f) -> dict[str, dict[str, object]]:
    res = {}
    for line in f:
        if line == "\n":
            break
        name, rules = line.strip().split("{")
        rules_list = []
        prev_rules_in_line = []
        for rule_body in rules.replace("}", "").split(","):
            extra_cond = " and ".join([r.condition for r in prev_rules_in_line])
            if extra_cond:
                if ":" in rule_body:
                    rule_body = extra_cond + " and " + rule_body
                else:
                    rule_body = extra_cond + ":" + rule_body
            a_rule = RulePart2(name, rule_body)
            prev_rules_in_line = [a_rule.inverse()]
            rules_list.append(a_rule)
        res[name] = rules_list
    return res

def read_input(f):
    res = []
    for line in f:
        parts = line.strip().replace("{", "").replace("}", "").split(",")
        res.append({part.split("=")[0]: int(part.split("=")[1]) for part in parts for eq in part.split("=")})
    return res

def process(rules, input):
    res = 0
    for part in input:
        next_rule = "in"
        while next_rule != 'A' and next_rule != 'R':
            for rule in rules[next_rule]:
                next_rule = rule.apply(part)
                if next_rule:
                    break

        res += sum(part.values()) if next_rule == 'A' else 0
    return res

depth = [0]
def walk_rules_tree(rules: dict[str, list[Rule]]) -> list:

    # print(f"{tab}> get_rule_range: {rule} {'A' if is_accepted else 'R'}, current_range = {current_range}")
    all_chains = []

    def bt(rule, ranges_chain: list):
        tab = "\t" * depth[0]
        print(f"{tab}get_rule_range: {rule}, range = {rule.body}")
        if rule.action == 'A':
            print(f"{tab} >>> A")
            all_chains.append(" and ".join([c for c in ranges_chain if c]))
            print(f"{tab}[!] Added {ranges_chain}")
            return
        if rule.action == 'R':
            print(f"{tab} --- R")
            return
        child_rules = rules[rule.action]
        for child in child_rules:
            # ranges_chain.append(child.condition)
            depth[0] += 1
            bt(child, ranges_chain + [child.condition])
            depth[0] -= 1
            # ranges_chain.pop()

    santinel_rule = Rule("santinel", "in")
    bt(santinel_rule, [])
    # print(f"{tab}< get_rule_range: {rule} {'A' if is_accepted else 'R'} ---------> {res}")
    return all_chains

def build_range(conditions: str):
    range4 = {}
    for cond in conditions.split(" and "):
        more_than = (">" in cond)
        var_threshold = cond.split(">") if more_than else cond.split("<")
        var, threshold = var_threshold[0], var_threshold[1]
        if var not in range4:
            range4[var] = VALUE_RANGE
        if range4[var][0] < 0:
            return range4   # Dead end
        addon = 0
        if threshold.startswith("="):
            threshold = threshold.replace("=", "")
            addon = -1 if more_than else 1
        threshold = int(threshold) + addon
        if more_than:
            range1 = (threshold+1, 4000)
        else:
            range1 = (1, threshold)
        if range4[var][0] > range1[1] or range1[0] > range4[var][1]:
            range4[var] = (-1, 0)
        range4[var] = (max(range4[var][0], range1[0]), min(range4[var][1], range1[1]))
    return range4

with open("test19.txt") as f:
# with open("19.input") as f:
    rules = read_rules(f)
    # Part 1
    # print(process(rules, read_input(f)))

    # Part 2
    r = walk_rules_tree(rules)
    all_power = 0
    for chain in r:
        print(chain)
        br = build_range(chain)
        print(br)
        chain_power = 1
        count = 0
        for r in br.values():
            count += 1
            if r[0] > r[1]:
                chain_power = 0
                break
            chain_power *= r[1] - r[0] + 1
        for i in range(count, 4):
            chain_power *= 4000
        # print(f"Adding: {chain_power}")
        all_power += chain_power
    print(all_power)


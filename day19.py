import re, math
from pprint import pp
import functools

from multiprocessing import Pool

class Workflow:
    def __init__(self, name, final_rule, rules=None):
        self.name = name
        self.rules = rules if rules else []
        self.final_rule = final_rule

    def evaluate(self, part):
        for rule in self.rules:
            res = rule.evaluate(part)
            if res:
                return res
        return self.final_rule

    def fancy_evaluate(self, workflows, part):
        for rule in self.rules:
            res = rule.evaluate(part)
            if res:
                if res in ['A', 'R']:
                    return res
                else:
                    next_flow = workflows[res]
                    flow_res = next_flow.fancy_evaluate(workflows, part)
                    return flow_res

        if self.final_rule in ['A', 'R']:
            return self.final_rule
        else:
            next_flow = workflows[self.final_rule]
            flow_res = next_flow.fancy_evaluate(workflows, part)
            return flow_res


class Rule:
    def __init__(self, variable, operator, operand, target):
        self.variable = variable
        self.operator = operator
        self.operand = operand
        self.target = target

    def evaluate(self, part):
        return self.target if eval(f"{part[self.variable]} {self.operator} {self.operand}") else False

    def __str__(self):
        return f"{self.variable} {self.operator} {self.operand} -> {self.target}"

    def __repr__(self):
        return self.__str__()


def part1(input_path="input/day19.tim.txt"):
    with open(input_path) as inputfile:
        # with open("input/day19.txt") as inputfile:
        workflows = {}
        main_re = r"(?P<name>\w+){(?P<rules>(?:\w+\W\d+:\w+,)+)(?P<final_rule>\w+)}"
        rule_re = r"(?P<variable>\w+)(?P<operator>\W)(?P<operand>\d+):(?P<target>\w+),"
        reading_rules = True

        parts = []
        for row in inputfile:
            if row.strip() == '':
                reading_rules = False
                continue
            if reading_rules:
                main_match = re.match(main_re, row)
                name = main_match.group('name')
                rule_string = main_match.group('rules')
                final_rule = main_match.group('final_rule')
                workflow = Workflow(name, final_rule)
                for match in re.finditer(rule_re, rule_string):
                    # pp(match.group())
                    workflow.rules.append(Rule(
                        match.group('variable'),
                        match.group('operator'),
                        match.group('operand'),
                        match.group('target'),
                    ))
                workflows[name] = workflow
            else:
                part = {k: v for k, v in [x.split('=') for x in row.strip().strip('{}').split(',')]}
                parts.append(part)

        total_part_sum = 0
        for part in parts:
            if workflows['in'].fancy_evaluate(workflows, part) == 'A':
                total_part_sum += sum([int(v) for v in part.values()])
        print(total_part_sum)
    return workflows, parts


def explore(workflows, workflow_name='in', rules=None):
    rules = rules if rules else []
    if workflow_name == 'R':
        return False
    elif workflow_name == 'A':
        # print(rules)
        return [rules]
    else:
        # return [explore(workflows, rule.target, [*rules, (workflow_name, rule)]) for rule in workflows[workflow_name].rules]
        ret_rules = []
        for rule in workflows[workflow_name].rules:
            res = explore(workflows, rule.target, [*rules, (workflow_name, rule)])
            if res:
                ret_rules.extend(res)
        return ret_rules


def process_set(limits, x_values=range(1, 4000), m_values=range(1, 4000), a_values=range(1, 4000), s_values=range(1, 4000) ):
    counter = 0
    for x in x_values:
        for m in m_values:
            print(f"{x},{m}")
            for a in a_values:
                for s in s_values:
                    for limit_set in limits:
                        if (limit_set['x'][0] <= x <= limit_set['x'][1]
                                and limit_set['m'][0] <= m <= limit_set['m'][1]
                                and limit_set['a'][0] <= a <= limit_set['a'][1]
                                and limit_set['s'][0] <= s <= limit_set['s'][1]):
                            counter += 1
    return counter

def part2(input_path="input/day19.sample.txt"):
    workflows, parts = part1(input_path)
    print("\nPart 2:")

    chain_limits = []
    chains = explore(workflows)
    # print(chains)
    for chain in chains:
        non_inclusive_limits = {
            'x': [0, 4001],
            'm': [0, 4001],
            'a': [0, 4001],
            's': [0, 4001],
        }
        for workflow_name, rule in chain:
            operand = int(rule.operand)
            if rule.operator == '<' and non_inclusive_limits[rule.variable][1] > operand:
                non_inclusive_limits[rule.variable][1] = operand
            elif rule.operator == '>' and non_inclusive_limits[rule.variable][0] < operand:
                non_inclusive_limits[rule.variable][0] = operand
        chain_limits.append({k: [v[0] + 1, v[1] - 1] for k, v in non_inclusive_limits.items()})
        # pp(non_inclusive_limits)
        # sizes = [mx-mn-2 for mn, mx in non_inclusive_limits.values()]
        # pp(sizes)
        # print(functools.reduce(lambda a, b: a*b, sizes))
    # pp(chain_limits)

    print("[")
    for entry in zip(chains, chain_limits):
        print(f" (\n   {entry[0]},\n   {entry[1]}\n ),")
    print("]")
    # print(f"{entry[1]} <== {entry[0]}")

    counter = 0
    results = []
    with Pool(processes=4) as pool:
        # The lists are processed one after another,
        # but the items are processed in parallel.
        results.append(pool.starmap(process_set, [
            (chain_limits, range(1,1001)),
            (chain_limits, range(1001,2001)),
            (chain_limits, range(2001,3001)),
            (chain_limits, range(3001,4001))
        ]))
        print(results)
        # counter += pool.starmap(process_set, zip(chain_limits, list(range(1,1001))))
        # counter += pool.starmap(process_set, zip(chain_limits, list(range(1001,2001))))
        # counter += pool.starmap(process_set, zip(chain_limits, list(range(2001,3001))))
        # counter += pool.starmap(process_set, zip(chain_limits, list(range(3001,4001))))
    print(counter)
    print(results)
    exit()

    def get_intersection(chain_a, chain_b):
        return {k: [max(chain_a[k][0], chain_b[k][0]), min(chain_a[k][1], chain_b[k][1])] for k, v in chain_a.items()}

    def get_combinations(chain_a):
        return math.prod([max(v) - min(v) + 1 for v in chain_a.values()])

    inter = get_intersection(chain_limits[0], chain_limits[1])
    print(inter)
    combos = get_combinations(chain_limits[0]) + get_combinations(chain_limits[0]) - get_combinations(inter)
    print(f"Actual:  {combos}")
    print(f"Correct: {167409079868000}")
    print(combos == 167409079868000)

    # def multinomial_coefficient_single(data):
    #     total_values = sum([max(v) - min(v) + 1 for v in data.values()])
    #     return [math.comb(total_values, len(v) - (min(v) - 1)) for v in data.values()]
    #
    # def multinomial_coefficient_multiple(data):
    #     coefficients = [multinomial_coefficient_single(d) for d in data]
    #     return math.prod([math.comb(sum(c), c) for c in coefficients])
    #
    # unique_combinations = multinomial_coefficient_multiple(chain_limits)
    # print(unique_combinations)
    #
    # overall_non_inclusive_limits = {
    #     'x': [functools.reduce(min, [v['x'][0] for v in chain_limits]), functools.reduce(max, [v['x'][1] for v in chain_limits])],
    #     'm': [functools.reduce(min, [v['m'][0] for v in chain_limits]), functools.reduce(max, [v['m'][1] for v in chain_limits])],
    #     'a': [functools.reduce(min, [v['a'][0] for v in chain_limits]), functools.reduce(max, [v['a'][1] for v in chain_limits])],
    #     's': [functools.reduce(min, [v['s'][0] for v in chain_limits]), functools.reduce(max, [v['s'][1] for v in chain_limits])],
    # }
    # # print(overall_non_inclusive_limits)
    # sizes = [mx-mn-2 for mn, mx in overall_non_inclusive_limits.values()]
    # # pp(sizes)
    # print(functools.reduce(lambda a, b: a*b, sizes))

    # sample val: 167409079868000
    # compare to: 86271264186651


if __name__ == '__main__':
    part2()

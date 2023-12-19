
import re
from pprint import pp

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
        return f"{self.variable} {self.operator} {self.operand}"

def part1():
    with open("input/day19.txt") as inputfile:
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


def part2():
    with open("input/dayX") as inputfile:
        for row in inputfile:
            pass


if __name__ == '__main__':
    part1()



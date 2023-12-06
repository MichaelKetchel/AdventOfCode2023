from collections import defaultdict


def part1():
    def adjacent_symbol(data, x, y):
        adjacent = False
        for scan_y in range(y-1, y+2):
            if scan_y < 0 or scan_y >= len(data):
                continue
            for scan_x in range(x-1, x+2):
                if scan_x < 0 or scan_x >= len(data[scan_y]):
                    continue
                if not data[scan_y][scan_x].isdigit() and data[scan_y][scan_x] != '.':
                    adjacent = True
        return adjacent


    with open("input/day3.txt") as inputfile:
        file_data = [row.strip() for row in inputfile]
        part_number_sum = 0
        current_number = ""
        tracking_number = False
        keep_number = False
        for y, row in enumerate(file_data):
            for x, cell in enumerate(row):
                if cell.isdigit():
                    tracking_number = True
                    current_number += cell
                    if adjacent_symbol(file_data, x, y):
                        keep_number = True
                if not cell.isdigit() or x == len(row) - 1:
                    if tracking_number:
                        tracking_number = False
                        print(f"Found number {current_number}; is part: {keep_number}")
                        if keep_number:
                            part_number_sum += int(current_number)
                        current_number = ''
                        keep_number = False
        print(f"Sum of part numbers is: {part_number_sum}")


def part2():
    def adjacent_gear(data, x, y):
        adjacent_gears = []
        for scan_y in range(y - 1, y + 2):
            if scan_y < 0 or scan_y >= len(data):
                continue
            for scan_x in range(x - 1, x + 2):
                if scan_x < 0 or scan_x >= len(data[scan_y]):
                    continue
                if data[scan_y][scan_x] == '*':
                    adjacent_gears.append((scan_x, scan_y))
        return adjacent_gears

    with open("input/day3.txt") as inputfile:
        file_data = [row.strip() for row in inputfile]
        ratio_sum = 0
        current_number = ""
        tracking_number = False
        adjacent_gears = []
        gear_sets = defaultdict(list)
        for y, row in enumerate(file_data):
            for x, cell in enumerate(row):
                if cell.isdigit():
                    tracking_number = True
                    current_number += cell
                    adjacent_gears.extend(adjacent_gear(file_data, x, y))
                if not cell.isdigit() or x == len(row)-1:
                    if tracking_number:
                        tracking_number = False
                        # print(f"Found number {current_number}; adjacent gears: {adjacent_gears}")
                        if len(adjacent_gears):
                            adjacent_gears = list(set([i for i in adjacent_gears]))
                            for gear_position in adjacent_gears:
                                gear_sets[gear_position].append(int(current_number))
                        current_number = ''
                        adjacent_gears = []

        filtered = dict(filter(lambda item: len(item[1]) == 2, gear_sets.items()))
        for v in filtered.values():
            ratio_sum += v[0]*v[1]
        print(f"Sum of gear ratios is: {ratio_sum}")


# 28501754 too low
# 84633828 too low
# 86841457

if __name__ == '__main__':
    part2()


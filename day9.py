import numpy as np

def part1():
    def recurse_this(row):
        diffs = np.diff(row)
        # print(f"diffs{diffs}")
        if (len(set(diffs)) ==1 ):
            # We've found the final sequence
            # print("End found, do cool shit now")
            return row[-1] + diffs[1]
        else:
            # print("gotta go deeper")
            final_val = recurse_this(diffs)
            return row[-1] + final_val

    with open("input/day9.txt") as inputfile:
        total_nums = 0
        for row in inputfile:
            next_val = recurse_this([int(a) for a in row.split(' ')])
            print(f"Extrapolated value is {next_val}")
            total_nums += next_val
        print(f"Final value: {total_nums}")

# Not 1641920653
#
def part2():
    def recurse_this(row):
        diffs = np.diff(row)
        # print(f"diffs{diffs}")
        if (len(set(diffs)) == 1):
            # We've found the final sequence
            # print("End found, do cool shit now")
            return row[0] - diffs[1]
        else:
            # print("gotta go deeper")
            final_val = recurse_this(diffs)
            return row[0] - final_val

    with open("input/day9.txt") as inputfile:
        total_nums = 0
        for row in inputfile:
            next_val = recurse_this([int(a) for a in row.split(' ')])
            print(f"Extrapolated value is {next_val}")
            total_nums += next_val
        print(f"Final value: {total_nums}")


if __name__ == '__main__':
    part2()



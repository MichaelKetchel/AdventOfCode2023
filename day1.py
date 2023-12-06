# This is a sample Python script.
import re

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def part1():
    sum = 0
    with open("input/day1p1") as inputfile:
        for row in inputfile:
            digits = re.findall('\d', row)
            number = digits[0]+digits[-1]
            sum += int(number)
        print(sum)

def part2():
    numwords = {
        "one": 1,
        "two": 2,
        "three": 3 ,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven":7 ,
        "eight": 8,
        "nine": 9,
    }
    regex = r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))'
    total = 0

    def word_to_num(word):
        if len(word) > 1:
            return str(numwords[word])
        else:
            return word

    # with open("input/subset.txt") as inputfile:
    with open("input/day1p1") as inputfile:
        for row in inputfile:
            digits = re.findall(regex, row)
            total += int(''.join([word_to_num(x) for x in [digits[0], digits[-1]]]))

            # print(digits)
            # pair = [digits[0], digits[-1]]
            # converted = [word_to_num(x) for x in pair]
            # value = int(''.join(converted))
            # # print(converted)
            # # print(f"{row.strip()} | {pair} => {converted} = {value}")
            # # print(value)
            # total += value

        print(total)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    part2()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

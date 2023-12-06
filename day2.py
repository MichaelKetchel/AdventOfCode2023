import functools
import re
from functools import reduce

def part1():
    limits = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    with open("input/day2.txt") as inputfile:
        game_total = 0
        for row in inputfile:
            possible = True

            [game, game_run] = row.split(':')
            rounds = [play.split(',') for play in game_run.split(';')]
            print(game)
            for round in rounds:
                colors = {
                    'red': 0,
                    'green': 0,
                    'blue': 0
                }

                for pair in round:
                    [count, color] = pair.strip().split(' ')
                    colors[color] += int(count)

                print(colors)
                for color in colors.keys():
                    if colors[color] > limits[color]:
                        # impossible
                        print("IMPOSSIBRU")
                        possible = False

            if possible:
                game_total += int(game.strip().split(' ')[1])

        print(game_total)



def part2():
    with open("input/day2.txt") as inputfile:
        game_total = 0
        for row in inputfile:
            colors = {
                'red': 0,
                'green': 0,
                'blue': 0
            }

            [game, game_run] = row.split(':')
            rounds = [play.split(',') for play in game_run.split(';')]
            print(game)

            for round in rounds:
                for pair in round:
                    [count, color] = pair.strip().split(' ')
                    colors[color] = max(colors[color], int(count))

            total = functools.reduce(lambda x, y: x*y, colors.values())
            print(game_run)
            print(colors, total)
            game_total += total
        print(game_total)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    part2()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import heapq
from queue import PriorityQueue
from colorama import just_fix_windows_console, Fore, Back, Style
import heapq
from queue import PriorityQueue, Queue

just_fix_windows_console()


def get_neighbors(r, c, matrix):
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]):
            neighbors.append((nr, nc, dr, dc))
    return neighbors


def sum_path(matrix, path):
    total = 0
    for step in path:
        x, y = step
        # print(matrix[y][x], end='')
        total += matrix[y][x]
    print()
    return total


def print_in_technicolor(data, path, node_of_interest=(-1, -1), arrows=False):
    # in (row, column)
    arrow_map = {
        (0, 0): 'X',
        (1, 0): 'v',
        (-1, 0): '^',
        (0, 1): '>',
        (0, -1): '<',
    }
    clean_path = [a[:2] for a in path]
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            if (row_index, col_index) == node_of_interest[:2]:
                print(Back.RED + Fore.BLACK + str(value) + Style.RESET_ALL + " ", end='')
                continue

            if (row_index, col_index) in clean_path:
                if arrows:
                    index = clean_path.index((row_index, col_index))
                    path_entry = path[index]
                    print(Back.GREEN + Fore.BLACK + arrow_map[tuple(path_entry[2:4])] + Style.RESET_ALL + " ", end='')
                else:
                    print(Back.GREEN + Fore.BLACK + str(value) + Style.RESET_ALL + " ", end='')
                continue

            print(str(value) + " ", end='')
        print()
    print()


def part1():
    with open("input/day17.txt") as inputfile:
        # with open("input/day17.sample.txt") as inputfile:
        the_data = [[int(x) for x in y] for y in [x.strip() for x in inputfile]]
        start = (0, 0)
        end = (len(the_data) - 1, len(the_data[0]) - 1)
        seen = set()
        the_queue = [(0, *start, 0, 0, 0, [(*start, 0, 0)])]

        while the_queue:
            heat_loss, row, col, dir_row, dir_col, steps, path = heapq.heappop(the_queue)

            if (row, col) == end:
                print(heat_loss)
                # print(path)
                print(f"Sum of displayed path: {sum_path(the_data, [(state[1], state[0]) for state in path][1:])}")
                print_in_technicolor(the_data, path, arrows=True)

                break

            # If we've seen this state before, discard
            if (row, col, dir_row, dir_col, steps) in seen:
                continue
            seen.add((row, col, dir_row, dir_col, steps))
            # print((row, col, dir_row, dir_col, steps))
            # if we have steps left, and aren't idle
            if steps < 3 and (dir_row, dir_col) != (0, 0):
                next_row, next_column = (row + dir_row, col + dir_col)
                if 0 <= next_row < len(the_data) and 0 <= next_column < len(the_data[0]):
                    new_heat_loss = heat_loss + the_data[next_row][next_column]
                    heapq.heappush(the_queue, (new_heat_loss, next_row, next_column, dir_row, dir_col, steps + 1,
                                               [*path, (next_row, next_column, dir_row, dir_col)]))

            for nr, nc, dr, dc in get_neighbors(row, col, the_data):
                if (nr, nc) not in [(row + dir_row, col + dir_col), (row - dir_row, col - dir_col)]:
                    new_heat_loss = heat_loss + the_data[nr][nc]
                    heapq.heappush(the_queue, (new_heat_loss
                                               , nr, nc, dr, dc, 1, [*path, (nr, nc, dr, dc)]))


# not 1244 or 1241
def part2():
    with open("input/day17.txt") as inputfile:
        # with open("input/day17.sample2.txt") as inputfile:
        the_data = [[int(x) for x in y] for y in [x.strip() for x in inputfile]]
        start = (0, 0)
        end = (len(the_data) - 1, len(the_data[0]) - 1)
        seen = set()
        pq = [(0, *start, 0, 0, 0, [(*start, 0, 0)])]

        while pq:
            heat_loss, row, col, dir_row, dir_col, steps, path = heapq.heappop(pq)

            if (row, col) == end and 3 < steps <= 10:
                print(heat_loss)
                # print(path)
                print(f"Sum of displayed path: {sum_path(the_data, [(state[1], state[0]) for state in path][1:])}")
                print_in_technicolor(the_data, path, arrows=True)

                break

            # If we've seen this state before, discard
            if (row, col, dir_row, dir_col, steps) in seen:
                continue
            seen.add((row, col, dir_row, dir_col, steps))
            # print((row, col, dir_row, dir_col, steps))
            # if we have steps left, and aren't idle
            if steps < 10 and (dir_row, dir_col) != (0, 0):
                next_row, next_column = (row + dir_row, col + dir_col)
                if 0 <= next_row < len(the_data) and 0 <= next_column < len(the_data[0]):
                    new_heat_loss = heat_loss + the_data[next_row][next_column]
                    heapq.heappush(pq, (new_heat_loss, next_row, next_column, dir_row, dir_col, steps + 1,
                                        [*path, (next_row, next_column, dir_row, dir_col)]))

            if steps > 3 or (dir_row, dir_col) == (0, 0):
                for nr, nc, dr, dc in get_neighbors(row, col, the_data):
                    if (nr, nc) not in [(row + dir_row, col + dir_col), (row - dir_row, col - dir_col)]:
                        new_heat_loss = heat_loss + the_data[nr][nc]
                        heapq.heappush(pq, (new_heat_loss
                                            , nr, nc, dr, dc, 1, [*path, (nr, nc, dr, dc)]))


if __name__ == '__main__':
    part2()

# at most, 3 blocks in a straight line before must turn
# can't reverse


#
#
# 1  function Dijkstra(Graph, source):
# 2      dist[source] ← 0                           // Initialization
# 3
# 4      create vertex priority queue Q
# 5
# 6      for each vertex v in Graph.Vertices:
# 7          if v ≠ source
# 8              dist[v] ← INFINITY                 // Unknown distance from source to v
# 9              prev[v] ← UNDEFINED                // Predecessor of v
# 10
# 11         Q.add_with_priority(v, dist[v])
# 12
# 13
# 14     while Q is not empty:                      // The main loop
# 15         u ← Q.extract_min()                    // Remove and return best vertex
# 16         for each neighbor v of u:              // Go through all v neighbors of u
# 17             alt ← dist[u] + Graph.Edges(u, v)
# 18             if alt < dist[v]:
# 19                 dist[v] ← alt
# 20                 prev[v] ← u
# 21                 Q.decrease_priority(v, alt)
# 22
# 23     return dist, prev

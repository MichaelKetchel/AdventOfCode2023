import heapq
from queue import PriorityQueue
from colorama import just_fix_windows_console, Fore, Back, Style
import numpy
import heapq
from queue import PriorityQueue, Queue


just_fix_windows_console()

def reconstruct_path(came_from, current):
    if came_from[current] is not None:
        res = reconstruct_path(came_from, came_from[current])
        res.append(current)
        return res
    else:
        return [current]

def get_last_n_steps(came_from, current, depth=3):
    if came_from[current] is not None and depth > 0:
        res = get_last_n_steps(came_from, came_from[current], depth=depth-1)
        res.append(current)
        return res
    else:
        return [current]

def check_history(matrix, came_from, current, depth=3, x=0,y=0):
    if came_from[current] is not None and x < depth and y < depth:
        if came_from[current][0] == current[0]:
            x += 1
        else:
            x = 0
        if came_from[current][1] == current[1]:
            y += 1
        else:
            y = 0
        return check_history(matrix, came_from, came_from[current], depth, x=x, y=y)
    else:
        return x < depth and y < depth
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
        print(matrix[y][x], end='')
        total += matrix[y][x]
    print()
    return total

def print_in_technicolor(data, path, node_of_interest=(-1,-1)):
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            if (row_index, col_index) == node_of_interest:
                print(Back.RED + Fore.BLACK + str(value) + Style.RESET_ALL + " ", end='')
                continue
            if (row_index, col_index) in path:
                print(Back.GREEN + Fore.BLACK + str(value) + Style.RESET_ALL + " ", end='')
                continue
            print(str(value) + " ", end='')
        print()
    print()


def part1():
    with open("input/day17.txt") as inputfile:
        the_data = [[int(x) for x in y] for y in [x.strip() for x in inputfile]]
        start = (0,0)
        end = (len(the_data)-1, len(the_data[0])-1)
        seen = set()
        pq = [(0,*start,0,0,0)]
        prev = {start: None}
        distances = {start: 0}

        while pq:
            heat_loss, row, col, dir_row, dir_col, steps = heapq.heappop(pq)

            if (row, col) == end:
                print(heat_loss)
                break

            # Discard invalid states
            if row < 0 or row >= len(the_data) or col < 0 or col >= len(the_data[0]):
                continue

            # If we've seen this state before, discard
            if (row, col, dir_row, dir_col, steps) in seen:
                continue
            seen.add((row, col, dir_row, dir_col, steps))
            # print((row, col, dir_row, dir_col, steps))
            # if we have steps left, and aren't idle
            if steps < 3 and (dir_row, dir_col) != (0,0):
                next_row, next_column = (row + dir_row, col + dir_col)
                if 0 <= next_row < len(the_data) and 0 <= next_column < len(the_data[0]):
                    new_heat_loss = heat_loss + the_data[next_row][next_column]
                    heapq.heappush(pq, (new_heat_loss, next_row, next_column, dir_row, dir_col, steps+1))
                    # if new_heat_loss < distances.get((next_row, next_column), float('infinity')):
                    #     distances[(next_row, next_column)] = new_heat_loss
                    #     prev[(next_row, next_column)] = (row, col)


            for nr, nc, dr, dc in get_neighbors(row, col, the_data):
                if (nr, nc) not in [(row+dir_row, col+dir_col), (row-dir_row, col-dir_col)]:
                    new_heat_loss = heat_loss + the_data[nr][nc]
                    heapq.heappush(pq, (new_heat_loss
                        , nr, nc, dr, dc, 1))
                    # if new_heat_loss < distances.get((nr, nc), float('infinity')):
                    #     distances[(nr, nc)] = new_heat_loss
                    #     prev[(nr, nc)] = (row, col)

        # print(f"{distances[end]}")
        # # path = [(x,y) for y,x in reconstruct_path(prev, end)]
        # path = reconstruct_path(prev, end)
        # print("The reconstruction just ain't quite right yet.")
        # # Gotta flip it for the render cuz we ain't rewriting that
        # print_in_technicolor(the_data, [(x,y) for y,x in path])
        # print(sum_path(the_data, path))

# not 1244 or 1241
def part2():
    with open("input/day17.sample.txt") as inputfile:
        for row in inputfile:
            pass


if __name__ == '__main__':
    part1()

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
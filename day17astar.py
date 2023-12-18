import heapq
from queue import PriorityQueue
from colorama import just_fix_windows_console, Fore, Back, Style

import heapq
from queue import PriorityQueue


def a_star(matrix, start, goal):
    queue = PriorityQueue()
    queue.put((0, start))  # (priority, node)
    came_from = {start: None}
    g_score = {}
    for y_pos in range(0, len(matrix)):
        for x_pos in range(0, len(matrix[0])):
            g_score[(x_pos, y_pos)] = float('inf')

    # g_score = {(x,y): float('inf') for y in matrix}
    g_score[start] = 0

    while not queue.empty():
        _, current = queue.get()  # Get the node with lowest score

        if current == goal:
            return reconstruct_path(came_from, goal)[1:]

        for neighbor in get_neighbors(*current, matrix):
            tentative_g_score = g_score[current] + matrix[neighbor[1]][neighbor[0]]
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                priority = tentative_g_score + heuristic(neighbor, goal)
                queue.put((priority, neighbor))
    return None  # No path found


def reconstruct_path(came_from, current):
    total_path = [current]
    while came_from[current]:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def get_neighbors(x, y, matrix):
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix):
            neighbors.append((nx, ny))
    return neighbors


def sum_path(matrix, path):
    total = 0
    for step in path:
        x, y = step
        total += matrix[y][x]
    return total

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


just_fix_windows_console()

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
    with open("input/day17.sample.txt") as inputfile:
        the_data = [[int(x) for x in y] for y in [x.strip() for x in inputfile]]

        path = a_star(the_data, (0, 0), (len(the_data[0]) - 1, len(the_data) - 1))
        print_in_technicolor(the_data, path)
        print("The shortest path is", path)
        print("Value of path is", sum_path(the_data, path))

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
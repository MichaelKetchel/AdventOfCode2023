import heapq
from queue import PriorityQueue
from colorama import just_fix_windows_console, Fore, Back, Style
import numpy
import heapq
from queue import PriorityQueue, Queue

def find_lowest_sum(start, end, matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    # Define directions for moving in a 2D grid (right, down, left, up)
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    queue = Queue()
    queue.put((start[0], start[1], []))  # put the starting point in the queue
    visited = set([(start[0], start[1])])  # keep track of visited nodes to avoid cycles

    min_sum = float('inf')
    min_path = None

    while not queue.empty():
        x, y, path = queue.get()

        if (x, y) == end:  # if we reached the end point, update the minimum sum and path if necessary
            current_sum = sum([matrix[i][j] for i, j in path]) + matrix[end[0]][end[1]]
            if current_sum < min_sum:
                min_sum = current_sum
                min_path = [(x, y)] + path
        else:  # otherwise add all reachable neighbors to the queue
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy

                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.put((nx, ny, path + [(x, y)]))

    return min_path[::-1]  # reverse the path to get it from start to end

def a_star(matrix, start, goal):
    potential_paths = []
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
            # potential_paths.append(reconstruct_path(came_from, goal)[1:])

        # # print_in_technicolor(matrix, reconstruct_path(came_from, current)[1:], current)
        # if not check_history(matrix, came_from, current, 3):
        #     # print("Failed history check\n")
        #     continue
        last_steps = get_last_n_steps(came_from, current, 2)
        for neighbor in get_neighbors(*current, matrix):
            if len(last_steps) >= 3 and (all(x[0] == neighbor[0] for x in last_steps) or all(x[1] == neighbor[1] for x in last_steps)):
                continue

            tentative_g_score = g_score[current] + matrix[neighbor[1]][neighbor[0]]
            print(f"g-score for {neighbor}: {tentative_g_score} vs {g_score.get(neighbor, float('inf'))}")
            print_in_technicolor(matrix, reconstruct_path(came_from, current)[1:], neighbor)
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                priority = tentative_g_score + heuristic(matrix, current, goal)
                # priority = tentative_g_score + heuristic(neighbor, goal)
                queue.put((priority, neighbor))

        # print()
    # return potential_paths  # No path found


def reconstruct_path_old(came_from, current):
    total_path = [current]
    while came_from[current]:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

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
#
# def heuristic(a, b):
#     (x1, y1) = a
#     (x2, y2) = b
#     return abs(x1 - x2) + abs(y1 - y2)

def dij_solve(matrix,x,y):
    n = len(matrix)
    m = len(matrix[0])

    # Initialize distances array with infinites and start position with zero
    distances = [[float('inf')] * m for _ in range(n)]
    distances[0][0] = 0

    heap = [(0, 0, 0)]  # (distance, row, col)
    while heap:
        dist, r, c = heapq.heappop(heap)

        if (r, c) == (n - 1, m - 1):
            return dist  # Reached the destination city block

        for n_r, n_c in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if 0 <= n_r < n and 0 <= n_c < m:  # If it's a valid city block
                cost = dist + int(matrix[n_r][n_c])
                if cost < distances[n_r][n_c]:  # Update the distance if new path is shorter
                    distances[n_r][n_c] = cost
                    heapq.heappush(heap, (cost, n_r, n_c))


def heuristic(matrix, a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def GetStraightParents(maxtrix, a, b):

    counter = 0
    isTurn = False



#
# def heuristic(matrix, a, b):
#     (x1, y1) = a
#     (x2, y2) = b
#     # return dij_solve(matrix, x2, y2)
#     # return sum_path(matrix, find_lowest_sum(a,b, matrix))
#     return 0

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
        # path = find_lowest_sum((0, 0), (len(the_data[0]) - 1, len(the_data) - 1), the_data)
        if not path:
            print("No path found!")
        else:
            print(path)

            print_in_technicolor(the_data, path)
            print("The shortest path is", path)
            print("Value of path is", sum_path(the_data, path))


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
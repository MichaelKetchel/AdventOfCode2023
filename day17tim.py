import heapq
from queue import PriorityQueue
from colorama import just_fix_windows_console, Fore, Back, Style
import numpy
import heapq
from queue import PriorityQueue, Queue


def get_neighbors(fileInput, coordinate):
    neighbor_list = []
    # looking up
    if coordinate[0] > 0:
        neighbor_list.append((coordinate[0]-1, coordinate[1],
                              (coordinate[2] * -coordinate[3]) + 1, -1, 0))
    # looking left
    if coordinate[1] > 0:
        neighbor_list.append((coordinate[0], coordinate[1]-1,
                              (coordinate[2] * -coordinate[4]) + 1, 0, -1))
    # looking down
    if coordinate[0] < len(fileInput) - 1:
        neighbor_list.append((coordinate[0]+1, coordinate[1],
                              (coordinate[2] * coordinate[3]) + 1, 1, 0))
    #looking right
    if coordinate[1] < len(fileInput) - 1:
        neighbor_list.append((coordinate[0], coordinate[1]+1,
                              (coordinate[2] * coordinate[4]) + 1, 0, 1))
    return neighbor_list
#
# def get_neighbors(matrix, x, y ):
#     neighbors = []
#     for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#         nx, ny = x + dx, y + dy
#         if 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix):
#             neighbors.append((nx, ny))
#     return neighbors


def set_weight_of_neighbor(fileInput, weightDict, source, target):
    if target not in weightDict.keys():
        weightDict[target] = fileInput[target[0]][target[1]] + weightDict[source]
    else:
        weightDict[target] = min(weightDict[target],
                                 fileInput[target[0]][target[1]] + weightDict[source])
    return

#
# def get_neighbors(matrix, x, y ):
#     neighbors = []
#     for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#         nx, ny = x + dx, y + dy
#         if 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix):
#             neighbors.append((nx, ny))
#     return neighbors

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


def reconstruct_path(came_from, current):
    # print(current, end='')
    if came_from[current] is not None:
        res = reconstruct_path(came_from, came_from[current])
        res.append(current)
        return res
    else:
        return [current]

def sum_path(matrix, path):
    total = 0
    for step in path:
        x, y = step
        total += matrix[y][x]
    return total
#

def part1():
    with open("input/day17.sample.txt") as inputfile:
        fileInput = [[int(x) for x in y] for y in [x.strip() for x in inputfile]]

        # (x, y, streak, x_origin, y_origin)
        startingCoordinate1 = (0, 0, 0, 0, 0)
        coordinatesToCheck = [startingCoordinate1]
        weightDict = {(0, 0, 0, 0, 0): 0}

        paths = {(0,0):None}

        while coordinatesToCheck:
            coordinatesToCheck.sort(key=lambda coordinate: weightDict[coordinate])

            coordinateToCheck = coordinatesToCheck[0]

            # Bingo
            if coordinateToCheck[0] == len(fileInput) - 1 and coordinateToCheck[1] == len(fileInput) - 1:
                break
            if (coordinateToCheck[0], coordinateToCheck[1]) != (0, 0):
                paths[(coordinateToCheck[0], coordinateToCheck[1])] = (coordinateToCheck[0] - coordinateToCheck[3], coordinateToCheck[1]-coordinateToCheck[4])
            current_path = reconstruct_path(paths, (coordinateToCheck[0], coordinateToCheck[1]))
            for neighbor in get_neighbors(fileInput, coordinateToCheck):

                # if we haven't checked the neighbor, and streak is less than 4
                if neighbor not in current_path and neighbor[2] != 4:
                    # magic
                    set_weight_of_neighbor(fileInput, weightDict, coordinateToCheck, neighbor)
                    coordinatesToCheck.append(neighbor)

            coordinatesToCheck.remove(coordinateToCheck)
        # print(weightDict)
        for items in weightDict.keys():
            if items[0] == len(fileInput) - 1 and items[1] == len(fileInput) - 1:
                print(items, weightDict[items])

        path = reconstruct_path(paths, (len(fileInput)-1, len(fileInput[0])-1))
        print(path)
        print(sum_path(fileInput, path))
        print_in_technicolor(fileInput, path)


        # print_in_technicolor(the_data, path)
        # print("The shortest path is", path)
        # print("Value of path is", sum_path(the_data, path))


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
import heapq

from queue import PriorityQueue

from colorama import just_fix_windows_console, Fore, Back, Style
just_fix_windows_console()

the_data = []
class Node(object):
    def __init__(self, value, x, y, direction=None, steps=0):
        self.value = value
        self.x = x
        self.y = y
        self.direction = direction
        self.steps = steps
        self.outgoing = {}  # outgoing edges (to other nodes)
        self.incoming = {}  # incoming edges (from other nodes)
        # self.visited = False

    def connect_to(self, node, cost=1):
        if isinstance(node, Node):
            if self != node:
                self.outgoing[node] = cost
                node.incoming[self] = cost

    def __str__(self):
        incoming_string = [f"{a.value}->s: {self.incoming[a]}" for a in self.incoming.keys()]
        outgoing_string = [f"s->{a.value}: {self.outgoing[a]}" for a in self.outgoing.keys()]
        return f"Node: {self.value}:\n\t\tIncoming: {incoming_string}\n\t\tOutgoing: {outgoing_string}, "
        # return f"Node: {self.value}| Incoming: {len(self.incoming)} Outgoing: {len(self.outgoing)}"
        # return f"Node: {self.value}| Incoming: {self.incoming.keys()} Outgoing: {(self.outgoing.keys())}"

class Graph(object):
    def __init__(self):
        self.nodes = {}  # key: value is name of the node : Node object

    def nodes_at(self, x, y):
        return list(filter(lambda node: node.x == x and node.y == y, self.nodes.values()))

    def node_at(self, x, y):
        return self.nodes_at(x,y)[0]

    def add_node(self, name, x, y, direction=None, steps=0):
        if not name in self.nodes:
            new_node = Node(name, x, y, direction, steps)
            self.nodes[name] = new_node

        return self.nodes[name]  # return the node (not yet connected to any other nodes)

    def add_edge(self, from_node, to_node, cost=1):
        if isinstance(from_node, Node) and isinstance(to_node, Node):
            from_node.connect_to(to_node, cost)  # connect nodes (and allow for bidirectional links)

    # def dijkstra(graph, source):
    #     distances = {
    #         source: 0
    #     }
    #

    def shortest_path(self, start, end):
        arbitrary_index = 0
        graph = self.nodes
        queue = [(0, arbitrary_index, start)]
        heapq.heapify(queue)
        distances = {node: float('infinity') for node in graph}
        distances[start.value] = 0
        paths = {start.value: []}

        while queue:
            (curr_distance, _, curr_vertex) = heapq.heappop(queue)

            print_in_technicolor(the_data, paths[curr_vertex.value], paths[curr_vertex.value])
            if curr_distance != distances[curr_vertex.value]:
                continue
            for neighbor, weight in graph[curr_vertex.value].outgoing.items():
                old_distance = distances[neighbor.value]
                new_distance = curr_distance + weight
                if new_distance < old_distance:
                    arbitrary_index += 1
                    heapq.heappush(queue, (new_distance, arbitrary_index, neighbor))
                    distances[neighbor.value] = new_distance
                    paths[neighbor.value] = paths[curr_vertex.value] + [neighbor.value]
        return distances[end.value], paths[end.value]


    def shortest_path_but_pain(self, start, end):
        global the_data
        arbitrary_index = 0
        graph = self.nodes
        queue = [(0, arbitrary_index, start)]
        heapq.heapify(queue)
        distances = {node: float('infinity') for node in graph}
        distances[start.value] = 0
        paths = {start.value: []}

        x_steps = 0
        y_steps = 0
        last_node = Node('fake', -1, -1)

        while queue:
            (curr_distance, _, current_node) = heapq.heappop(queue)
            if curr_distance != distances[current_node.value]:
                continue

            last_steps = [self.node_at(*point) for point in paths[current_node.value][-3:]]
            for neighbor, weight in graph[current_node.value].outgoing.items():
                if len(last_steps) >= 3 and (
                        all(x.x == neighbor.x for x in last_steps) or all(x.y == neighbor.y for x in last_steps)):
                    continue

                old_distance = distances[neighbor.value]
                # new_distance = curr_distance + (9-weight)
                new_distance = curr_distance + weight

                if new_distance < old_distance:
                    arbitrary_index += 1
                    heapq.heappush(queue, (new_distance, arbitrary_index, neighbor))
                    distances[neighbor.value] = new_distance
                    paths[neighbor.value] = paths[current_node.value] + [neighbor.value]
            last_node = current_node
        return distances[end.value], paths[end.value]




    def __str__(self):
        node_strings = '\n'.join([f"\t {str(node)}" for node in self.nodes.values()])
        return f"Graph:\n {node_strings}"



def print_in_technicolor(data, path, node_of_interest=(-1,-1)):

    clean_path = [a[:2] for a in path]
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            if (row_index, col_index) == node_of_interest[:2]:
                print(Back.RED + Fore.BLACK + str(value) + Style.RESET_ALL + " ", end='')
                continue
            if (row_index, col_index) in clean_path:
                print(Back.GREEN + Fore.BLACK + str(value) + Style.RESET_ALL + " ", end='')
                continue
            print(str(value) + " ", end='')
        print()
    print()


def print_in_arrows(data, path, node_of_interest=(-1,-1)):
    arrow_map = {
        None: 'X',
        'u':'^',
        'r':'>',
        'd':'v',
        'l':'<',
    }
    clean_path = [a[:2] for a in path]
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            if (row_index, col_index) == node_of_interest[:2]:
                print(Back.RED + Fore.BLACK + str(value) + Style.RESET_ALL + " ", end='')
                continue
            if (row_index, col_index) in clean_path:
                index = clean_path.index((row_index, col_index))
                path_entry = path[index]
                print(Back.GREEN + Fore.BLACK + arrow_map[path_entry[2]] + Style.RESET_ALL + " ", end='')
                continue
            print(str(value) + " ", end='')
        print()
    print()

def sum_path(matrix, path):
    total = 0
    for step in path:
        x, y = step[:2]
        total += matrix[y][x]
    return total
#
# def part1b():
#     # with open("input/day17.sample.txt") as inputfile:
#     with open("input/day17.txt") as inputfile:
#         the_graph = Graph()
#         the_data = [[int(x) for x in y] for y in [x.strip() for x in inputfile]]
#
#         print(solve(the_data))


def get_neighbors(x, y, matrix):
    neighbors = []
    for dx, dy, d in [(-1, 0, 'l'), (1, 0, 'r'), (0, -1, 'd'), (0, 1, 'u')]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix):
            neighbors.append((nx, ny, d))
    return neighbors

def generate_graph(the_graph, matrix, x=0, y=0, direction=None, steps = 0, parent_node=None, path=None, depth=10):
    path = [] if path is None else path
    neighbors = get_neighbors(x, y, matrix)
    print((x, y))

    if depth == 0 or (x, y) in path:
        return
    my_path = [*path, (x, y, direction, steps)]
    print_in_arrows(matrix, my_path,(x,y))
    this_node = the_graph.add_node((x, y, direction, steps), x, y, direction, steps)
    if parent_node is not None:
        this_node.connect_to(parent_node, matrix[parent_node.y][parent_node.x])
        parent_node.connect_to(this_node, matrix[y][x])

    if steps < 3:
        for x,y,d in neighbors:
            next_steps = steps + 1 if direction == d or direction is None else 0
            generate_graph(the_graph, matrix, x, y, d, next_steps, this_node, my_path, depth-1)





def part1():
    global the_data
    # with open("input/day17.txt") as inputfile:
    with open("input/day17.sample.txt") as inputfile:
        the_graph = Graph()
        the_data = [[int(x) for x in y] for y in [x.strip() for x in inputfile]]

        col_size = len(the_data)
        row_size = len(the_data[0])

        # # Build the graph

        generate_graph(the_graph, the_data)


        # for row_index, row in enumerate(the_data):
        #     for col_index, weight in enumerate(row):
        #         pass


        # for row_index, row in enumerate(the_data):
        #     for col_index, weight in enumerate(row):
        #         this_node = the_graph.add_node((col_index, row_index), col_index, row_index)
        #         my_weight = the_data[row_index][col_index]
        #
        #         # Left node
        #         if(col_index > 0):
        #             weight = the_data[row_index][col_index-1]
        #             left_node = the_graph.nodes[(col_index-1, row_index)]
        #             the_graph.add_edge(this_node, left_node, weight)
        #             the_graph.add_edge(left_node, this_node, my_weight)
        #
        #         # Up node
        #         if(row_index > 0):
        #             weight = the_data[row_index-1][col_index]
        #             up_node = the_graph.nodes[(col_index, row_index-1)]
        #             the_graph.add_edge(this_node, up_node, weight)
        #             the_graph.add_edge(up_node, this_node, my_weight)

        end_distance, end_path = the_graph.shortest_path(the_graph.node_at(0,0), the_graph.node_at(row_size-1, col_size-1))
        print(end_path)
        print_in_technicolor(the_data, end_path)
        print(f"End weight: {end_distance}")
        print(sum_path(the_data, end_path))
        # print()
        # print(the_graph)

                # print(col_index, weight)
            # the_graph.ad

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
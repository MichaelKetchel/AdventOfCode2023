import heapq



class Node(object):
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.outgoing = {}  # outgoing edges (to other nodes)
        self.incoming = {}  # incoming edges (from other nodes)

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

    def node_at(self, x, y):
        return self.nodes[(x, y)]

    def add_node(self, name, x, y):
        if not name in self.nodes:
            new_node = Node(name, x, y)
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


    def __str__(self):
        node_strings = '\n'.join([f"\t {str(node)}" for node in self.nodes.values()])
        return f"Graph:\n {node_strings}"





def part1():
    with open("input/day17.sample.txt") as inputfile:
        the_graph = Graph()
        the_data = [[int(x) for x in y] for y in [x.strip() for x in inputfile]]

        col_size = len(the_data)
        row_size = len(the_data[0])

        # Build the graph
        for row_index, row in enumerate(the_data):
            for col_index, weight in enumerate(row):
                this_node = the_graph.add_node((col_index, row_index), col_index, row_index)
                my_weight = the_data[row_index][col_index]

                # Left node
                if(col_index > 0):
                    weight = the_data[row_index][col_index-1]
                    left_node = the_graph.nodes[(col_index-1, row_index)]
                    the_graph.add_edge(this_node, left_node, weight)
                    the_graph.add_edge(left_node, this_node, my_weight)

                # Up node
                if(row_index > 0):
                    weight = the_data[row_index-1][col_index]
                    up_node = the_graph.nodes[(col_index, row_index-1)]
                    the_graph.add_edge(this_node, up_node, weight)
                    the_graph.add_edge(up_node, this_node, my_weight)

        print(the_graph.shortest_path(the_graph.node_at(0,0), the_graph.node_at(row_size-1, col_size-1)))
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
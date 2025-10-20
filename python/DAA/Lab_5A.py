import heapq

# ============================================
# DIJKSTRA'S ALGORITHM - Shortest Path
# ============================================
def dijkstra(graph, start_node):
    """
    Find shortest paths from start_node to all other nodes
    Time Complexity: O((V + E) log V) with min-heap
    """
    num_nodes = len(graph)
    distances = {node: float('inf') for node in range(num_nodes)}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    predecessors = {node: None for node in range(num_nodes)}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor in range(num_nodes):
            weight = graph[current_node][neighbor]
            if weight > 0 and weight != float('inf'):
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, predecessors

def print_dijkstra_path(predecessors, start, end):
    """Print the shortest path from start to end"""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    return " -> ".join(map(str, path))


# ============================================
# PRIM'S ALGORITHM - Minimum Spanning Tree
# ============================================
def prims(graph, start_node):
    """
    Find Minimum Spanning Tree using Prim's Algorithm
    Time Complexity: O(V^2) for adjacency matrix
    """
    num_nodes = len(graph)
    mst_set = [False] * num_nodes
    key = [float('inf')] * num_nodes
    parent = [None] * num_nodes
    
    key[start_node] = 0
    parent[start_node] = -1
    total_cost = 0
    mst_edges = []

    for _ in range(num_nodes):
        # Find minimum key vertex not in MST
        min_key = float('inf')
        u = -1
        for v in range(num_nodes):
            if not mst_set[v] and key[v] < min_key:
                min_key = key[v]
                u = v
        
        if u == -1:
            break
        
        mst_set[u] = True
        
        # Add edge to MST
        if parent[u] != -1:
            mst_edges.append((parent[u], u, graph[u][parent[u]]))
            total_cost += graph[u][parent[u]]

        # Update keys of adjacent vertices
        for v in range(num_nodes):
            weight = graph[u][v]
            if weight > 0 and not mst_set[v] and key[v] > weight:
                key[v] = weight
                parent[v] = u
                
    return mst_edges, total_cost


# ============================================
# KRUSKAL'S ALGORITHM - Minimum Spanning Tree
# ============================================
class UnionFind:
    """Union-Find (Disjoint Set) data structure for Kruskal's algorithm"""
    def __init__(self, n):
        self.parent = {i: i for i in range(n)}
        self.rank = {i: 0 for i in range(n)}
    
    def find(self, node):
        """Find with path compression"""
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]
    
    def union(self, n1, n2):
        """Union by rank"""
        r1, r2 = self.find(n1), self.find(n2)
        if r1 != r2:
            if self.rank[r1] > self.rank[r2]:
                self.parent[r2] = r1
            elif self.rank[r1] < self.rank[r2]:
                self.parent[r1] = r2
            else:
                self.parent[r1] = r2
                self.rank[r2] += 1
            return True
        return False

def kruskals(graph):
    """
    Find Minimum Spanning Tree using Kruskal's Algorithm
    Time Complexity: O(E log E) for sorting edges
    """
    num_nodes = len(graph)
    edges = []
    
    # Extract all edges from adjacency matrix
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if graph[i][j] != 0 and graph[i][j] != float('inf'):
                edges.append((graph[i][j], i, j))
    
    # Sort edges by weight
    edges.sort()
    
    # Initialize Union-Find
    uf = UnionFind(num_nodes)
    
    mst_edges = []
    total_cost = 0
    
    # Process edges in sorted order
    for weight, u, v in edges:
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_cost += weight
            if len(mst_edges) == num_nodes - 1:
                break
            
    return mst_edges, total_cost


# ============================================
# EXAMPLE GRAPHS
# ============================================

# Example 1: Simple 5-vertex graph (from PDF)
graph1 = [
    [0, 2, 0, 6, 0],
    [2, 0, 3, 8, 5],
    [0, 3, 0, 0, 7],
    [6, 8, 0, 0, 9],
    [0, 5, 7, 9, 0]
]

# Example 2: 6-vertex graph
graph2 = [
    [0, 4, 0, 0, 0, 0],
    [4, 0, 8, 0, 0, 0],
    [0, 8, 0, 7, 0, 4],
    [0, 0, 7, 0, 9, 14],
    [0, 0, 0, 9, 0, 10],
    [0, 0, 4, 14, 10, 0]
]

# Example 3: 7-vertex weighted graph
graph3 = [
    [0, 2, 0, 1, 0, 0, 0],
    [2, 0, 2, 2, 0, 0, 0],
    [0, 2, 0, 0, 3, 0, 0],
    [1, 2, 0, 0, 1, 0, 0],
    [0, 0, 3, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 1, 0]
]

# Example 4: Disconnected graph example
graph4 = [
    [0, 5, 3, 0, 0],
    [5, 0, 0, 4, 0],
    [3, 0, 0, 2, 6],
    [0, 4, 2, 0, 1],
    [0, 0, 6, 1, 0]
]


# ============================================
# MAIN EXECUTION
# ============================================
def print_separator(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def run_all_examples():
    """Run all algorithms on all example graphs"""
    
    graphs = [
        ("Graph 1 (5 vertices)", graph1),
        ("Graph 2 (6 vertices)", graph2),
        ("Graph 3 (7 vertices)", graph3),
        ("Graph 4 (5 vertices - Different Weights)", graph4)
    ]
    
    for graph_name, graph in graphs:
        print_separator(graph_name)
        
        # Print adjacency matrix
        print("\nAdjacency Matrix:")
        print("     ", end="")
        for i in range(len(graph)):
            print(f"{i:4}", end="")
        print()
        for i, row in enumerate(graph):
            print(f"{i:4}:", end="")
            for val in row:
                if val == float('inf'):
                    print("  ∞ ", end="")
                else:
                    print(f"{val:4}", end="")
            print()
        
        # DIJKSTRA'S ALGORITHM
        print_separator("DIJKSTRA'S ALGORITHM - Shortest Paths from Node 0")
        distances, predecessors = dijkstra(graph, 0)
        print("\nShortest distances from node 0:")
        for node, distance in sorted(distances.items()):
            if distance == float('inf'):
                print(f"  Node {node}: ∞ (unreachable)")
            else:
                path = print_dijkstra_path(predecessors, 0, node)
                print(f"  Node {node}: {distance:3} | Path: {path}")
        
        # PRIM'S ALGORITHM
        print_separator("PRIM'S ALGORITHM - Minimum Spanning Tree from Node 0")
        mst_edges_prim, total_cost_prim = prims(graph, 0)
        print("\nMinimum Spanning Tree (Prim's):")
        if mst_edges_prim:
            for u, v, weight in mst_edges_prim:
                print(f"  Edge: {u} -- {v} | Weight: {weight}")
            print(f"\n  Total MST Cost: {total_cost_prim}")
        else:
            print("  No MST found (graph might be disconnected)")
        
        # KRUSKAL'S ALGORITHM
        print_separator("KRUSKAL'S ALGORITHM - Minimum Spanning Tree")
        mst_edges_kruskal, total_cost_kruskal = kruskals(graph)
        print("\nMinimum Spanning Tree (Kruskal's):")
        if mst_edges_kruskal:
            for u, v, weight in mst_edges_kruskal:
                print(f"  Edge: {u} -- {v} | Weight: {weight}")
            print(f"\n  Total MST Cost: {total_cost_kruskal}")
        else:
            print("  No MST found (graph might be disconnected)")
        
        print("\n")

if __name__ == "__main__":
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + " " * 15 + "GRAPH ALGORITHMS DEMONSTRATION" + " " * 23 + "█")
    print("█" + " " * 10 + "Dijkstra's | Prim's | Kruskal's Algorithms" + " " * 16 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    run_all_examples()
    
    print("\n" + "=" * 70)
    print("  EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 70 + "\n")



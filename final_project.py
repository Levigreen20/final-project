import heapq

# Algorithm 1: Lowest Cost Delivery Between Two Locations (Dijkstra's Algorithm)
def algorithm_1(graph, start, end):
    # Step 1: Initialize distances
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    prev = {node: None for node in graph}
    pq = [(0, start)]  # (cost, node)
    
    # Step 2: Main Loop
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_node == end:
            break
        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                prev[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    # Step 3: Reconstruct Path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    
    return path, dist[end]

# Algorithm 2: Best Path from the Hub (Prim's Minimum Spanning Tree)
def algorithm_2(graph, start):
    mst = []
    total_cost = 0
    visited = set()
    min_heap = [(0, start, None)]  # (cost, node, previous_node)

    while min_heap:
        cost, node, prev_node = heapq.heappop(min_heap)
        if node not in visited:
            visited.add(node)
            if prev_node:
                mst.append((prev_node, node, cost))
                total_cost += cost
            for neighbor, weight in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(min_heap, (weight, neighbor, node))

    return mst, total_cost

# Algorithm 3: Dynamic Network Changes (Update MST)
def algorithm_3(graph, start, remove_edges, add_edges):
    # Step 1: Remove specified edges
    for edge in remove_edges:
        node1, node2 = edge.split('-')
        graph[node1] = [(n, w) for n, w in graph[node1] if n != node2]
        graph[node2] = [(n, w) for n, w in graph[node2] if n != node1]

    # Step 2: Add new edges
    for node1, node2, weight in add_edges:
        graph[node1].append((node2, weight))
        graph[node2].append((node1, weight))

    # Step 3: Recompute MST
    return algorithm_2(graph, start)


# --- Below is example usage ---

example_graph = {
    "A": [("B", 4), ("C", 2)],
    "B": [("A", 4), ("C", 1), ("D", 5)],
    "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
    "D": [("B", 5), ("C", 8), ("E", 2)],
    "E": [("C", 10), ("D", 2)]
}

# Testing Algorithm 1
print("\n--- Algorithm 1 Tests ---")
path, cost = algorithm_1(example_graph, "A", "E")
print("Shortest Path A -> E:", path)
print("Total Cost:", cost)

path, cost = algorithm_1(example_graph, "A", "B")
print("Shortest Path A -> B:", path)
print("Total Cost:", cost)

# Testing Algorithm 2
print("\n--- Algorithm 2 Tests ---")
mst, total_cost = algorithm_2(example_graph, "A")
print("Minimum Spanning Tree:", mst)
print("Total MST Cost:", total_cost)

# Testing Algorithm 3
print("\n--- Algorithm 3 Tests ---")
# Here we reset the graph because Algorithm 3 modifies it
example_graph_dynamic = {
    "A": [("B", 4), ("C", 2)],
    "B": [("A", 4), ("C", 1), ("D", 5)],
    "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
    "D": [("B", 5), ("C", 8), ("E", 2)],
    "E": [("C", 10), ("D", 2)]
}
mst, total_cost = algorithm_3(example_graph_dynamic, "A", ["C-E"], [("B", "E", 3)])
print("Updated MST after changes:", mst)
print("Updated Total Cost:", total_cost)

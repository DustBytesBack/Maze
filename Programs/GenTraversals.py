import pygame

# draw path
def draw_path(path,color, TILE, DELAY, LINEWIDTH, sc):
    for edges in path:
        x1, y1 = edges[0]
        x2, y2 = edges[1]
        pygame.draw.line(sc, pygame.Color(color),
                         (x1 * TILE + TILE // 2, y1 * TILE + TILE // 2),
                         (x2 * TILE + TILE // 2, y2 * TILE + TILE // 2), LINEWIDTH)
        
    pygame.display.flip()
    pygame.time.delay(DELAY)


# dfs traversal
def dfs_traversal(graph, start, goal, TILE, DELAY, LINEWIDTH, sc):
    stack = [start]
    visited = set()
    parent = {}
    path_set = []

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)

            if node in parent:
                path_set.append((parent[node], node))
                draw_path([(parent[node], node)], 'green', TILE, DELAY, LINEWIDTH, sc)

            if node == goal:
                path = []
                while node in parent:
                    prev = parent[node]
                    path.append((prev, node))
                    node = prev
                path.reverse()
                return path

            backtracked = False                                       # Flag to check if backtracking occurred
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:                           # If the neighbor is not visited , i.e backtracking occurs
                    stack.append(neighbor)
                    parent[neighbor] = node
                    backtracked = True
            
            if not backtracked and node in parent:                     # If backtracking occurs, draw the path in purple
                draw_path([(parent[node], node)], 'purple', TILE, DELAY, LINEWIDTH, sc)

    return []

# bsf traversal 
def bfs_traversal(graph,start,goal, TILE, DELAY, LINEWIDTH, sc):
    visited = set()
    queue = [start]
    parent = {}
    path_set = []

    while queue:
        node = queue.pop(0)

        if node not in visited:
            visited.add(node)

            if node in parent:
                # path_set.append((parent[node], node))
                draw_path([(parent[node], node)],'green', TILE, DELAY, LINEWIDTH, sc)

            if node == goal:
                current = goal
                while current != start:
                    path_set.append((parent[current], current))
                    current = parent[current]
                path_set.reverse()
                return visited,path_set
            
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    queue.append(neighbor)
                    parent[neighbor] = node

    return visited, path_set

# A*

def heuristic(a, b):    #manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(graph, start, goal, TILE, DELAY, LINEWIDTH, sc):
    open_set = {start}  # The set of nodes to be evaluated
    pq = [(0, start)]

    g_score = {node: float('inf') for node in graph.nodes}  # Cost from start along best known path.
    g_score[start] = 0

    f_score = {node: float('inf') for node in graph.nodes} # Estimated total cost from start to goal through y.
    f_score[start] = heuristic(start, goal)

    parent = {}
    path = []

    while pq:
        _, node = pq.pop(0)

        if node == goal:
            path = []
            while node in parent:
                prev = parent[node]
                path.append((prev, node))
                node = prev
            path.reverse()
            return path

        open_set.remove(node)   # Remove the node from the open set

        for neighbor in graph.neighbors(node):
            tentative_g_score = g_score[node] + 1   # Assuming the weight of each edge is 1

            if tentative_g_score < g_score[neighbor]:
                parent[neighbor] = node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)   # f(x) = g(x) + h(x)

                if neighbor not in open_set:
                    open_set.add(neighbor)
                    pq.append((f_score[neighbor], neighbor))
                    pq.sort()                                   # Sort the priority queue based on f_score
                    draw_path([(node, neighbor)], 'green', TILE, DELAY, LINEWIDTH, sc)

    return []

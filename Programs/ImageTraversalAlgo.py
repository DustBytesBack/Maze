from collections import deque
import heapq
import pygame
import time


# ------------------------ DFS Traversal ------------------------
def draw_path(screen, path, color, cell_size):
    """Draw the path on the screen."""
    for edge in path:
        (x1, y1), (x2, y2) = edge
        pygame.draw.line(
            screen, color,
            (x1 * cell_size + cell_size // 2, y1 * cell_size + cell_size // 2),
            (x2 * cell_size + cell_size // 2, y2 * cell_size + cell_size // 2),
            7
        )
    pygame.display.flip()
    time.sleep(0.02)

def dfs_traversal(graph, start, goal, screen, cell_size):
    """Perform DFS to find the path and visualize it."""
    stack = [start]
    visited = set()
    parent = {}
    path_set = []

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)

            # Draw the traversal path
            if node in parent:
                path_set.append((parent[node], node))
                draw_path(screen, [(parent[node], node)], 'green', cell_size)

            # Check if goal is reached
            if node == goal:
                path = []
                while node in parent:
                    prev = parent[node]
                    path.append((prev, node))
                    node = prev
                path.reverse()
                return path  # Return the final path

            backtracked = False  # Flag to check for backtracking
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
                    parent[neighbor] = node
                    backtracked = True

            if not backtracked and node in parent:  # Draw backtracking path
                draw_path(screen, [(parent[node], node)], 'purple', cell_size)

    return []

#------------------------ BFS Traversal ------------------------
def bfs_traversal(graph, start, goal, screen, cell_size):
    """Perform BFS to find the path and visualize it."""
    queue = deque([start])
    visited = set()
    parent = {}
    path_set = []

    while queue:
        node = queue.popleft()

        if node not in visited:
            visited.add(node)

            # Draw the traversal path
            if node in parent:
                path_set.append((parent[node], node))
                draw_path(screen, [(parent[node], node)], 'green', cell_size)

            # Check if goal is reached
            if node == goal:
                path = []
                while node in parent:
                    prev = parent[node]
                    path.append((prev, node))
                    node = prev
                path.reverse()
                return path  # Return the final path

            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    parent[neighbor] = node

    return []

#------------------------ A* Traversal ------------------------
def h(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def a_star_traversal(graph, start, goal, screen, cell_size):
    """Perform A* to find the path and visualize it."""
    open_list = []
    heapq.heappush(open_list, (0 + h(start, goal), 0, start))  # (f, g, node)
    g_costs = {start: 0}  # g cost for each node
    parent = {}
    closed_list = set()

    while open_list:
        _, g, current = heapq.heappop(open_list)

        if current in closed_list:
            continue

        # Draw the current node
        if current in parent:
            draw_path(screen, [(parent[current], current)], 'green', cell_size)

        closed_list.add(current)

        # If we reached the goal, backtrack to find the path
        if current == goal:
            path = []
            while current in parent:
                prev = parent[current]
                path.append((prev, current))
                current = prev
            path.reverse()
            return path  # Return the final path

        # Expand neighbors
        for neighbor in graph[current]:
            if neighbor in closed_list:
                continue

            tentative_g = g + 1  # All edges have cost 1 (equal distance)
            if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g
                f = tentative_g + h(neighbor, goal)
                heapq.heappush(open_list, (f, tentative_g, neighbor))
                parent[neighbor] = current

    return []
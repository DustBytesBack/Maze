import pygame
import random as rd
import networkx
import miscFunc as mf
import traversals as tr
import Cell as cl

cols, rows, sc, TILE, ALGORITHM, GENALGO = cl.return_maze_features()
DELAY, LINEWIDTH, TICK = mf.compute_delay_and_width_tick(TILE)

clock = pygame.time.Clock()
    
def remove_walls(node, next):
    dx = node.x - next.x
    if dx == 1:
        node.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        node.walls['right'] = False
        next.walls['left'] = False
    dy = node.y - next.y
    if dy == 1:
        node.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        node.walls['bottom'] = False
        next.walls['top'] = False

def create_graph(grid_cells):
    G = networkx.Graph()
    for cell in grid_cells:
        node_idx = (cell.x, cell.y)
        G.add_node(node_idx)

        neighbors = [
            ((cell.x, cell.y - 1), cell.walls['top']),
            ((cell.x + 1, cell.y), cell.walls['right']),
            ((cell.x, cell.y + 1), cell.walls['bottom']),
            ((cell.x - 1, cell.y), cell.walls['left'])
        ]

        for (nx, ny), wall in neighbors:
            if not wall:
                G.add_edge((cell.x, cell.y), (nx, ny))
    return G

def maze_generator_dfs(grid_cells):
    current_cell = grid_cells[0]
    stack = []
    
    while True:
        [cell.show() for cell in grid_cells]
        current_cell.visited = True
        current_cell.current_cell()

        next_cell = current_cell.check_neighbors()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        else:
            break
        
        yield

import pygame
import random as rd

def kruskal_maze(grid_cells):
    edges = []
    for cell in grid_cells:
        x, y = cell.x, cell.y
        neighbors = [
            ((x, y), (x, y - 1)),  # Top neighbor
            ((x, y), (x + 1, y)),  # Right neighbor
            ((x, y), (x, y + 1)),  # Bottom neighbor
            ((x, y), (x - 1, y)),  # Left neighbor
        ]

        for edge in neighbors:
            (x1, y1), (x2, y2) = edge
            if 0 <= x2 < cols and 0 <= y2 < rows:  # Ensure the neighbor is within bounds
                edges.append(edge)

    # Randomly shuffle edges
    rd.shuffle(edges)

    # Initialize disjoint sets
    parent = {}
    rank = {}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)

        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    # Initialize each cell as its own set
    for cell in grid_cells:
        node = (cell.x, cell.y)
        parent[node] = node
        rank[node] = 0

    # Create the maze using Kruskal's algorithm
    for (x1, y1), (x2, y2) in edges:
        if find((x1, y1)) != find((x2, y2)):
            union((x1, y1), (x2, y2))

            # Remove walls between the two cells
            current = grid_cells[x1 + y1 * cols]
            neighbor = grid_cells[x2 + y2 * cols]

            current.visited = True
            neighbor.visited = True

            remove_walls(current, neighbor)

            # Visualize: Highlight the current and neighbor cells
            sc.fill(pygame.Color('darkslategrey'))
            for cell in grid_cells:
                cell.show()
            current.highlight(pygame.Color('orange'))  # Highlight current cell

            pygame.display.flip()
            pygame.time.delay(DELAY)

            yield  # Pause and allow resumption
    
    sc.fill(pygame.Color('darkslategrey'))
    for cell in grid_cells:
        cell.show()  # Draw the final grid without highlights
    pygame.display.flip()

"""Make this whole thing a function,for eg. main()"""
def main():
    sc.fill(pygame.Color('darkslategrey'))
    grid_cells = cl.get_grid_cells()
    if GENALGO == 'DFS':
        maze_generator = maze_generator_dfs(grid_cells)
    elif GENALGO == 'Kruskal':
        maze_generator = kruskal_maze(grid_cells)
    graph_made = False
    path = []
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        try:
            next(maze_generator)
        except StopIteration:
            graph_made = True

        if pygame.key.get_pressed()[pygame.K_SPACE] and graph_made:
            G = create_graph(grid_cells)
            graph_made = True
            start = (0, 0)
            if ALGORITHM == 'DFS':
                path = tr.dfs_traversal(G, start, (cols - 1, rows - 1), TILE, DELAY, LINEWIDTH, sc)
            elif ALGORITHM == 'BFS':
                visited, path = tr.bfs_traversal(G, start, (cols - 1, rows - 1), TILE, DELAY, LINEWIDTH, sc)
            elif ALGORITHM == 'A*':
                path = tr.a_star(G, start, (cols - 1, rows - 1), TILE, DELAY, LINEWIDTH, sc)

        tr.draw_path(path, 'orange', TILE, DELAY, LINEWIDTH, sc)
        
        pygame.display.flip()
        clock.tick(TICK)

if __name__ == "__main__":
    main()
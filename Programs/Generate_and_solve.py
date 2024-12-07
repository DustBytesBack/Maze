import pygame
import random as rd
import networkx
import miscFunc as mf
import traversals as tr
import Cell as cl

cols, rows, sc, TILE, ALGORITHM = cl.return_maze_features()
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

def create_graph():
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

"""Make this whole thing a function,for eg. main()"""
sc.fill(pygame.Color('darkslategrey'))
grid_cells = cl.get_grid_cells()
maze_generator = maze_generator_dfs(grid_cells)
graph_made = False
# visited_edges = [] ??
path = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()    
    try:
        next(maze_generator)
    except StopIteration:
        pass

    if all(cell.visited for cell in grid_cells):
        G = create_graph()
        graph_made = True

    if pygame.key.get_pressed()[pygame.K_SPACE] and graph_made:
        start = (0, 0)
        if ALGORITHM == 'DFS':
            path = tr.dfs_traversal(G, start, (cols - 1, rows - 1), TILE, DELAY, LINEWIDTH, sc)
        elif ALGORITHM == 'BFS':
            visited,path = tr.bfs_traversal(G, start, (cols - 1, rows - 1), TILE, DELAY, LINEWIDTH, sc)
        elif ALGORITHM == 'A*':
            path = tr.a_star(G, start, (cols - 1, rows - 1), TILE, DELAY, LINEWIDTH, sc)

    tr.draw_path(path,'orange',  TILE, DELAY, LINEWIDTH, sc)
        
    pygame.display.flip()
    clock.tick(TICK)
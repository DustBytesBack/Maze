import pygame
import random as rd
import networkx
import miscFunc as mf
import traversals as tr

RES = WIDTH, HEIGHT = 800, 800
TILE,ALGORITHM = mf.get_tile_size_and_algorithm()
print(TILE,ALGORITHM)
DELAY, LINEWIDTH, TICK = mf.compute_delay_and_width_tick(TILE)
cols, rows = WIDTH // TILE, HEIGHT // TILE

sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}   
        self.visited = False


    def show(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('white'), (x, y), (x + TILE, y), 2)
        if self.walls['right']: 
            pygame.draw.line(sc, pygame.Color('white'), (x + TILE, y), (x + TILE, y + TILE), 2) 
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('white'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('white'), (x, y + TILE), (x, y), 2)
    
    def current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('orange'), (x, y, TILE, TILE))
    
    def check_cell(self, x, y):
        find_idx = lambda x, y: x + y * cols
        if x < 0 or y < 0 or x > cols - 1 or y > rows - 1:
            return False
        return grid_cells[find_idx(x, y)]
    
    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return rd.choice(neighbors) if neighbors else None
    
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

def draw_path(path,color):
    for edges in path:
        x1, y1 = edges[0]
        x2, y2 = edges[1]
        pygame.draw.line(sc, pygame.Color(color),
                         (x1 * TILE + TILE // 2, y1 * TILE + TILE // 2),
                         (x2 * TILE + TILE // 2, y2 * TILE + TILE // 2), LINEWIDTH)
        
    pygame.display.flip()
    pygame.time.delay(DELAY)

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


grid_cells = [Cell(x, y) for y in range(rows) for x in range(cols)]
sc.fill(pygame.Color('darkslategrey'))
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
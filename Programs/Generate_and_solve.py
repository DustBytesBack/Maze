import pygame
import random as rd
import networkx

RES = WIDTH, HEIGHT = 800, 800
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE
pygame.init()

sc = pygame.display.set_mode(RES, pygame.RESIZABLE)
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

def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
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

def dfs_traversal(graph,start,goal):
    visited = set()
    stack = [start]
    parent = {}
    path_set = set()

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)

            if node in parent:
                px, py = parent[node]
                x,y = node

                pygame.draw.line(sc, pygame.Color('orange'),
                                 (px * TILE + TILE // 2, py * TILE + TILE // 2),
                                 (x * TILE + TILE // 2, y * TILE + TILE // 2), 20)
                path_set.add((px, py))
                pygame.display.flip()
                pygame.time.delay(50)

            if node == goal:
                return visited

            has_unvisited = False
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    stack.append(neighbor)
                    parent[neighbor] = node
                    has_unvisited = True

            if not has_unvisited and node in parent:
                px, py = parent[node]
                x, y = node
                pygame.draw.line(sc, pygame.Color('purple'),
                                 (px * TILE + TILE // 2, py * TILE + TILE // 2),
                                 (x * TILE + TILE // 2, y * TILE + TILE // 2), 20)
                pygame.display.flip()
                pygame.time.delay(100)

    return visited

grid_cells = [Cell(x, y) for y in range(rows) for x in range(cols)]
current_cell = grid_cells[0]
stack = []

while True:
    graph_made = False
    sc.fill(pygame.Color('darkslategrey'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
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

    if all(cell.visited for cell in grid_cells):
        G = create_graph()
        graph_made = True

        for edge in G.edges:
            x1, y1 = edge[0]
            x2, y2 = edge[1]
            pygame.draw.line(sc, pygame.Color('blue'), (x1 * TILE + TILE // 2, y1 * TILE + TILE // 2), (x2 * TILE + TILE // 2, y2 * TILE + TILE // 2), 2)

    if pygame.key.get_pressed()[pygame.K_SPACE] and graph_made:
        start = (0, 0)
        visited = dfs_traversal(G, start, (cols - 1, rows - 1))

    pygame.display.flip()
    clock.tick(50)
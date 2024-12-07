import pygame
import random as rd
import networkx
import miscFunc as mf

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

def heuristic(a, b) ->int:    #manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(graph, start, goal) -> list:
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
                    draw_path([(node, neighbor)], 'green')

    return []

def dfs_traversal(graph, start, goal) -> list:
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
                draw_path([(parent[node], node)], 'green')

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
                draw_path([(parent[node], node)], 'purple')

    return []


def bfs_traversal(graph,start,goal) -> list:
    visited = set()
    queue = [start]
    parent = {}
    path_set = []

    while queue:
        node = queue.pop(0)

        if node not in visited:
            visited.add(node)

            if node in parent:
                path_set.append((parent[node], node))
                draw_path([(parent[node], node)],'green')

            if node == goal:
                return visited,path_set
            
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    queue.append(neighbor)
                    parent[neighbor] = node

    return visited, path_set


def main():
    grid_cells = [Cell(x, y) for y in range(rows) for x in range(cols)]
    current_cell = grid_cells[0]
    stack = []
    sc.fill(pygame.Color('darkslategrey'))
    graph_made = False
    visited_edges = []
    path = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # if not graph_made:    
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

                # for edge in G.edges:
                #     x1, y1 = edge[0]
                #     x2, y2 = edge[1]
                #     pygame.draw.line(sc, pygame.Color('blue'), (x1 * TILE + TILE // 2, y1 * TILE + TILE // 2), (x2 * TILE + TILE // 2, y2 * TILE + TILE // 2), 2)

        if pygame.key.get_pressed()[pygame.K_SPACE] and graph_made:
            start = (0, 0)
            if ALGORITHM == 'DFS':
                path = dfs_traversal(G, start, (cols - 1, rows - 1))
            elif ALGORITHM == 'BFS':
                visited,path = bfs_traversal(G, start, (cols - 1, rows - 1))
            elif ALGORITHM == 'A*':
                path = a_star(G, start, (cols - 1, rows - 1))

        draw_path(path,'orange')
            
        pygame.display.flip()
        clock.tick(TICK)

if __name__ == '__main__':
    main()
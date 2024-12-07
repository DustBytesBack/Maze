import miscFunc as mf
import pygame
import random as rd    

TILE, ALGO = mf.get_tile_size_and_algorithm()
RES = WIDTH, HEIGHT = 800, 800
cols, rows = WIDTH // TILE, HEIGHT // TILE
sc = pygame.display.set_mode(RES)

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
    
grid_cells = [Cell(x, y) for y in range(rows) for x in range(cols)]

def get_grid_cells():
    return grid_cells

def return_maze_features():
    return cols, rows, sc, TILE, ALGO
import pygame as pg
from Colors import *


class Spot:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = BLACK
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row,self.col

    def is_closed(self):
        return self.color == BLUE

    def is_open(self):  
        return self.color == TURQUOISE

    def is_barrier(self):   
        return self.color == WHITE

    def is_start(self):   
        return self.color == ORANGE

    def is_end(self):   
        return self.color == TURQUOISE

    def reset(self):   
        self.color = BLACK

    def make_closed(self):   
        self.color = BLUE

    def make_open(self):   
        self.color = TURQUOISE

    def make_barrier(self):   
        self.color = WHITE

    def make_start(self):   
        self.color = ORANGE

    def make_end(self):   
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self,win):
        pg.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def update_neighbours(self,grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier(): #down
            self.neighbours.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():    #up
            self.neighbours.append(grid[self.row-1][self.col])
        
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier():     #right
            self.neighbours.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():    #left
            self.neighbours.append(grid[self.row][self.col-1])

    def __lt__(self,other):
        return False

import pygame as pg
from queue import PriorityQueue

# WIDTH = 800
# WIN = pg.display.set_mode((WIDTH,WIDTH))
# pg.display.set_caption("Maze")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,128,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

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

def h(p1,p2):   #manhattan distance
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def algorithm(draw,grid,start,end): #A* algorithm
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(),end.get_pos())

    open_set_hash = {start} #to check if the spot is in the open set
    
    while not open_set.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            for row in grid:
                for spot in row:
                    if spot.is_closed() or spot.is_open():
                        spot.reset()
            return True
        for neighbor in current.neighbours:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()

    return False

def make_grid(rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)

    return grid

def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pg.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pg.draw.line(win,GREY,(j*gap,0),(j*gap,width))


def draw(win,grid,rows,width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win,rows,width)
    pg.display.update()

def get_clicked_pos(pos,rows,width):
    gap = width // rows
    y,x = pos

    row = y // gap
    col = x // gap

    return row,col

def main(win,width):
    ROWS = 25
    grid = make_grid(ROWS,width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win,grid,ROWS,width)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if started:
                continue

            if pg.mouse.get_pressed()[0]: #if the pressed button is left
                pos = pg.mouse.get_pos()
                if pos[0] > width or pos[1] > width:
                    continue
                row,col = get_clicked_pos(pos,ROWS,width)
                spot = grid[row][col] 
                if not start and spot!= end:
                    start = spot
                    start.make_start()
                elif not end and spot!= start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()


            elif pg.mouse.get_pressed()[2]: #if the pressed button is right
                pos = pg.mouse.get_pos()
                if pos[0] > width or pos[1] > width:
                    continue
                row,col = get_clicked_pos(pos,ROWS,width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            
            elif pg.mouse.get_pressed()[1]:
                grid = make_grid(ROWS, width)
                start = None
                end = None
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                    
                    algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)
    
    pg.quit()

def start():
    WIDTH = 800
    WIN = pg.display.set_mode((WIDTH,WIDTH))
    pg.display.set_caption("Maze")
    main(WIN,WIDTH)

start()
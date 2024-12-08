from collections import deque
import heapq
import pygame
from PIL import Image
import sys
import time
from Colors import *
from ImageTraversalAlgo import dfs_traversal,bfs_traversal,a_star_traversal

# ------------------------ Load Maze Image ------------------------
def load_image(image_path):
    """Load the BMP maze image and convert it to RGB."""
    try:
        return Image.open(image_path).convert('RGB')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        sys.exit(1)

def create_grid_and_graph(image):
    """Convert image to grid and create graph."""
    width, height = image.size
    grid = []
    graph = {}

    for y in range(height):
        row = []
        for x in range(width):
            pixel = image.getpixel((x, y))
            if pixel == (0, 0, 0):  # Black pixel (wall)
                row.append(1)  # Wall
            else:  # White pixel (path)
                row.append(0)  # Path
                graph[(x, y)] = []  # Initialize node in graph
        grid.append(row)

    return grid, graph, width, height

def build_graph(grid, graph, width, height):
    """Build graph by adding edges for adjacent path cells."""
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 0:  # Only consider path cells
                neighbors = [
                    (x, y - 1),  # Top
                    (x + 1, y),  # Right
                    (x, y + 1),  # Bottom
                    (x - 1, y),  # Left
                ]
                for nx, ny in neighbors:
                    if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 0:
                        graph[(x, y)].append((nx, ny))

def load_maze_image(image_path):
    """Load the BMP maze image, convert it into a grid, and create a graph."""
    image = load_image(image_path)
    grid, graph, width, height = create_grid_and_graph(image)
    build_graph(grid, graph, width, height)
    return grid, graph, width, height

# ------------------------ Display Maze ------------------------
def calculate_cell_size(grid, window_size):
    """Calculate the cell size to fit the grid into the window."""
    rows, cols = len(grid), len(grid[0])
    scale_factor_x = window_size / cols
    scale_factor_y = window_size / rows
    return min(scale_factor_x, scale_factor_y)

def draw_maze(screen, grid, cell_size):
    """Draw the maze grid on the screen."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    rows, cols = len(grid), len(grid[0])

    for y in range(rows):
        for x in range(cols):
            color = BLACK if grid[y][x] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

def highlight_nodes(screen, start_node, goal_node, cell_size):
    """Highlight the start and goal nodes."""

    if start_node:
        sx, sy = start_node
        pygame.draw.circle(screen, BLUE, (sx * cell_size + cell_size // 2, sy * cell_size + cell_size // 2), cell_size // 3)
    if goal_node:
        gx, gy = goal_node
        pygame.draw.circle(screen, RED, (gx * cell_size + cell_size // 2, gy * cell_size + cell_size // 2), cell_size // 3)

def draw_final_path(screen, final_path, cell_size):
    """Draw the final path on the screen."""

    for edge in final_path:
        (x1, y1), (x2, y2) = edge
        pygame.draw.line(
            screen, ORANGE,
            (x1 * cell_size + cell_size // 2, y1 * cell_size + cell_size // 2),
            (x2 * cell_size + cell_size // 2, y2 * cell_size + cell_size // 2),
            4
        )

def display_maze(grid, graph,ALGO, cell_size=10):
    """Display the maze grid, visualize graph, and allow selecting start and goal nodes."""
    pygame.init()

    window_size = 1000
    cell_size = calculate_cell_size(grid, window_size)
    screen_width = int(len(grid[0]) * cell_size)
    screen_height = int(len(grid) * cell_size)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze with DFS Traversal")

    start_node = None
    goal_node = None
    final_path = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left-click
                mouse_x, mouse_y = event.pos
                clicked_x = int(mouse_x // cell_size)
                clicked_y = int(mouse_y // cell_size)

                if (clicked_x, clicked_y) in graph:
                    if not start_node:
                        start_node = (clicked_x, clicked_y)
                        print("Start Node selected: ",start_node)
                    elif not goal_node:
                        goal_node = (clicked_x, clicked_y)
                        print("Goal Node selected: ",goal_node)
                        if ALGO == 'DFS':
                            final_path = dfs_traversal(graph, start_node, goal_node, screen, cell_size)
                        elif ALGO == 'BFS':
                            final_path = bfs_traversal(graph, start_node, goal_node, screen, cell_size)
                        elif ALGO == 'A*':
                            final_path = a_star_traversal(graph, start_node, goal_node, screen, cell_size)

        draw_maze(screen, grid, cell_size)
        highlight_nodes(screen, start_node, goal_node, cell_size)
        draw_final_path(screen, final_path, cell_size)

        pygame.display.flip()

    pygame.quit()

# ------------------------ Main ------------------------
def main(image_path,ALGO):
    # image_path = "assets/100.bmp"
    grid, graph, width, height = load_maze_image(image_path)
    display_maze(grid, graph, ALGO, cell_size=10)

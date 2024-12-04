import random as rd
import tkinter as tk
from tkinter import simpledialog

def compute_delay_and_width_tick(TILE):
    
    if TILE < 15:
        return 0  # No delay when TILE < 15
    else:
        m = 40 / (7*4)  # Slope
        c = -600 / (7*4)  # Y-intercept
        delay = m * TILE + c

    
    m = 3 / 7  # Slope
    c = -10 / 7  # Y-intercept
    line_width = m * TILE + c
    
    if TILE <= 20:
        tick =0
    else:
        tick = TILE * 0.5

    return int(delay), int(line_width),int(tick)

def transform_tile(n:int):
    if 10 <= n <= 100:
        return 110 - n
    else:
        return False

def get_tile_size_and_algorithm():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    tile_size = None
    algorithm = None

    def on_select_algo(algo):
        nonlocal algorithm
        algorithm = algo
        algo_window.destroy()

    while tile_size is None:
        tile_size_str = simpledialog.askstring("Input", "Enter TILE Size in a range of 10 to 100 :\n(as the value increases maze complexity increases)")
        if tile_size_str is not None and tile_size_str.isdigit() and int(tile_size_str) > 0 and transform_tile(int(tile_size_str)):
            tile_size = transform_tile(int(tile_size_str))
        else:
            tk.messagebox.showerror("Invalid input", "Please enter a positive integer.")

    algo_window = tk.Toplevel(root)
    algo_window.title("Select Algorithm")

    tk.Button(algo_window, text="DFS", command=lambda: on_select_algo("DFS")).pack()
    tk.Button(algo_window, text="BFS", command=lambda: on_select_algo("BFS")).pack()
    tk.Button(algo_window, text="A*", command=lambda: on_select_algo("A*")).pack()

    root.wait_window(algo_window)
    root.destroy()

    return tile_size, algorithm
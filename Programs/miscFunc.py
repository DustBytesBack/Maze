import random as rd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


def compute_delay_and_width_tick(TILE) -> tuple:
    
    if TILE < 15:
        delay = 0
    else:
        m = 40 / (7*4)
        c = -600 / (7*4)
        delay = m * TILE + c

    
    m = 3 / 7
    c = -10 / 7
    line_width = m * TILE + c
    
    if TILE <= 20:
        tick =0
    else:
        tick = TILE * 0.5

    return int(delay), int(line_width),int(tick)

def transform_tile(n:int) -> int:
    if 10 <= n <= 100:
        return 110 - n
    else:
        return False

def getMazeConfigurations() -> tuple:
    """
    Displays a UI for selecting tile size and traversal algorithm,
    styled to match the given reference image.
    Returns:
        tile_size (int): Selected maze tile size.
        algorithm (str): Selected traversal algorithm.
        file_path (str): Path to the selected maze image.
    """
    root = tk.Tk()
    def onClose():
        nonlocal tile_size, algorithm, genalgo, filepath,drawMaze
        tile_size, algorithm, genalgo, filepath,drawMaze = None, None, None, None,False

        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", onClose)

    root.title("Maze Pathfinder")
    root.geometry("500x600")
    root.resizable(False, False)
    style = ttk.Style() # Style object for customizing widgets
    style.theme_use("xpnative") 

    tile_size = 50
    algorithm = None
    genalgo = None
    drawMaze = False
    filepath = None

    # Function to update slider value display
    def update_slider_label(event):
        slider_label.config(text=str(int(tile_size_slider.get())))

    # Function to set algorithm and close UI
    def set_algorithm(algo):
        nonlocal algorithm
        algorithm = algo

    def setGenAlgo(algo):
        nonlocal genalgo
        genalgo = algo

    def setdrawMaze():
        nonlocal drawMaze
        drawMaze = True
        root.quit()

    # Function to handle submission
    def submit_selection():
        nonlocal tile_size
        tile_size = transform_tile(int(tile_size_slider.get()))
        if not algorithm:
            messagebox.showerror("Error", "Please select an algorithm to Solve the Maze.")
        elif not genalgo:
            messagebox.showerror("Error", "Please select an algorithm to Generate the Maze.")
        else:
            root.quit()

    def browse_file():
        nonlocal filepath
        filepath = filedialog.askopenfilename(
            title="Select a Maze File",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All Files", "*.*")]
        )
        if filepath:  # If user selected a file
            input_var.set(filepath)  # Display the file path in the input field
            toggle_maze_generator()
    
    def clear_file():
        nonlocal filepath
        filepath = None
        input_var.set("")
        toggle_maze_generator()

    def submit_selectionImgaeSolver():
        nonlocal tile_size
        tile_size = None
        if not input_var.get():
            messagebox.showerror("Error", "Please select an image of a Maze to Solve.")
        else:
            if not algorithm:
                messagebox.showerror("Error", "Please select an algorithm to solve the Maze.")
            else:
                root.quit()

    def toggle_maze_generator(event=None):
        input_value = input_var.get().strip()
        if input_value:
            generator_frame.pack_forget()
            draw_frame.pack_forget()
        else:
            generator_frame.pack(fill="x", padx=10, pady=10)
            draw_frame.pack(fill="x", padx=10, pady=10)

    # Image Maze Solver Section
    solver_frame = ttk.LabelFrame(root, text="Maze solver", padding=10)
    solver_frame.pack(fill="x", padx=10, pady=10)

    # Input File Selection
    ttk.Label(solver_frame, text="Input:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    input_var = tk.StringVar()
    input_entry = ttk.Entry(solver_frame, textvariable=input_var, width=30,state='readonly')
    input_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
    
    ttk.Button(solver_frame, text="Browse",command=browse_file).grid(row=0, column=3, padx=5, pady=5)
    ttk.Button(solver_frame, text="Clear",command=clear_file).grid(row=0, column=4, padx=5, pady=5)

    input_entry.bind("<KeyRelease>", toggle_maze_generator)

    # Solve Maze Button
    ttk.Button(solver_frame, text="Solve maze!", command=submit_selectionImgaeSolver).grid(row=3, column=0, columnspan=4, pady=10)

    # Traverse Method Selection
    traversal_frame = ttk.LabelFrame(root, text="Traverse method", padding=10)
    traversal_frame.pack(fill="x", padx=10, pady=10)

    ttk.Label(traversal_frame, text="Traverse method:").grid(row=0, column=0, sticky="w",padx=5, pady=5)

    algo_var = tk.StringVar(value=None)
    ttk.Radiobutton(traversal_frame, text="DFS", variable=algo_var, value="DFS", command=lambda: set_algorithm("DFS")).grid(row=1, column=0, sticky="w")
    ttk.Radiobutton(traversal_frame, text="BFS", variable=algo_var, value="BFS", command=lambda: set_algorithm("BFS")).grid(row=1, column=1, sticky="w",padx=100)
    # ttk.Radiobutton(traversal_frame, text="Dijkstra", variable=algo_var, value="Dijkstra", command=lambda: set_algorithm("Dijkstra")).grid(row=2, column=2, sticky="w")
    ttk.Radiobutton(traversal_frame, text="A*", variable=algo_var, value="A*", command=lambda: set_algorithm("A*")).grid(row=1, column=2, sticky="w")

    # Maze Generator Section
    generator_frame = ttk.LabelFrame(root, text="Maze generator", padding=10)
    generator_frame.pack(fill="x", padx=10, pady=10)

    ttk.Label(generator_frame, text="Generation Algorithm:").grid(row=0, column=0, sticky="w", padx=5, pady=5)

    # Genaration Algorithm Selection
    genalgo_var = tk.StringVar(value=None)
    ttk.Radiobutton(generator_frame, text="DFS", variable=genalgo_var, value="DFS", command=lambda: setGenAlgo("DFS")).grid(row=1, column=0, sticky="w")
    ttk.Radiobutton(generator_frame, text="Kruskal", variable=genalgo_var, value="Kruskal", command=lambda: setGenAlgo("Kruskal")).grid(row=1, column=1, sticky="w")
    ttk.Radiobutton(generator_frame, text="Prim", variable=genalgo_var, value="Prim", command=lambda: setGenAlgo("Prim")).grid(row=1, column=2, sticky="w")

    ttk.Label(generator_frame, text="Maze size:").grid(row=2, column=0, sticky="w", padx=5, pady=5)

    tile_size_slider = ttk.Scale(generator_frame, from_=10, to=100, orient="horizontal", length=300)
    tile_size_slider.set(tile_size)
    tile_size_slider.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    slider_label = ttk.Label(generator_frame, text=str(tile_size))
    slider_label.grid(row=3, column=2, padx=5, pady=5)
    tile_size_slider.bind("<Motion>", update_slider_label)
    style.map("TScale",
          background=[('active', 'black'), ('!active', 'grey')]  # Active state vs inactive state color change
          )

    ttk.Button(generator_frame, text="Generate maze!", command=submit_selection).grid(row=4, column=0, columnspan=3, pady=10)

    # Draw Maze Section
    draw_frame = ttk.LabelFrame(root, text="Draw maze", padding=10)
    draw_frame.pack(fill="x", padx=10, pady=10)

    ttk.Label(draw_frame, text="Want to Draw your own Maze ?").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    ttk.Button(draw_frame, text="Draw", command=setdrawMaze).grid(row=0, column=1, padx=5, pady=5)

    root.mainloop()
    try:
        root.destroy()
    except tk.TclError:
        pass

    return tile_size, algorithm, genalgo, filepath,drawMaze

if '__main__' == __name__:
    getMazeConfigurations()
from miscFunc import getMazeConfigurations
# from GenerateNsolve import main as generateNsolve
from Draw_and_solve import start as drawNsolve
from ImageMazeSolver import main as imageMazeSolver

def main():
    TILE:int = None
    ALGO:str = None
    GENALGO:str = None
    FILE:str = None
    DRAW:bool = False
    TILE, ALGO,GENALGO,FILE,DRAW = getMazeConfigurations()
    
    if FILE is not None:
        imageMazeSolver(FILE,ALGO)
    # elif GENALGO is not None and ALGO is not None and TILE is not None:
    #     generateNsolve(TILE, ALGO, GENALGO)
    elif DRAW:
        drawNsolve()

if __name__ == "__main__":
    main()
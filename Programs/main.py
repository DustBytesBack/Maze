from miscFunc import getMazeConfigurations
from GenerateNsolve import main as generateNsolve
from Draw_and_solve import start as drawNsolve
from ImageMazeSolver import main as imageMazeSolver

def main():
    while True:
        TILE:int = None
        ALGO:str = None
        GENALGO:str = None
        FILE:str = None
        DRAW:bool = False
        TILE, ALGO,GENALGO,FILE,DRAW = getMazeConfigurations()
        
        if DRAW:
            drawNsolve()
        elif GENALGO is not None and ALGO is not None and TILE is not None:
            generateNsolve(TILE, GENALGO, ALGO)
        elif FILE is not None:
            imageMazeSolver(FILE,ALGO)
        elif FILE is None and GENALGO is None and ALGO is None and TILE is None and not DRAW :
            break

if __name__ == "__main__":
    main()
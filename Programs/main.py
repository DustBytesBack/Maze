from miscFunc import getMazeConfigurations
from GenerateNsolve import main as generateNsolve
from Draw_and_solve import main as drawNsolve

def main():
    TILE:int = None
    ALGO:str = None
    GENALGO:str = None
    FILE:str = None
    DRAW:bool = False
    TILE, ALGO,GENALGO,FILE,DRAW = getMazeConfigurations()
    
    if FILE is not None:
        pass
    elif GENALGO is not None and ALGO is not None and TILE is not None:
        generateNsolve(TILE, ALGO, GENALGO)
    elif ALGO is not None and DRAW:
        drawNsolve(ALGO)

if __name__ == "__main__":
    main()
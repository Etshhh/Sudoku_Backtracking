import numpy as np

    # grid = [
    #     [7,8,0,4,0,0,1,2,0],
    #     [6,0,0,0,7,5,0,0,9],
    #     [0,0,0,6,0,1,0,7,8],
    #     [0,0,7,0,4,0,2,6,0],
    #     [0,0,1,0,5,0,9,3,0],
    #     [9,0,4,0,6,0,0,0,5],
    #     [0,7,0,3,0,0,0,1,2],
    #     [1,2,0,0,0,7,4,0,0],
    #     [0,4,9,2,0,6,0,0,7]
    # ]

def printer(grid):
    """ A pretty printer for the grid.
    
    Parameters:
        grid (2D numpy): the sudoku grid """

    print()
    for i in range(9):
        if ((i % 3) == 0 ) and (i != 0):
            print('-'*21)

        for j in range(9):
            if ((j % 3) == 0) and (j != 0):
                print('| ', end='')

            print(str(grid[i][j]) +' ', end='')

            if (j == 8):
                print()
    print()


def empty_cells(grid):
    """ Find all empty cells and returns their indices.
    
    Parameters:
        grid (2D numpy): the sudoku grid 
    Returns:
        coords (list): list of tuples, each tuple is the x,y index """

    coords = np.argwhere(grid == 0)
    coords = zip(coords[:,0], coords[:,1])
    return list(coords)


def validator(grid, coord, val):
    """ Validates that an added value is valid relative to the current grid.
    
    Parameters:
        grid (2D numpy): the sudoku grid
        coord (tuple): the cell to be added coordinate
        val(int): value to be validated
    Returns:
        (boolean): True if it is valid """

    row, col = tuple(coord)
    if val in grid[row]:
        return False
    if val in grid[:, col]:
        return False

    r = 3 * (row // 3)
    c = 3 * (col // 3)
    box = grid[r:r+3, c:c+3]
    if val in box:
        return False
        
    return True


def solver(grid):
    """ Solves the grid using the backtracking algorithm.
    
    Parameters:
        grid (2D numpy): the sudoku grid
    Returns:
        No returns as it edits the passed one by reference """

    coords = empty_cells(grid)
    
    def adder(grid, coords):
        
        if not len(coords):
            return True

        coord = coords.pop(0)
        for val in range(1, 10):
            if validator(grid, coord, val):
                grid[tuple(coord)] = val

                if adder(grid, coords.copy()):
                    return True
                
                grid[tuple(coord)] = 0

        return False

    adder(grid, coords)



if __name__ == "__main__":

    grid = [
        [0,7,0,0,2,0,0,4,6],
        [0,6,0,0,0,0,8,9,0],
        [2,0,0,8,0,0,7,1,5],
        [0,8,4,0,9,7,0,0,0],
        [7,1,0,0,0,0,0,5,9],
        [0,0,0,1,3,0,4,8,0],
        [6,9,7,0,0,2,0,0,8],
        [0,5,8,0,0,0,0,6,0],
        [4,3,0,0,8,0,0,7,0]
    ]

    
    grid = np.array(grid)

    printer(grid)
    solver(grid)
    printer(grid)
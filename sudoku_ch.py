import numpy as np
import random as rd

def printer(grid):
    print()
    for i in range(9):
        if ((i % 3) == 0 )and (i != 0):
            print('-'*21)

        for j in range(9):
            if ((j % 3) == 0) and (j != 0):
                print('| ', end='')

            print(str(grid[i][j]) +' ', end='')

            if (j == 8):
                print()
    print()


def empty_cells(grid, rdm):
    coords = np.argwhere(grid == 0)
    coords = list(zip(coords[:,0], coords[:,1]))
    if rdm:
        rd.shuffle(coords)

    return coords


def full_cells(grid, rdm):
    coords = np.argwhere(grid != 0)
    coords = list(zip(coords[:,0], coords[:,1]))
    if rdm:
        rd.shuffle(coords)

    return coords


def validator(grid, coord, val):
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


def solver(grid, rdm):
    coords = empty_cells(grid, False)
    
    def adder(grid, coords):
        
        if not len(coords):
            return True

        coord = coords.pop(0)
        numbers = [i for i in range(1, 10)]
        if rdm:
            rd.shuffle(numbers)

        for val in numbers:
            if validator(grid, coord, val):
                grid[tuple(coord)] = val

                if adder(grid, coords.copy()):
                    return True
                
                grid[tuple(coord)] = 0

        return False

    adder(grid, coords)


def challenger_old(grid):
    attempts = 13

    while attempts > 0:
        row = rd.randint(0,8)
        col = rd.randint(0,8)
        
        if grid[row, col] != 0:
            grid[row, col] = 0
            attempts-=1


def challenger(grid, attempts):
    print(f'attempts: {attempts}')
    true_grid = np.copy(grid)
    coords = full_cells(grid, True)

    while attempts > 0:
        # print('_'*50)
        coord = coords.pop(0)
        bk_grid = np.copy(grid)
        bk_grid[tuple(coord)] = 0
        solver(bk_grid, rdm=True)
        if (true_grid == bk_grid).all():
            grid[tuple(coord)] = 0
            attempts -= 1
        # else: print('not the same solution')
        # printer(grid)
        

def createagrid(diff):
    # attempts = 10*(diff+1)
    options = [30, 36, 44]
    attempts = options[diff]
    grid = [[0 for _ in range(9)] for _ in range(9)]
    grid = np.array(grid)
    solver(grid, rdm=True)
    challenger(grid, attempts)
    # printer(grid)
    return grid



if __name__ == "__main__":
    grid = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ]
    mgrid = [[0 for _ in range(9)] for _ in range(9)]
    grid = np.array(grid)
    mgrid = np.array(mgrid)

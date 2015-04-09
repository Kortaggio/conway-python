#!/usr/bin/python
"""
Conway's Game of life implementation in Python.
Grid is a torus, i.e. cells on the edges wrap around to the other side.
"""
from __future__ import print_function
import os.path

def main():
    input_file = open('input.txt', 'r')
    outfile_num = 0
    outfile_name = 'output_' + str(outfile_num)
    while os.path.isfile(outfile_name + '.txt'):
        outfile_num += 1
        outfile_name = 'output_' + str(outfile_num)

    output_file = open('output_'+ str(outfile_num) +'.txt', 'a')

    iterations = 0
    height = 0
    width = 0
    grid = {}

    # Process input from file
    for i, line in enumerate(input_file):
        if i == 0:
            iterations = int(line.strip())
        elif i == 1:
            line = line.split()
            width = int(line[0])
            height = int(line[-1])
        else:
            row = i - 2
            line = map(int, line.split())
            for col, value in enumerate(line):
                grid[(row, col)] = value

    # Run the simulation
    grid = conway(iterations, width, height, grid)
    print('See', outfile_name + '.txt for the output.')

    # Print output to file
    # Convert to a nested array first
    output = []
    for row in range(height):
        # Build nested array
        out_row = []
        for col in range(width):
            out_row.append(None)
        output.append(out_row)

    for cell in grid:
        # Populate nested array
        row = cell[0]
        col = cell[1]
        value = grid[(row, col)]
        output[row][col] = value

    for row in output:
        # Write to file
        row = map(str, row)
        output_file.write(' '.join(row) + '\n')

    input_file.close()
    output_file.close()


def build_empty_grid(width, height):
    """
    Initializes an empty grid with the appropriate dictionary keys
    """
    grid = {}
    for row in range(width):
        for col in range(height):
            grid[(row, col)] = 0

    return grid


def conway(iterations, width, height, grid):
    """
    Implementation of Conway's game of life based on a dictionary as a grid.
    Returns the result grid after running for
    the specified number of iterations.
    """
    for generation in range(iterations):
        # Build a new grid for the next generation
        new_grid = grid
        print('Generation', str(generation))

        for cell in grid:
            # Get all the neighbors
            vals_of_neighbors = []
            for neighbor in neighbors(cell, width, height):
                vals_of_neighbors.append(grid[neighbor])

            # Live square dies if it has > 3 or < 2 live neighbors
            if grid[cell] == 1 and \
                (vals_of_neighbors.count(1) > 3 or \
                vals_of_neighbors.count(1) < 2):
                new_grid[cell] = 0

            # Empty square comes to life if it has three live neighbors
            elif grid[cell] == 0 and vals_of_neighbors.count(1) == 3:
                new_grid[cell] = 1

            elif grid[cell] != 1 and grid[cell] != 0:
                raise Exception('Grid can only contain 0 or 1')

    print('Completed simulation after', str(iterations), 'generations.')
    return new_grid

def neighbors(cell, width, height):
    """
    Returns an array of tuples with all neighbors of the given cell
    """
    x = cell[0] # == 3
    y = cell[1] # == 3

    return [
        (x-1 if x-1 >= 0 else width-1, y-1 if y-1 >= 0 else height-1),
        (x-1 if x-1 >= 0 else width-1, y),
        (x-1 if x-1 >= 0 else width-1, y+1 if y+1 < height-1 else 0),
        (x+1 if x+1 < width-1 else 0, y-1 if y-1 >= 0 else height-1),
        (x+1 if x+1 < width-1 else 0, y),
        (x+1 if x+1 < width-1 else 0, y+1 if y+1 < height-1 else 0),
        (x, y-1 if y-1 >= 0 else height-1),
        (x, y+1 if y+1 < height-1 else 0),
    ]



def test():
    """Unit testing"""
    assert build_empty_grid(1,1) == {(0, 0): 0}
    assert build_empty_grid(2,2) == {(0, 0): 0, (0, 1):0, (1, 0): 0, (1, 1): 0}
    for cell in neighbors((3, 3), 4, 4):
        assert cell in [
            (0,0),
            (0,2),
            (0,3),
            (2,0),
            (2,2),
            (2,3),
            (3,0),
            (3,2),
        ]

    for cell in neighbors((0, 0), 5, 5):
        assert cell in [
            (0,1),
            (1,0),
            (1,1),
            (4,4),
            (0,4),
            (4,0),
            (1,4),
            (4,1),
        ]
    assert conway(5, 3, 3, {(0, 1): 0, (1, 2): 0, (0, 0): 0, (2, 1): 0, (1, 1): 1, (2, 0): 0, (2, 2): 0, (1, 0): 0, (0, 2): 0}
        ) == {(0, 1): 0, (1, 2): 0, (0, 0): 0, (2, 1): 0, (1, 1): 0, (2, 0): 0, (2, 2): 0, (1, 0): 0, (0, 2): 0}
    assert conway(4, 5, 5, {(1, 3): 0, (3, 0): 0, (2, 1): 0, (0, 3): 0, (4, 0): 0, (1, 2): 0, (3, 3): 0, (4, 4): 0, (2, 2): 0, (4, 1): 0, (1, 1): 1, (3, 2): 0, (0, 0): 1, (0, 4): 0, (1, 4): 0, (2, 3): 0, (4, 2): 0, (1, 0): 1, (0, 1): 1, (3, 1): 0, (2, 4): 0, (2, 0): 0, (4, 3): 0, (3, 4): 0, (0, 2): 0}
        ) == {(1, 3): 0, (3, 0): 0, (2, 1): 0, (0, 3): 0, (4, 0): 0, (1, 2): 0, (3, 3): 0, (4, 4): 0, (2, 2): 0, (4, 1): 0, (1, 1): 1, (3, 2): 0, (0, 0): 1, (0, 4): 0, (1, 4): 0, (2, 3): 0, (4, 2): 0, (1, 0): 1, (0, 1): 1, (3, 1): 0, (2, 4): 0, (2, 0): 0, (4, 3): 0, (3, 4): 0, (0, 2): 0}
    print("All tests pass")


if __name__ == '__main__':
    test()
    main()
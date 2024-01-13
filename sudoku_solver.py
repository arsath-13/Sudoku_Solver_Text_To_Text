import sys
import math
import time
from typing import List, Tuple

def is_safe(grid: List[List[int]], row: int, col: int, num: int, size: int) -> bool:
    for x in range(size):
        if grid[row][x] == num or grid[x][col] == num:
            return False

    sqrt_size = int(math.sqrt(size))
    start_row, start_col = row - row % sqrt_size, col - col % sqrt_size
    for i in range(sqrt_size):
        for j in range(sqrt_size):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True

def count_possibilities(grid: List[List[int]], row: int, col: int, size: int) -> int:
    used = [False] * (size + 1)

    for i in range(size):
        if grid[row][i] != 0:
            used[grid[row][i]] = True

    for i in range(size):
        if grid[i][col] != 0:
            used[grid[i][col]] = True

    sqrt_size = int(math.sqrt(size))
    start_row, start_col = row - row % sqrt_size, col - col % sqrt_size
    for i in range(sqrt_size):
        for j in range(sqrt_size):
            if grid[i + start_row][j + start_col] != 0:
                used[grid[i + start_row][j + start_col]] = True

    count = 0
    for i in range(1, size + 1):
        if not used[i]:
            count += 1

    return count

def find_empty_cell_with_fewest_possibilities(grid: List[List[int]], size: int) -> Tuple[int, int]:
    min_possibilities = size + 1
    cell_with_min_possibilities = (-1, -1)

    for i in range(size):
        for j in range(size):
            if grid[i][j] == 0:
                possibilities = count_possibilities(grid, i, j, size)
                if possibilities < min_possibilities:
                    min_possibilities = possibilities
                    cell_with_min_possibilities = (i, j)

    return cell_with_min_possibilities

def solve_sudoku(grid: List[List[int]], size: int) -> bool:
    row, col = find_empty_cell_with_fewest_possibilities(grid, size)

    if row == -1 and col == -1:
        return True

    for num in range(1, size + 1):
        if is_safe(grid, row, col, num, size):
            grid[row][col] = num
            if solve_sudoku(grid, size):
                return True
            grid[row][col] = 0

    return False



def main():
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "<filename>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as inFile:
            grid = [list(map(int, line.split())) for line in inFile]

    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)

    size = len(grid)

    print(grid)

    start_time = time.time()

    if solve_sudoku(grid, size):
        end_time = time.time()
        duration = (end_time - start_time)*1000

        print(f"Sudoku solved in {duration:.1f} milliseconds.")

        with open(sys.argv[1] + "_output.txt", 'w') as outFile:
            for row in grid:
                outFile.write(" ".join(map(str, row)) + "\n")

    else:
        with open(sys.argv[1] + "_output.txt", 'w') as outFile:
            outFile.write("No Solution")


if __name__ == "__main__":
    main()
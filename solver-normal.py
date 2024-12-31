import time
import concurrent.futures

# Standard 9x9 Sudoku Board
def setBoard():
    board = [[2,3,0,9,4,0,0,5,0],
            [8,0,0,5,3,2,1,0,9],
            [9,5,0,1,0,0,7,0,3],
            [0,8,7,0,0,0,6,3,0],
            [4,0,3,0,7,1,0,8,0],
            [0,0,2,0,5,3,0,0,0],
            [3,6,8,0,0,0,0,0,0],
            [0,0,0,4,1,9,0,0,0],
            [0,0,9,0,0,8,0,7,2]]

    return board

# Position of a 0 on sudoku board
def findEmpty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None


# Checks whether a specific number can be used for specific diminesions
def isValid(board, num, pos):
    row, col = pos
    for i in range(9):
        if board[i][col] == num:
            return False
    for j in range(9):
        if board[row][j] == num:
            return False
    rowBlockStart = 3 * (row // 3)
    colBlockStart = 3 * (col // 3)
    for i in range(rowBlockStart, rowBlockStart + 3):
        for j in range(colBlockStart, colBlockStart + 3):
            if board[i][j] == num:
                return False
    return True

# Prints the puzzle
def puzzle(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            print(grid[i][j], end=" ")
        print()

# Backtracking algorithm
def solve(board):
    blank = findEmpty(board)
    if not blank:
        return True
    else:
        row, col = blank

    for i in range(1, 10):
        if isValid(board, i, blank):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False

def solve_with_threads(board, num_threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future = executor.submit(solve, board)
        return future.result()

if __name__ == '__main__':
    board = setBoard()
    num_threads = 5  # Change this to the desired number of threads
    start_time = time.time()
    if solve_with_threads(board, num_threads):
        puzzle(board)
        end_time = time.time()
        print(f"Time taken to solve: {end_time - start_time:.6f} seconds")
    else:
        print("Solution does not exist!")
        end_time = time.time()

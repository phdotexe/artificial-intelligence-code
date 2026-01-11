dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]

def isSafe(x, y, n, board):
    return x >= 0 and y >= 0 and x < n and y < n and board[x][y] == -1

def knightTourUtil(x, y, step, n, board):
    # If all squares are visited
    if step == n * n:
        return True

    # Try all 8 possible knight moves
    for i in range(8):
        nx = x + dx[i]
        ny = y + dy[i]

        if isSafe(nx, ny, n, board):
            board[nx][ny] = step

            if knightTourUtil(nx, ny, step + 1, n, board):
                return True

            # Backtrack
            board[nx][ny] = -1

    return False

def knightTour(n):
    board = [[-1 for _ in range(n)] for _ in range(n)]

    # Start from top-left corner
    board[0][0] = 0

    if knightTourUtil(0, 0, 1, n, board):
        return board

    return [[-1]]

if __name__=="__main__":
    n = 5
    res = knightTour(n)

    for row in res:
        for val in row:
            print(val, end=" ")
        print()
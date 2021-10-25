import random
import sys

##############################################
#                PARAMS                      #
##############################################
q = []
direction_row = [-1, 1, 0, 0]
direction_col = [0, 0, 1, -1]
move_counter = 0
N = -1
k = -1


##############################################
#          functions for the matrix          #
##############################################
def create_matrix(nrows, ncols, default_value):
    matrix = []
    for i in range(0, nrows):
        column = []
        for j in range(0, ncols):
            column.append(default_value)
        matrix.append(column)
    return matrix


def create_matrix_from_file(file):
    matrix = []
    with open(file) as f:
        lines = f.readlines()
    for i in range(0, len(lines)):
        line = lines[i].rstrip('\n').split(' ')
        line = [int(j) for j in line]
        matrix.append(line)
    return matrix


def print_matrix(matrix):
    for i in range(0, len(matrix)):
        print(matrix[i])


def pr_print_matrix(matrix, path):
    for elem in path:
        matrix[elem[0]][elem[1]] = "*"
    print_matrix(matrix)


def randomize_matrix(matrix, diff_value, n):
    n_rows = len(matrix)
    if n_rows > 0:
        n_cols = len(matrix[0])
    else:
        return
    while n != 0:
        r = random.randint(0, n_rows - 1)
        c = random.randint(0, n_cols - 1)
        if matrix[r][c] != diff_value:
            matrix[r][c] = diff_value
            n = n - 1


##############################################
#               helping functions            #
##############################################
def explore_neighbours(r, c):
    for i in range(0, 4):
        rr = r + direction_row[i]
        cc = c + direction_col[i]
        if rr < 0 or cc < 0 or rr >= N or cc >= N:
            continue
        if matrix[rr][cc] == 0 or visited[rr][cc] == 1:
            continue
        q.append([rr, cc])
        visited[rr][cc] = 1
        prev[rr][cc] = [r, c]


def deconstruct(starting_row, starting_col, ending_row, ending_col):
    path = []
    if ending_row == starting_row and ending_col == starting_col:
        return path
    previous = [-1, -1]
    path.append([ending_row, ending_col])
    while previous[0] != starting_row or previous[1] != starting_col:
        previous = prev[ending_row][ending_col]
        path.append(previous)
        ending_row, ending_col = previous
    path.reverse()
    return path


##############################################
#            modified bfs                    #
##############################################
def solve(starting_row, starting_col, ending_row, ending_col):
    global move_counter
    matrix[ending_row][ending_col] = "*"
    q.append([starting_row, starting_col])
    visited[starting_row][starting_col] = 1
    flag = 0
    while len(q) > 0 and flag != 1:
        r, c = q[0]
        del q[0]
        if matrix[r][c] == "*":
            flag = 1
            return move_counter
        explore_neighbours(r, c)
        move_counter = move_counter + 1
    return -1


if __name__ == '__main__':
    if len(sys.argv) < 7:
        sys.exit("Too few arguments!")
    if len(sys.argv) > 8:
        sys.exit("Too many arguments!")
    N = int(sys.argv[1])
    k = int(sys.argv[2])
    visited = create_matrix(N, N, 0)
    prev = create_matrix(N, N, [])
    starting_row = int(sys.argv[3])
    starting_col = int(sys.argv[4])
    ending_row = int(sys.argv[5])
    ending_col = int(sys.argv[6])
    if len(sys.argv) == 7:
        matrix = create_matrix(N, N, 1)
        randomize_matrix(matrix, 0, k)
    if len(sys.argv) == 8:
        file = sys.argv[7]
        matrix = create_matrix_from_file(file)
    solve(starting_row, starting_col, ending_row, ending_col)
    path = deconstruct(starting_row, starting_col, ending_row, ending_col)
    pr_print_matrix(matrix, path)

import copy
import math
import sys


##############################################
#                 params                     #
##############################################
matrix = []
goal_matrix = []
possible_moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]
p_m = {'[-1, 0]': "left", '[1, 0]': "right", '[0, -1]': "up", '[0, 1]': "down"}
curent_blank_position = [-1, -1]


##############################################
#          functions for the matrix          #
##############################################
def validate_number_for_matrix(number):
    root = int(math.sqrt(number))
    return number == int(root + 0.5) ** 2


def init_size(number):
    return int(math.sqrt(number))


def init_blank_position(number, size):
    return [number // size, number % size]


def print_matrix(matrix, size):
    for i in range(0, size):
        print(matrix[i])


def create_matrix(size):
    matrix = []
    for i in range(0, size):
        row = [-1] * size
        matrix.append(row)
    return matrix


def shufle_matrix(matrix, sequence, curent_position, size):
    counter = 0
    for i in range(0, size):
        for j in range(0, size):
            if i == curent_position[0] and j == curent_position[1]:
                matrix[i][j] = 0
            else:
                matrix[i][j] = int(sequence[counter])
                counter = counter + 1
    return matrix


def create_goal_matrix(size):
    matrix = create_matrix(size)
    counter = 1
    for i in range(0, size):
        for j in range(0, size):
            matrix[i][j] = counter
            counter = counter + 1
    matrix[size - 1][size - 1] = 0
    return matrix


##############################################
#         functions for the sequence         #
##############################################
def create_list_from_file(file):
    seq = []
    with open(file) as f:
        seq_helper = f.readlines()
    for elem in seq_helper:
        seq.append(elem.replace("\n", ""))
    return seq


def check_if_goal_is_reached(matrix):
    size = len(matrix)
    helper = []
    for i in range(0, size):
        for j in range(0, size):
            helper.append(matrix[i][j])
    for i in range(0, size * size - 1):
        if helper[i] != i + 1:
            return False
    return True


##############################################
#         functions for movement             #
##############################################
def pairElements(x, y):
    return [x[0] + y[0], x[1] + y[1]]


def possibleMove(matrix, x):
    return x[0] >= 0 and x[0] < len(matrix) and x[1] >= 0 and x[1] < len(matrix[1])


def manhhatan_distance_helper(dx, dy):
    return abs(dx) + abs(dy)


def manhatan_distance(matrix, size):
    distance = 0
    for x in range(0, size):
        for y in range(0, size):
            value = int(matrix[x][y])
            if value != 0:
                targetX = (value - 1) // size
                targetY = (value - 1) % size
                dx = x - targetX
                dy = y - targetY
                distance = distance + manhhatan_distance_helper(dx, dy)
    return distance


def find_curent_blank_position(matrix):
    curent_blank_position = [-1, -1]
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if matrix[i][j] == 0:
                curent_blank_position = [i, j]
    return curent_blank_position


def create_possible_moves(matrix):
    curent_blank_position = find_curent_blank_position(matrix)
    result = list(map(lambda x: pairElements(
        x, curent_blank_position), possible_moves))
    result = list(filter(lambda x: possibleMove(matrix, x), result))
    return result


def move(matrix, step, cbs):
    kid = create_matrix(len(matrix))
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if i == step[0] and j == step[1]:
                kid[i][j] = 0
            elif i == cbs[0] and j == cbs[1]:
                kid[i][j] = matrix[step[0]][step[1]]
            else:
                kid[i][j] = matrix[i][j]
    return kid


def getChildren(matrix):
    cbp = find_curent_blank_position(matrix)
    children = []
    poss = create_possible_moves(matrix)
    helper = copy.deepcopy(matrix)
    for elem in poss:
        kid = move(matrix, elem, cbp)
        children.append(kid)
        matrix = helper
    return children


##############################################
#                  game                      #
##############################################
def idaStar(matrix, size):
    bound = manhatan_distance(matrix, size)
    path = [matrix]
    flag = False
    while flag is False:
        r = search(path, 0, bound)
        if r == 'FOUND':
            flag = True
            return (path, bound)
        if r == math.inf:
            return -1
        bound = r
    return r


def search(path, g, bound):
    curent_matrix = path[-1]
    curent_matrix_size = len(curent_matrix)
    f = g + manhatan_distance(curent_matrix, curent_matrix_size)
    if f > bound:
        return f
    if check_if_goal_is_reached(curent_matrix):
        return 'FOUND'
    minimum = math.inf
    children = getChildren(curent_matrix)
    for elem in children:
        if elem not in path:
            path.append(elem)
            t = search(path, g + 1, bound)
            if t == 'FOUND':
                return 'FOUND'
            if t < minimum:
                minimum = t
            del path[-1]
    return minimum


if __name__ == '__main__':
    N = int(sys.argv[1])
    i = int(sys.argv[2]) - 1
    file = sys.argv[3]
    if validate_number_for_matrix(N) is False:
        sys.exit(-1)
    size = init_size(N)
    matrix = create_matrix(size)
    curent_blank_position = init_blank_position(i, size)
    seq = create_list_from_file(file)
    matrix = shufle_matrix(matrix, seq, curent_blank_position, size)
    goal_matrix = create_goal_matrix(size)
    print("START WITH : ")
    print(matrix)
    r = idaStar(matrix, size)
    print("path")
    print(r[0])
    print("steps : ", r[1])
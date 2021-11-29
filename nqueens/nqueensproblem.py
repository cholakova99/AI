import sys
import time
import random


def random_generator(N):
    return [random.randint(0, N-1) for i in range(N)]


def nqueens(N):
    queens_seq = random_generator(N)
    return min_conflicts(queens_seq, N)


def min_conflicts(queens_seq, N, iters=1000):
    def random_pos(seq, func):
        return random.choice([i for i in range(N) if func(seq[i])])

    if iters < N:
        iters = N
    for i in range(iters):
        conflicts = find_conflicts(queens_seq, N)
        if sum(conflicts) == 0:
            return queens_seq
        col = random_pos(conflicts, lambda x: x > 0)
        vconfs = [hits_counter(queens_seq, N, col, row) for row in range(N)]
        queens_seq[col] = random_pos(vconfs, lambda x: x == min(vconfs))
    raise Exception("Incomplete solution: try more iterations.")


def find_conflicts(queens_seq, N):
    return [hits_counter(queens_seq, N, col, queens_seq[col]) for col in range(N)]


def hits_counter(queens_seq, N, col, row):
    total = 0
    for i in range(N):
        if i == col:
            continue
        if queens_seq[i] == row:
            total += 1
        diff = abs(col-i)
        if row - diff == queens_seq[i] or row + diff == queens_seq[i]:
            total += 1
    return total


def generate_solution(N):
    return [i for i in range(N)]


def print_solution(queens_seq, N):
    for i in range(N):
        row = ['_'] * N
        row[queens_seq[i]] = "*"
        print(''.join(row))


if __name__ == "__main__":
    N = int(sys.argv[1])
    start_time = time.time()
    s = nqueens(N)
    end_time = time.time()
    print_solution(s, N)
    print("finished in", end_time - start_time)
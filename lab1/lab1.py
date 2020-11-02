import numpy as np
import random

N = 7
P = np.array([[0.159, 0.177, 0.664],
              [    0, 0.439, 0.561],
              [    0, 0.173, 0.827]])

Pk = np.array([[0.458,     0, 0.542],
              [ 0.192, 0.195, 0.613],
              [ 0.544,     0, 0.456]])

def trans_matrices(matrix, eps=0.00001, p=False):
    n = 2
    curr_matrix = np.linalg.matrix_power(matrix, 2)
    delta = max([abs(x) for x in np.nditer((matrix - curr_matrix))])
    while delta > eps:
        if p:
            print("n:", n)
            print("delta:", delta)
            print(curr_matrix)
            print("")
        n += 1
        prev_matrix = curr_matrix
        curr_matrix = np.linalg.matrix_power(matrix, n)
        delta = max([abs(x) for x in np.nditer((prev_matrix - curr_matrix))])
    if p:
        print("n:", n)
        print("delta:", delta)
        print(curr_matrix)
        print("")
    return n

def find_stationar(matrix):
    # print(matrix)
    a = np.transpose(matrix)
    a = a - np.identity(3)
    a = np.vstack((a, [1, 1, 1]))
    b = np.array([0, 0, 0, 1])
    return np.linalg.lstsq(a, b, rcond=None)[0]

def find_distributions(matrix, start_distribution, eps=0.00001, p=False):
    r = find_stationar(matrix)
    n = 0
    curr_distr = np.array(start_distribution)
    delta = max(abs(curr_distr - r))
    while delta > eps:
        if p: print(n, ":", curr_distr)
        curr_distr = curr_distr.dot(matrix)
        delta = max(abs(curr_distr - r))
        n += 1
    if p: print(n, ":", curr_distr)
    return n

def calc_comebacks(matrix, start_pos, eps=0.001, p=False):
    r = find_stationar(matrix)
    curr_pos = start_pos
    R = 0
    n = 0
    b = 0
    delta = abs(R - r[start_pos - 1])
    while delta > eps:
        if p: print(n, b, R)
        x = random.random()
        curr_pos = (1 if x < matrix[curr_pos - 1][0]
        else 2 if x < matrix[curr_pos - 1][0] + matrix[curr_pos -1][1] else 3)
        if curr_pos == start_pos: b += 1
        n += 1
        R = b / n
        delta = abs(R - r[start_pos - 1])
    if p: print(n, b, R)
    return n




print(trans_matrices(P, p=True))
foo = find_stationar(P)
print(foo)
# print(foo.dot(P))
# print(find_distributions(P, [1, 0, 0], p=True))
# print(calc_comebacks(P, 3, p=True))
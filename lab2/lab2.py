import numpy as np

V = 7
Lambda = [[-3,  0,  1,  1,  1],
          [ 1, -3,  1,  0,  1],
          [ 0,  1, -2,  1,  0],
          [ 1,  1,  1, -3,  0],
          [ 1,  1,  0,  1, -3]]

def find_stationar(matrix):
    a = np.transpose(matrix)
    a = np.vstack((a, [1, 1, 1, 1, 1]))
    b = np.array([0, 0, 0, 0, 0, 1])
    return np.linalg.lstsq(a, b, rcond=None)[0]

def lambda_i(matrix, i):
    return sum(matrix[i]) - matrix[i][i]

def next_pos_i(matrix, curr_pos, lmbd):
    next_pos_val = np.random.random()
    next_pos = 0
    temp_val = 0
    for i in range(len(matrix)):
        val = matrix[curr_pos][i]
        if curr_pos == i: val = 0
        temp_val += val / lmbd
        if next_pos_val <= temp_val:
            next_pos = i
            break
    return next_pos

def simulate(matrix, start_pos=0, eps=0.001):
    size = len(matrix)
    curr_pos = start_pos
    l = 0
    t = 0
    lmbd = lambda_i(matrix, curr_pos)
    tau = np.random.exponential(1/lmbd)
    next_pos = next_pos_i(matrix, curr_pos, lmbd)
    r = [0] * len(matrix)
    nr = r.copy()
    
    t += tau
    l += 1
    curr_pos = next_pos
    lmbd = lambda_i(matrix, curr_pos)
    tau = np.random.exponential(1/lmbd)
    next_pos = next_pos_i(matrix, curr_pos, lmbd)
    nr[curr_pos] += 1
    d = max([(i/l) for i in nr])
    while (d >= eps):
        print(l, t, curr_pos, tau, d)
        r = nr.copy()
        t += tau
        l += 1
        curr_pos = next_pos
        lmbd = lambda_i(matrix, curr_pos)
        tau = np.random.exponential(1/lmbd)
        next_pos = next_pos_i(matrix, curr_pos, lmbd)
        nr[curr_pos] += 1
        d = max([abs(nr[i]/l - r[i]/(l-1)) for i in range(size)])
    print(l, t, curr_pos, tau, d)




# print(find_stationar(Lambda))
simulate(Lambda)
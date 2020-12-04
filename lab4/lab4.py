import numpy as np

LMBD = 4.742
MU = 2.33

def find_kolmogor_coeffs (lmbd, mu, M):
	size = M
	matrix = np.zeros((size, 3))
	matrix[0][0] = -lmbd
	matrix[0][1] = mu
	for i in range(1, size):
		matrix[i][0] = lmbd
		matrix[i][1] = -(lmbd + i * mu)
		matrix[i][2] = (i + 1) * mu
	return matrix

def find_stationar (lmbd, mu, M):
	p = lmbd / mu
	res = []
	for i in range(M + 1):
		r = (p**i) / np.math.factorial(i) * np.math.exp(-p)
		res.append(r)
	return res

def decrease_time(seq, d):
	for i in range(len(seq)):
		if (seq[i] > 0):
			seq[i] -= d
	return seq

def simulate (lmbd, mu, K):
	table = []
	curr_row = [0] * 7
	devices = [0] * 30
	event_num = 1
	event_type = 1
	t = np.random.exponential(1 / lmbd)
	process_time_d = np.random.exponential(1 / mu)
	next_req_time_d = np.random.exponential(1 / lmbd)
	min_process_time_d = process_time_d
	# fill first row
	curr_row[0] = event_num
	curr_row[1] = t
	curr_row[2] = event_type
	curr_row[3] = 1
	curr_row[4] = min_process_time_d
	curr_row[5] = next_req_time_d
	curr_row[6] = 1
	table.append(curr_row.copy())
	devices[0] = process_time_d
	event_num += 1
	while event_num <= K:
		curr_row[0] = event_num
		if min_process_time_d != -1 and min_process_time_d < next_req_time_d:
			event_type = 2
			t += min_process_time_d
			next_req_time_d -= min_process_time_d
			curr_row[1] = t
			curr_row[2] = event_type
			curr_row[3] = len([i for i in devices if i > 0]) - 1
			k = devices.index(min([i for i in devices if i > 0])) + 1
			if curr_row[3] > 0:
				devices = decrease_time(devices, min_process_time_d)
				min_process_time_d = min([i for i in devices if i > 0])
			else:
				devices = [0] * 20
				min_process_time_d = -1
			curr_row[4] = min_process_time_d
			curr_row[5] = next_req_time_d
			curr_row[6] = k
		else:
			event_type = 1
			t += next_req_time_d
			curr_row[1] = t
			curr_row[2] = event_type
			curr_row[3] = len([i for i in devices if i > 0]) + 1
			devices = decrease_time(devices, next_req_time_d)
			k = (devices.index(0) if 0 in devices else len(devices)) + 1
			process_time_d = np.random.exponential(1 / mu)
			devices[k - 1] = process_time_d
			min_process_time_d = min([i for i in devices if i > 0])
			next_req_time_d = np.random.exponential(1 / lmbd)
			curr_row[4] = min_process_time_d
			curr_row[5] = next_req_time_d
			curr_row[6] = k
		table.append(curr_row.copy())
		event_num += 1
	return table







# print("Kolmogorov's equations coeffs:")
# print(find_kolmogor_coeffs(LMBD, MU, 5))
# print("\nStationar values:")
# print(find_stationar(LMBD, MU, 8))

tmp = simulate(LMBD, MU, 10)
for i in tmp:
	for j in range(len(i)):
		if j in [1, 4, 5]:
			print("{:.5f}".format(i[j]), end =" ")
		else:
			print(i[j], end=" ")
	print("")
import numpy as np


def dynamic_task(A):
    n, m = A.shape
    OPT = np.zeros((n, m))
    X = np.zeros((n, m))
    for q in range(m):
        OPT[0, q] = A[0, q]
        X[0, q] = q
    for k in range(1, n):
        for q in range(m):
            total_sum = 0
            index_q = None
            for index in range(0, q + 1):
                temp_sum = sum([A[k, index], OPT[k - 1, q - index]])
                if index_q is None or total_sum < temp_sum:
                    total_sum = temp_sum
                    index_q = index
            OPT[k, q] = total_sum
            X[k, q] = index_q
    print('OPT:\n{0} '.format(OPT))
    print('X:\n{0} '.format(X))
    res_X = []
    rest_q = m
    for k in range(n - 1, -1, -1):
        res_X.append(X[k, int(rest_q - 1)])
        rest_q -= res_X[-1]
    res_X = list(reversed(res_X))
    opt_X = np.array(res_X)
    print('resources:\n{0}'.format(opt_X))


if __name__ == '__main__':
    # A = np.array([[0, 1, 2, 3],
    #               [0, 0, 1, 2],
    #               [0, 2, 2, 3]])
    # A = np.array([[0, 0.2, 0.25, 0.4,0.6],
    #               [0, 0.15, 0.3, 0.45,0.55],
    #               [0, 0.1, 0.3, 0.55,0.7],
    #               [0, 0.22, 0.4, 0.5,0.6]])
    A = np.array([[0, 10, 31, 42, 62, 76],
                  [0, 12, 24, 36, 52, 74],
                  [0, 12, 36, 45, 60, 77],
                  [0, 16, 37, 46, 63, 80]])
    dynamic_task(A)


import math

import numpy as np
from simplex_method import SimplexMethod


class ILP:

    def __init__(self, m, n, A, b, c):
        self.__m = m
        self.__n = n
        self.__A = A
        self.__b = b
        self.__c = c

    def solve(self):
        solve = self.dual_simplex(self.__A, self.__b, self.__c)
        return solve

    def add_condition(self, new_x, new_b, J):
        self.__A = np.c_[self.__A, np.zeros(self.__m)]
        self.__n += 1
        temp = np.zeros(self.__n)
        for index, j in enumerate(J):
            # temp[j] = abs(new_x[index] - int(new_x[index]))
            temp[j] = abs(new_x[index] - math.floor(new_x[index]))
        temp[-1] = -1
        self.__A = np.vstack([self.__A, temp])
        self.__m += 1
        self.__c = np.append(self.__c, 0)
        self.__b = np.append(self.__b, new_b - int(new_b))
        print('new A: {}'.format(self.__A))
        print('new b: {}'.format(self.__b))
        print('new c: {}'.format(self.__c))

    def get_A(self):
        return self.__A

    def dual_simplex(self, A, b, c):
        simplex = SimplexMethod(c, A, b)
        x, J_b = simplex.solve()
        opt_plan = []
        for i in x:
            opt_plan.append(round(float(i), 15))
        J_b.sort()
        return opt_plan, J_b


def Gauss_method(ILP, n):
    count = n
    while True:
        X, Jb = ILP.solve()
        Jb.sort()
        if len(X) == 0:
            print("Решение не совместно")
            return
        else:
            print("Базисный план задачи равен: {0}\nБазисные компоненты: {1}".format(X, Jb))
        new_variable = None
        j_index = None
        for index, j in enumerate(Jb):
            if not X[j].is_integer():
                new_variable = X[j]
                j_index = index
        if new_variable is None:
            # print("Базисный план в целых числах: {}".format(X))
            print('Решение в целых числах: {}'.format(X[:count]))
            return
        else:
            print("Базисный план не в целых числах, выбрана {0}-ая компонента:".format(j_index + 1))
            A = ILP.get_A()
            Ab = []
            for j in Jb:
                Ab.append(A[:, j])
            Ab = np.array(Ab).transpose()
            print("Базисная матрица Ab:\n {}".format(Ab))
            Ab_1 = np.linalg.inv(Ab)
            print("Матрица обратная базисной Ab-1:\n {}".format(Ab_1))
            An = []
            for j in [i for i in range(n) if i not in Jb]:
                An.append(A[:, j])
            An = np.array(An).transpose()
            print("Не базисная матрица An:\n {}".format(An))
            Abn = Ab_1.dot(An)
            print("Abn:\n {}".format(Abn))
            ILP.add_condition(Abn[j_index], new_variable, [i for i in range(n) if i not in Jb])
            n += 1


if __name__ == '__main__':
    m = 2
    n = 4
    A = np.array([[-4, 6, 1, 0],
                  [1, 1, 0, 1]])
    b = np.array([9, 4])
    c = np.array([-1, 2, 0, 0])
    # m = 2
    # n = 4
    # A = np.array([[3, 2, 1, 0],
    #               [-3, 2, 0, 1]])
    # b = np.array([6, 0])
    # c = np.array([0, 1, 0, 0])

    ILP = ILP(m, n, A, b, c)
    Gauss_method(ILP, n)

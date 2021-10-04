import math

from copy import copy
import numpy as np
import method

stack = []
record = None
x_b = None


class ILP:

    def __init__(self, m, n, A, b, c, number):
        self.__m = m
        self.__n = n
        self.__A = A
        self.__b = b
        self.__c = c
        self.__number = number

    def solve(self):
        return method.first_and_second_step_simplex_method(self.__A, self.__b, self.__c)

    def add_condition(self, index, value, count_variables, direction):
        global temp, is_consist
        is_consist = []
        conditions = self.__A[:, 0:count_variables]
        new_condition = np.zeros(count_variables)
        new_condition[index] = 1
        new_variable_index = np.where(conditions == new_condition)[0]
        if new_variable_index is not None:
            for index in new_variable_index:
                temp = self.__A[index][count_variables:]
                if direction:
                    is_consist = np.where(temp == -1)[0]
                else:
                    is_consist = np.where(temp == 1)[0]
                if len(is_consist):
                    break
        A = copy(self.__A)
        b = copy(self.__b)
        m = copy(self.__m)
        n = copy(self.__n)
        c = copy(self.__c)
        number = copy(self.__number)
        if direction:
            number += '2'
            print("Добавлено условие {0} - c ограничением x >= {1}".format(number, value))
        else:
            number += '1'
            print("Добавлено условие {0} - c ограничением x <={1}".format(number, value))
        if len(is_consist):
            new_condition = np.concatenate((new_condition, temp))
            A[index,] = new_condition
            b[index] = value
            A[index,] = new_condition
            b[index] = value
        else:
            A = np.c_[A, np.zeros(m)]
            temp = np.zeros(len(A[0]) - count_variables)
            if direction:
                temp[-1] = -1
            else:
                temp[-1] = 1
            new_condition = np.concatenate((new_condition, temp))
            A = np.vstack([A, new_condition])
            c = np.append(c, 0)
            b = np.append(b, value)
            m += 1
            n += 1

        return ILP(m, n, A, b, c, number)

    def get_number(self):
        return self.__number


def branch_and_bound(count_variables):
    global new_variable_index, record, x_b
    while len(stack) != 0:
        current_ilp_task = stack.pop()
        print("Решаем задачу {}".format(current_ilp_task.get_number()))
        x = current_ilp_task.solve()
        if len(x) == 0:
            # if x is None:
            print("Решение не совместно")
            continue
        else:
            print("Базисный план задачи {0}: {1}".format(current_ilp_task.get_number(), x[:count_variables]))
        new_variable = None
        for x_index in x[:count_variables]:
            if not x_index.is_integer():
                new_variable = x_index
                new_variable_index = np.where(x == x_index)[0][0]
                break
        if new_variable is None:
            print("Базисный план в целых числах")
            r = math.floor(c[:count_variables].dot(x[:count_variables]))
            if record:
                if record >= r:
                    print("Рекорд не больше текущего: {0} < {1} \nВетвление останавливается".format(r, record))
                    continue
                else:
                    print("Рекорд обновлен: {0}".format(r))
                    record = r
                    x_b = x[:count_variables]
                    continue
            elif record is None:
                print("Рекорд обновлен: {0}".format(r))
                record = r
                x_b = x[:count_variables]
                continue
        else:
            print("Базисный план не в целых числах, выбрана {0}-ая компонента:".format(new_variable_index + 1))

        ceil_border = math.ceil(new_variable)
        floor_border = math.floor(new_variable)

        new_ilp_task = current_ilp_task.add_condition(new_variable_index, ceil_border, count_variables, True)
        stack.append(new_ilp_task)
        new_ilp_task = current_ilp_task.add_condition(new_variable_index, floor_border, count_variables, False)
        stack.append(new_ilp_task)


if __name__ == "__main__":
    count_variables = 2
    # m = 5
    # n = 7
    # A = np.array([[4, 3, 1, 0, 0, 0, 0],
    #               [-4, 3, 0, 1, 0, 0, 0],
    #               [1, 0, 0, 0, -1, 0, 0],
    #               [1, 0, 0, 0, 0, 1, 0],
    #               [0, 1, 0, 0, 0, 0, 1]])
    # b = np.array([22, 2, 1, 4, 5])
    # c = np.array([-5, 4, 0, 0, 0, 0, 0])
    m = 2
    n = 4
    A = np.array([[5, 7, 1, 0],
                  [4, 9, 0, 1]])
    b = np.array([35, 36])
    c = np.array([2, 3, 0, 0])
    stack.append(ILP(m, n, A, b, c, '1'))
    branch_and_bound(count_variables)
    print("Базисный план в целых числах:\n {}".format(x_b))

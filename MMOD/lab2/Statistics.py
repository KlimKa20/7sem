import matplotlib.pyplot as plt


class Statistics:

    def __init__(self, model, X, Y, R, y, limit_of_requests, duration):
        self.__model = model
        self.__X = X
        self.__Y = Y
        self.__R = R
        self.__y = y
        self.__duration = duration
        self.__limit_of_requests = limit_of_requests

        self.__reject = 0

        self.__free = 0
        self.__work = 0
        self.__broke = 0

    def reject(self):
        self.__reject += 1

    def collect(self):
        if self.__model.get_channel().is_broke():
            self.__broke += 1
        elif self.__model.get_channel().is_free():
            self.__free += 1
        else:
            self.__work += 1

    def get_e_prob(self):
        return self.__free / (self.__broke + self.__free + self.__work), self.__work / (
                self.__broke + self.__free + self.__work), self.__broke / (
                       self.__broke + self.__free + self.__work)

    def get_t_prob(self):
        p2 = 1 / (1 + self.__R * (self.__Y / self.__X + 2) / (self.__X + self.__y + self.__y * self.__Y / self.__X))
        p1 = p2 * self.__R / (self.__X + self.__y + self.__y * self.__Y / self.__X)
        p0 = p1 * (self.__Y / self.__X + 1)
        return round(p0, 15), round(p1, 15), round(p2, 15)

    def show_chart(self):
        X = [0, 1, 2]
        values = self.get_t_prob()
        fig, ax = plt.subplots(1, 1)
        ax.bar(X, values, width=0.1)
        ax.set_title('Theoretical_histogram')
        plt.show()

    def generate(self):
        print('\nX:{}'.format(self.__X))
        print('Y:{}'.format(self.__Y))
        print('R:{}'.format(self.__R))
        print('y:{}'.format(self.__y))
        print('duration:{}'.format(self.__duration))

        self.show_chart()

        e_prob = self.get_e_prob()
        print('p0:{0}\np1:{1}\np2:{2}'.format(e_prob[0], e_prob[1], e_prob[2]))
        print('Полная теоретическая вероятность:{}'.format(sum(e_prob)))
        t_prob = self.get_t_prob()
        print('\np0:{0}\np1:{1}\np2:{2}'.format(t_prob[0], t_prob[1], t_prob[2]))
        print('Полная практическая вероятность:{}'.format(sum(t_prob)))

        print('\nВероятность отказа(Практическая): {}'.format(sum(t_prob[1:])))
        relative_bandwidth_t = t_prob[0]
        print('Относительная пропускная способность(Практическая): {}'.format(relative_bandwidth_t))
        print('\nВероятность отказа(Практическая): {}'.format(sum(e_prob[1:])))
        relative_bandwidth_e = e_prob[0]
        print('Относительная пропускная способность(Практическая): {}'.format(relative_bandwidth_e))

        absolute_bandwidth_t = relative_bandwidth_t * self.__X
        print('\nАбсолютная пропускная способность(Практическая): {}'.format(absolute_bandwidth_t))
        absolute_bandwidth_e = relative_bandwidth_e * self.__X
        print('Абсолютная пропускная способность(Практическая): {}'.format(absolute_bandwidth_e))

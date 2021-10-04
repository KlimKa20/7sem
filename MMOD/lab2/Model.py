from Channel import *
from Request import *
from Statistics import *


class Model:

    def __init__(self, X, Y, R, y, limit_of_requests, duration):
        self.__X = X
        self.__Y = Y
        self.__R = R
        self.__y = y

        self.__limit_of_requests = limit_of_requests
        self.__number_of_requests = 0

        self.__duration = duration

        self.__channel = Channel(X, Y, R, y, duration)

        self.__ctime = 0
        self.__ntime = np.random.exponential(1/X)

        self.__statistics = Statistics(self, X, Y, R, y, limit_of_requests, duration)

    def step(self):
        result = self.__channel.step()
        if result is not None and result == 'reject':
            self.__statistics.reject()
        self.__statistics.collect()
        self.__ctime += self.__duration
        self.__ntime -= self.__duration

    def get_channel(self):
        return self.__channel

    def add_request(self):
        self.__number_of_requests += 1
        request = Request()
        if self.__channel.is_broke():
            self.__statistics.reject()
            print("Заявка {} отклонена(канал отказал)".format(request.get_count()))
        elif not self.__channel.is_free():
            self.__statistics.reject()
            print("Заявка {} отклонена(канал занят)".format(request.get_count()))
        else:
            print("Заявка {} поступила в обработку".format(request.get_count()))
            self.__channel.run(request)

    def free(self):
        while not self.__channel.is_free():
            self.step()

    def run(self):
        while self.__number_of_requests < self.__limit_of_requests:
            if self.__ntime <= 0:
                self.add_request()
                self.__ntime = np.random.exponential(1/self.__X)
            self.step()

        self.free()

        return self.__statistics

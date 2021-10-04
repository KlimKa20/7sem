import numpy as np
import simpy


class Model:
    def __init__(self, X, Y, R, y, env):
        self.__X = X
        self.__Y = Y
        self.__R = R
        self.__y = y
        self.__env = env
        self.__request = simpy.Resource(env)

        self.__free = True
        self.__broke = False

        self.__stat = []

        self.__count = 0

        self.system_free = env.event()
        self.system_broke = env.event()

        env.process(self.broke_without_work())
        env.process(self.fix())
        env.process(self.run())

    def run(self):
        self.system_free.succeed()
        self.system_free = self.__env.event()
        while True:
            yield self.__env.timeout(np.random.exponential(1 / self.__X))
            self.__env.process(self.add_request())

    def free(self):
        print("Заявка {0} выполнена в {1}".format(self.__count, self.__env.now))
        self.__free = True
        self.system_free.succeed()
        self.system_free = self.__env.event()

    def broke(self):
        self.__broke = True
        self.system_broke.succeed()
        self.system_broke = self.__env.event()

    def fix(self):
        while True:
            yield self.system_broke
            yield self.__env.timeout(np.random.exponential(1 / self.__R))
            self.__free = True
            self.__broke = False
            print("Канал востановлен в {0}".format(self.__env.now))
            self.system_free.succeed()
            self.system_free = self.__env.event()

    def broke_without_work(self):
        while True:
            yield self.system_free
            if self.__free and not self.__broke:
                yield self.__env.timeout(np.random.exponential(1 / self.__y))
            if self.__free and not self.__broke:
                print("Канал отказал во время простоя в {0}".format(self.__env.now))
                self.broke()

    def collect(self):
        if self.__free and not self.__broke:
            self.__stat.append(0)
        elif not self.__free and not self.__broke:
            self.__stat.append(1)
        else:
            self.__stat.append(2)

    def add_request(self):
        active_channel = self.__request.count
        with self.__request.request() as Request:
            self.collect()
            self.__count += 1
            if active_channel == 0 and not self.__broke:
                print("Заявка {0} поступила в обработку в {1}".format(self.__count, self.__env.now))
                yield Request
                print("Заявка {0} начала обработку в {1}".format(self.__count, self.__env.now))
                self.__free = False
                t1, t2 = self.__env.timeout(np.random.exponential(1 / self.__Y), value='accept'), self.__env.timeout(
                    np.random.exponential(1 / self.__X), value='broke')
                res = yield t1 | t2
                if res == {t1: 'accept'}:
                    self.free()
                elif res == {t2: 'broke'}:
                    print("Заявка {0} отклонена(канал отказал) в {1}".format(self.__count, self.__env.now))
                    self.broke()
            elif self.__broke:
                print("Заявка {0} отклонена(канал сломан) в {1}".format(self.__count, self.__env.now))
            elif active_channel == 1:
                print("Заявка {0} отклонена(канал занят) в {1}".format(self.__count, self.__env.now))

    def get_data_for_statistic(self):
        return self.__stat


# import numpy as np
# import simpy
#
#
# class Model:
#     def __init__(self, X, Y, R, y, env):
#         self.__X = X
#         self.__Y = Y
#         self.__R = R
#         self.__y = y
#         self.__env = env
#         self.__request = simpy.Resource(env)
#
#         self.__free = True
#         self.__broke = False
#
#         self.__stat = []
#
#         self.__count = 0
#
#     # def run(self):
#     #     # yield self.__env.process(self.fix())
#     #     while True:
#     #         yield self.__env.timeout(np.random.exponential(1 / self.__X))
#     #         self.__env.process(self.add_request())
#
#     def run(self):
#         # yield self.__env.process(self.fix())
#         while True:
#             yield self.__env.timeout(np.random.exponential(1 / self.__X))
#             self.__env.process(self.add_request())
#             if self.__broke:
#                 self.__env.process(self.fix_test())
#
#     # def run(self):
#     #     while True:
#     #         if self.__free and not self.__broke:
#     #             t1, t2 = self.__env.timeout(np.random.exponential(1 / self.__X), value='new'), self.__env.timeout(
#     #                 np.random.exponential(1 / self.__y), value='broke')
#     #             res = yield t1 | t2
#     #             if res == {t1: 'new'}:
#     #                 self.__env.process(self.add_request())
#     #             elif res == {t2: 'broke'}:
#     #                 self.broke()
#     #                 yield self.__env.process(self.fix_test())
#     #         else:
#     #             yield self.__env.timeout(np.random.exponential(1 / self.__X))
#     #             self.__env.process(self.add_request())
#
#     def free(self):
#         print("Заявка {0} выполнена в {1}".format(self.__count, self.__env.now))
#         self.__free = True
#
#     def fix(self):
#         while True:
#             if self.__broke:
#                 yield self.__env.timeout(np.random.exponential(1 / self.__R))
#                 self.__free = True
#                 self.__broke = False
#                 print("Канал востановлен в {0}".format(self.__env.now))
#
#     def broke(self):
#         print("Заявка {0} отклонена во время обработки(отказ канала) в {1}".format(self.__count, self.__env.now))
#         self.__broke = True
#
#     def fix_test(self):
#         yield self.__env.timeout(np.random.exponential(1 / self.__R))
#         self.__free = True
#         self.__broke = False
#         print("Канал востановлен в {0}".format(self.__env.now))
#
#     def broke_without_work(self):
#         while True:
#             if self.__free and not self.__broke:
#                 yield self.__env.timeout(np.random.exponential(1 / self.__y))
#             if self.__free and not self.__broke:
#                 print("Канал отказал во время простоя в {0}".format(self.__env.now))
#                 self.__env.process(self.broke())
#
#     def collect(self):
#         if self.__free and not self.__broke:
#             self.__stat.append(0)
#         elif not self.__free and not self.__broke:
#             self.__stat.append(1)
#         else:
#             self.__stat.append(2)
#
#     def add_request(self):
#         active_channel = self.__request.count
#         with self.__request.request() as Request:
#             self.collect()
#             self.__count += 1
#             if active_channel == 0 and not self.__broke:
#                 print("Заявка {0} поступила в обработку в {1}".format(self.__count, self.__env.now))
#                 yield Request
#                 print("Заявка {0} начала обработку в {1}".format(self.__count, self.__env.now))
#                 self.__free = False
#                 t1, t2 = self.__env.timeout(np.random.exponential(1 / self.__Y), value='accept'), self.__env.timeout(
#                     np.random.exponential(1 / self.__X), value='broke')
#                 res = yield t1 | t2
#                 if res == {t1: 'accept'}:
#                     self.free()
#                 elif res == {t2: 'broke'}:
#                     self.broke()
#                     yield self.__env.process(self.fix_test())
#             elif self.__broke:
#                 print("Заявка {0} отклонена(канал отказал) в {1}".format(self.__count, self.__env.now))
#             elif active_channel == 1:
#                 print("Заявка {0} отклонена(канал занят) в {1}".format(self.__count, self.__env.now))

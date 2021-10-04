import numpy as np


class Channel:

    def __init__(self, X, Y, R, y, duration):
        self.__broke = False
        self.__free = True

        self.__X = X
        self.__Y = Y
        self.__R = R
        self.__y = y
        self.__duration = duration

        self.__nwb_time = np.random.exponential(1/y)
        self.__wb_time = None
        self.__free_time = None
        self.__fix_time = None

        self.__request = None

    def broke(self):
        self.__fix_time = np.random.exponential(1/self.__R)
        self.__broke = True
        self.__free = True

    def recovery(self):
        self.__nwb_time = np.random.exponential(1/self.__y)
        self.__broke = False

    def take_free(self):
        self.__nwb_time = np.random.exponential(1/self.__y)
        self.__free = True

    def run(self, request):
        self.__free = False
        self.__request = request
        self.__request.run()
        self.__free_time = np.random.exponential(1/self.__Y)
        self.__wb_time = np.random.exponential(1/self.__X)

    def is_free(self):
        return self.__free

    def is_broke(self):
        return self.__broke

    def step(self):
        if self.is_broke():
            self.__fix_time -= self.__duration
            if self.__fix_time <= 0:
                print("Канал востановлен")
                self.recovery()
        elif self.is_free():
            self.__nwb_time -= self.__duration
            if self.__nwb_time <= 0:
                print("Канал отказал во время простоя")
                self.broke()
        else:
            self.__free_time -= self.__duration
            if self.__free_time <= 0:
                print("Заявка {} выполнена".format(self.__request.get_count()))
                self.take_free()
                return 'accept'
            self.__wb_time -= self.__duration
            if self.__wb_time <= 0:
                print("Заявка {} отклонена во время обработки(отказ канала)".format(self.__request.get_count()))
                self.broke()
                return 'reject'
#
#
# import numpy as np
#
#
# class Channel:
#
#     def __init__(self, X, Y, R, y, duration):
#         self.__broke = False
#         self.__free = True
#
#         self.__X = X
#         self.__Y = Y
#         self.__R = R
#         self.__y = y
#         self.__duration = duration
#
#         self.__nwb_time = np.random.exponential(y)
#         self.__wb_time = np.random.exponential(X)
#         self.__free_time = None
#         self.__fix_time = None
#
#         self.__request = None
#
#     def broke(self):
#         self.__fix_time = np.random.exponential(self.__R)
#         self.__broke = True
#         self.__free = True
#
#     def recovery(self):
#         self.__broke = False
#
#     def take_free(self):
#         self.__free = True
#
#     def run(self, request):
#         self.__free = False
#         self.__request = request
#         self.__request.run()
#         self.__free_time = np.random.exponential(self.__Y)
#
#     def is_free(self):
#         return self.__free
#
#     def is_broke(self):
#         return self.__broke
#
#     def step(self):
#         if self.is_broke():
#             self.__fix_time -= self.__duration
#             if self.__fix_time <= 0:
#                 print("Канал востановлен")
#                 self.recovery()
#         elif self.is_free():
#             self.__nwb_time -= self.__duration
#             if self.__nwb_time <= 0:
#                 print("Канал отказал во время простоя")
#                 self.broke()
#                 self.__nwb_time = np.random.exponential(self.__y)
#         else:
#             self.__free_time -= self.__duration
#             if self.__free_time <= 0:
#                 print("Заявка {} выполнена".format(self.__request.get_count()))
#                 self.take_free()
#                 return 'accept'
#                 # return self.__request
#             self.__wb_time -= self.__duration
#             if self.__wb_time <= 0:
#                 print("Заявка {} отклонена во время обработки(отказ канала)".format(self.__request.get_count()))
#                 self.broke()
#                 self.__wb_time = np.random.exponential(self.__X)
#                 return 'reject'
#                 # return self.__request, 'reject'
#

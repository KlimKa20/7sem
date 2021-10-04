class Request:
    COUNT = 0

    def __init__(self):
        Request.COUNT += 1
        self.__count = Request.COUNT

    def run(self):
        pass

    def get_count(self):
        return self.__count

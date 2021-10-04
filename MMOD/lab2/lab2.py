from Model import *

if __name__ == '__main__':
    X = 3

    tobs = 1
    tr = 4
    tww = 500

    # Y = 1 / tobs
    # R = 1 / tr
    # y = 1 / tww

    Y = 6
    R = 1.5
    y = 2
    # X = 1/6
    #
    # tobs = 1
    # tr = 4
    # tww = 500
    #
    # # Y = 1 / tobs
    # # R = 1 / tr
    # # y = 1 / tww
    #
    # Y = 1/3
    # R = 1/1.5
    # y = 1/2

    model = Model(X, Y, R, y, 10000, 0.0001)
    statistics = model.run()
    statistics.generate()

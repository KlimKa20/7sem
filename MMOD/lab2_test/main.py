import simpy
import Model
import Statistics
import numpy as np

if __name__ == '__main__':
    time = 3000
    X = 3
    Y = 6
    R = 1.5
    y = 2

    env = simpy.Environment()
    model = Model.Model(X, Y, R, y, env)
    env.run(time)

    Statistic = Statistics.Statistics(X, Y, R, y,np.array(model.get_data_for_statistic()))
    Statistic.generate()

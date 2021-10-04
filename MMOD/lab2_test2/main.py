import simpy
import Model
import Statistics

if __name__ == '__main__':
    time = 3000

    # _lambda = 9
    # mu = 4
    # v = 1
    # m = 2
    # n = 1
    _lambda = 10
    mu = 3
    v = 6
    m = 4
    n = 3

    env = simpy.Environment()
    model = Model.Model(_lambda, mu, v, m, n, env)
    env.run(time)

    Statistic = Statistics.Statistics(_lambda, mu, v, m, n, model.get_data_for_statistic())
    Statistic.generate()

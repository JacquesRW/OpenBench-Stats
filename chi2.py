from core import Test

class Chi2:
    __crit_vals_99 = [
        1000.0,  6.635,  9.210, 11.345, 13.277,
        15.086, 16.812, 18.475, 20.090, 21.666,
        23.209, 24.725, 26.217, 27.688, 29.141,
        30.578, 32.000, 33.409, 34.805, 36.191,
        37.566, 38.932, 40.289, 41.638, 42.980,
        44.314, 45.642, 46.963, 48.278, 49.588,
        50.892, 52.191, 53.486, 54.776, 56.061,
    ]

    @staticmethod
    def __statistic(sprt: Test) -> tuple[float, int]:
        results = [0, 0, 0]

        for worker in sprt.workers():
            worker_results = worker.results()
            for i in range(3):
                results[i] += worker_results[i]

        for result in results:
            if result == 0:
                return None, 0

        played = sum(results)
        proportions = [result / played for result in results]

        statistic = 0.0
        most_anomalous, worst = 0, 0.0

        for num, worker in enumerate(sprt.workers()):
            worker_results = worker.results()
            worker_played = sum(worker_results)

            worker_anomaly = 0.0
            for i in range(3):
                expected = proportions[i] * worker_played
                stat = pow(worker_results[i] - expected, 2) / expected
                worker_anomaly += stat
                statistic += stat

            if worker_anomaly > worst:
                most_anomalous = num
                worst = worker_anomaly

        return statistic, most_anomalous

    @staticmethod
    def test(sprt: Test) -> tuple[bool, int]:
        statistic, most_anomalous = Chi2.__statistic(sprt)
        degrees_of_freedom = 2 * (len(sprt.workers()) - 1)
        if statistic is None or degrees_of_freedom >= len(Chi2.__crit_vals_99):
            return None, 0

        return statistic > Chi2.__crit_vals_99[degrees_of_freedom], most_anomalous

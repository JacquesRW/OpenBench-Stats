from core import Test

class Chi2:
    __crit_vals_95 = [
           0.0,  3.841,  5.991,  7.815,  9.488,
        11.070, 12.592, 14.067, 15.507, 16.919,
        18.307, 19.675, 21.026, 22.362, 23.685,
        24.996, 26.296, 27.587, 28.869, 30.144,
        31.410, 32.671, 33.924, 35.172, 36.415,
        37.652, 38.885, 40.113, 41.337, 42.557,
        43.773, 44.985, 46.194, 47.400, 48.602,
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

        for i, worker in enumerate(sprt.workers()):
            worker_results = worker.results()
            worker_played = sum(worker_results)

            worker_anomaly = 0.0
            for i in range(3):
                expected = proportions[i] * worker_played
                stat = pow(worker_results[i] - expected, 2) / expected
                worker_anomaly += stat
                statistic += stat

            if worker_anomaly > worst:
                most_anomalous = i

        return statistic, most_anomalous

    @staticmethod
    def test(sprt: Test) -> tuple[bool, int]:
        statistic, most_anomalous = Chi2.__statistic(sprt)
        degrees_of_freedom = 2 * (len(sprt.workers()) - 1)
        if statistic is None or degrees_of_freedom >= len(Chi2.__crit_vals_95):
            return None, 0

        return statistic > Chi2.__crit_vals_95[degrees_of_freedom], most_anomalous

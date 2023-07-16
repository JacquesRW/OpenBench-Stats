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
    def __statistic(sprt: Test) -> float:
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

        num_workers = 0
        for worker in sprt.workers():
            worker_results = worker.results()
            worker_played = sum(worker_results)
            if worker_played == 0:
                continue

            num_workers += 1
            for i in range(3):
                expected = proportions[i] * worker_played
                stat = pow(worker_results[i] - expected, 2) / expected
                statistic += stat

        return statistic, num_workers

    @staticmethod
    def test(sprt: Test) -> bool:
        statistic, num_workers = Chi2.__statistic(sprt)
        degrees_of_freedom = 2 * (num_workers - 1)
        if statistic is None or degrees_of_freedom >= len(Chi2.__crit_vals_95):
            return None

        return statistic > Chi2.__crit_vals_95[degrees_of_freedom]


def test_sprts(instance: str, start: int, end: int):
    anomalies = []

    for test_number in reversed(range(start, end + 1)):
        sprt = Test(instance, test_number)
        test = Chi2.test(sprt)
        if test:
            anomalies.append(sprt.url())
            print(f"Anomaly Detected: {sprt.url()}")
        elif test is None:
            print(f"Can't Calculate: {sprt.url()}")
        else:
            print(f"A-Okay: {sprt.url()}")

    print("Anomalies:")
    for anomaly in anomalies:
        print(anomaly)

if __name__ == "__main__":
    instance = "https://chess.swehosting.se"

    test_sprts(instance, 2500, 2599)
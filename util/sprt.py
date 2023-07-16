import math
from dataclasses import dataclass
from util.core import Test


@dataclass
class Probability:
    win: float
    loss: float
    draw: float


@dataclass
class BayesElo:
    elo: float
    draw: float


class Sprt:
    H1 = 2
    NA = 1
    H0 = 0

    @staticmethod
    def __expected_score(x: float) -> float:
        return 1.0 / (1.0 + math.pow(10, -x / 400.0))

    @staticmethod
    def __adj_probs(b: BayesElo) -> Probability:
        win  = Sprt.__expected_score(-b.draw + b.elo)
        loss = Sprt.__expected_score(-b.draw - b.elo)
        return Probability(win, loss, 1 - win - loss)

    @staticmethod
    def __llr(w: int, l: int, d: int, e0: float, e1: float) -> float:
        if w == 0 or l == 0 or d == 0:
            return 0.0

        total = w + d + l

        probs = Probability(w / total, l / total, d / total)

        draw_elo = 200 * math.log10((1 - 1 / probs.win) * (1 - 1 / probs.loss))

        b0 = BayesElo(e0, draw_elo)
        b1 = BayesElo(e1, draw_elo)

        p0 = Sprt.__adj_probs(b0)
        p1 = Sprt.__adj_probs(b1)

        return w * math.log(p1.win  / p0.win ) \
             + l * math.log(p1.loss / p0.loss) \
             + d * math.log(p1.draw / p0.draw)


    @staticmethod
    def sprt(test: Test, e0: float, e1: float) -> tuple[int, float]:
        results = [0, 0, 0]
        for worker in test.workers():
            worker_results = worker.results()
            for i in range(3):
                results[i] += worker_results[i]

        [w, l, d] = results
        llr = Sprt.__llr(w, l, d, e0, e1)
        return (llr >= -2.94) + (llr > 2.94), llr


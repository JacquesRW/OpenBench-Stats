import math
from math import sqrt, log, log10, copysign, pi
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


def erf_inv(x):
    a = 8 * (pi - 3) / (3 * pi * (4 - pi))
    y = log(1 - x * x)
    z = 2 / (pi * a) + y / 2
    return copysign(sqrt(sqrt(z * z - y / a) - z), x)


def phi_inv(p):
    return sqrt(2) * erf_inv(2 * p - 1)


def elo(score: float) -> float:
    if score <= 0 or score >= 1:
        return 0.0
    return -400 * log10(1 / score - 1)


class Sprt:
    H1 = 2
    NA = 1
    H0 = 0

    @staticmethod
    def __expected_score(x: float) -> float:
        return 1.0 / (1.0 + math.pow(10, -x / 400.0))

    @staticmethod
    def __adj_probs(b: BayesElo) -> Probability:
        win = Sprt.__expected_score(-b.draw + b.elo)
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

        return w * math.log(p1.win / p0.win) \
            + l * math.log(p1.loss / p0.loss) \
            + d * math.log(p1.draw / p0.draw)

    @staticmethod
    def sprt(test: Test, e0: float, e1: float) -> tuple[int, float]:
        w, l, d = test.results()
        llr = Sprt.__llr(w, l, d, e0, e1)
        return (llr >= -2.94) + (llr > 2.94), llr

    @staticmethod
    def elo(test: Test):
        wins, losses, draws = test.results()
        # win/loss/draw ratio
        N = wins + losses + draws
        if N == 0:
            return (0, 0, 0)

        p_w = float(wins) / N
        p_l = float(losses) / N
        p_d = float(draws) / N

        mu = p_w + p_d / 2
        stdev = sqrt(p_w * (1 - mu)**2 + p_l * (0 - mu)**2 + p_d * (0.5 - mu)**2) / sqrt(N)

        # 95% confidence interval for mu
        mu_min = mu + phi_inv(0.025) * stdev
        mu_max = mu + phi_inv(0.975) * stdev

        return (elo(mu_min), elo(mu), elo(mu_max))

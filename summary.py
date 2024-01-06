from util.core import Test
from util.chi2 import Chi2
from util.sprt import Sprt

HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def fmt(line: str, fmtter: str) -> str:
    return fmtter + line + ENDC + "\n"


def add_outcome(summary, test, e0, e1):
    sprt_result, llr = Sprt.sprt(test, e0, e1)
    return summary + fmt(f"[{e0: >2}, {e1}] LLR {llr: >5.2f}", [RED, YELLOW, GREEN][sprt_result])


def summary(sprt: Test) -> str:
    # carry out chi2 test
    anomalous, most = Chi2.test(sprt)

    # generate summary strings
    summary = f"CREATOR: {sprt.creator()}\n"
    summary += f"ENGINE : {sprt.engine()}\n"
    summary += f"URL    : {UNDERLINE}{sprt.url()}{ENDC}\n"
    summary += f"DIFF   : {UNDERLINE}{sprt.diff()}{ENDC}\n\n"

    summary += fmt("ID  :OWNER       :GAMES :WINS  :LOSSES:DRAWS", BLUE + BOLD)
    for i, worker in enumerate(sprt.workers()):
        if sum(worker.results()) > 0:
            if anomalous and most == i:
                summary += fmt(str(worker) + "<-- Most Anomalous Worker", RED + BOLD)
            else:
                summary += str(worker) + "\n"

    if anomalous:
        summary += "\n" + fmt("Anomaly detected, SPRT rejected.", RED + BOLD) + "\n"
    else:
        summary += "\n" + fmt("No anomalous workers detected.", GREEN + BOLD) + "\n"

    summary += "ELO: "
    e1, e2, e3 = Sprt.elo(test)
    summary += f"{round(e2, 2)} +- {round((e3 - e1) / 2, 2)}\n"

    summary += "\nPossible SPRT Results\n"
    summary = add_outcome(summary, test, -5, 0)
    summary = add_outcome(summary, test, -3, 1)
    summary = add_outcome(summary, test, 0, 3)
    summary = add_outcome(summary, test, 0, 5)

    print(summary)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--instance',
        type=str,
        default="https://chess.swehosting.se",
        help="URL of the target instance."
    )
    parser.add_argument('-t', '--test', type=int, default=1, help="Test number to analyse.")
    args = parser.parse_args()

    test = Test(args.instance, args.test)
    summary(test)

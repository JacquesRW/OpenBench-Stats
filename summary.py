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

    summary += "Possible SPRT Results\n"
    for i in [3, 5, 10]:
        sprt_result, llr = Sprt.sprt(test, 0, i)
        summary += fmt(f"[0, {i: >2}] LLR {llr: >5.2f}", [RED, YELLOW, GREEN][sprt_result])

    print(summary)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instance', type=str, default="https://chess.swehosting.se", help="URL of the target instance.")
    parser.add_argument('-t', '--test', type=int, default=1, help="Test number to analyse.")
    args = parser.parse_args()

    test = Test(args.instance, args.test)
    summary(test)
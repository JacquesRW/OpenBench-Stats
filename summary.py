from core import Test
from chi2 import Chi2

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def summary(sprt: Test) -> str:
    # carry out chi2 test
    anomalous, most = Chi2.test(sprt)

    # generate summary strings
    summary = f"CREATOR: {sprt.creator()}\n"
    summary += f"ENGINE : {sprt.engine()}\n"
    summary += f"URL    : {UNDERLINE}{sprt.url()}{ENDC}\n"
    summary += f"DIFF   : {UNDERLINE}{sprt.diff()}{ENDC}\n\n"

    summary += OKBLUE + BOLD + "ID  :OWNER       :GAMES :WINS  :LOSSES:DRAWS" + ENDC + "\n"
    for i, worker in enumerate(sprt.workers()):
        if sum(worker.results()) > 0:
            if anomalous and most == i:
                summary += FAIL + BOLD + str(worker) + "<-- Most Anomalous Worker" + ENDC + "\n"
            else:
                summary += str(worker) + "\n"

    if anomalous:
        summary += "\n" + FAIL + BOLD + "Anomaly detected, SPRT rejected." + ENDC + "\n"
    else:
        summary += "\n" + FAIL + OKGREEN + "We gamin'." + ENDC + "\n"

    print(summary)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instance', type=str, default="https://chess.swehosting.se", help="URL of the target instance.")
    parser.add_argument('-t', '--test', type=int, default=1, help="Test number to analyse.")
    args = parser.parse_args()

    summary(Test(args.instance, args.test))
import sys

from holdingsparser.application import run


def main():
    try:
        term = sys.argv[1]
    except IndexError:
        print("Enter a ticker symbol or CIK.")
        sys.exit(1)
    try:
        run(term)
    except RuntimeError as e:
        print(str(e))
        sys.exit(2)


if __name__ == "__main__":
    main()

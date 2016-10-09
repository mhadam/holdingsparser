import sys
import holdingsparser

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    if len(args) > 1:
    	print("Too many arguments, enter only a ticker or CIK.")
    	sys.exit()
	elif len(args) < 1:
    	print("Enter a ticker or CIK.")
    	sys.exit()

    search_results = search_edgar(args[0])
    if not search_results:
    	print("No matching Ticker Symbol or CIK found, enter a valid one.")

if __name__ == "__main__":
    main()
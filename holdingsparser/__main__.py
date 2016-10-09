import sys
import holdingsparser

def main(args=None):
    """The main routine."""
    print(sys.path)
    if args is None:
        args = sys.argv[1:]

    if len(args) > 1:
        print("Too many arguments, enter only a ticker or CIK.")
        sys.exit()
    elif len(args) < 1:
        print("Enter a ticker or CIK.")
        sys.exit()

    # get a URL to the search results, if any results are found
    search_url = holdingsparser.search_edgar(args[0])
    if not search_url:
        print("No matching Ticker Symbol or CIK found, enter a valid one.")
        sys.exit()

    # find the URL to the filings for the ticker or CIK
    filings_url = holdingsparser.get_filings_download_url(search_url, "13F-HR", "holdings")
    if not filings_url:
        print("No 13F-HR filings found.")
        sys.exit()
    else:
        print("Filings URL:")
        print(filings_url + "\n")

    # find the URL to the holdings document
    holdings_document_url = holdingsparser.get_holdings_document_url(filings_url)
    if not holdings_document_url:
        print("No holdings document found.")
        print("Investigate the filings URL.")
        sys.exit()
    else:
        print("Holdings document URL:")
        print(holdings_document_url + "\n")

    # parse the holdings document and convert into TSV data
    
    try:
        tsv_data = holdingsparser.parse_holdings_document(holdings_document_url, './holdingsparser/13F-HR.xsl')
    except:
        print("Encountered problem parsing holdings document.")

    # write the TSV file
    print(str(tsv_data))
    with open('output.tsv', 'w') as tsvfile:
        tsvfile.write(str(tsv_data))

if __name__ == "__main__":
    main()
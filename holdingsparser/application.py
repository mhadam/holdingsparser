from pathlib import Path

import lxml.etree as et
import requests
from bs4 import BeautifulSoup

from holdingsparser.scrape import get_cleaned_information_table, get_filings_url
from holdingsparser.sec import get_edgar_filing, get_holdings_document_url


def run(term: str):
    soup = get_edgar_filing(term)

    # find 13F-HR filings
    filings_url = get_filings_url(soup)

    # find holdings document url
    holdings_document_url = get_holdings_document_url(filings_url)

    # retrieve holdings document and transform to TSV
    holdings_document = requests.get(holdings_document_url)
    holdings_document_soup = BeautifulSoup(holdings_document.text, 'lxml')

    information_table = get_cleaned_information_table(holdings_document_soup)
    xsl_file_path = Path(__file__).parent.parent / "xslfiles/13F-HR.xsl"
    with open(xsl_file_path, 'r') as xsl_file:
        parsed_xsl = et.parse(xsl_file)
        xslt = et.XSLT(parsed_xsl)
    dom = et.fromstring(information_table)
    transformed_information_table = xslt(dom)

    # write TSV file
    with open(f'{term}_holdings.tsv', 'w') as tsvfile:
        tsvfile.write(str(transformed_information_table))
    print(str(transformed_information_table))

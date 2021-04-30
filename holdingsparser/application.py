import logging
from pathlib import Path

import lxml.etree as et
import requests
from bs4 import BeautifulSoup

from holdingsparser.scrape import get_cleaned_information_table, get_filings_url
from holdingsparser.sec import get_holdings_document_url


logger = logging.getLogger(__name__)


def search(term: str):
    # find 13F-HR filings
    filings_url = get_filings_url(term)
    logger.info(f"filings url is {filings_url}")

    # find holdings document url
    holdings_document_url = get_holdings_document_url(filings_url)
    logger.info(f"holdings document url is {holdings_document_url}")

    # retrieve holdings document and transform to TSV
    holdings_document = requests.get(holdings_document_url)
    holdings_document_soup = BeautifulSoup(holdings_document.text, "lxml")

    logger.debug(f"{holdings_document_soup=}")
    information_table = get_cleaned_information_table(holdings_document_soup)
    xsl_file_path = Path(__file__).parent.parent / "xslfiles/13F-HR.xsl"
    with open(xsl_file_path, "r") as xsl_file:
        parsed_xsl = et.parse(xsl_file)
        xslt = et.XSLT(parsed_xsl)
    dom = et.fromstring(information_table)
    transformed_information_table = xslt(dom)

    # write TSV file
    with open(f"{term}_holdings.tsv", "w") as tsvfile:
        tsvfile.write(str(transformed_information_table))
    print(str(transformed_information_table), end="")

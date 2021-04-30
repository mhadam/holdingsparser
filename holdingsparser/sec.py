import requests

from bs4 import BeautifulSoup

from holdingsparser.scrape import find_holdings_document_url


def get_holdings_document_url(filings_url: str) -> str:
    filings_page = requests.get(filings_url)
    filings_page_soup = BeautifulSoup(filings_page.text, "html.parser")
    holdings_document_url = find_holdings_document_url(filings_page_soup)
    return holdings_document_url

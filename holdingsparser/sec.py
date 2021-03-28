import requests
from bs4 import BeautifulSoup

from holdingsparser.scrape import is_results_missing, find_holdings_document_url


def get_search_url(term: str) -> str:
    hostname = 'http://www.sec.gov/cgi-bin/browse-edgar'
    query_params = f'?CIK={term}&Find=Search&owner=exclude&action=getcompany'
    return hostname + query_params


def get_edgar_filing(term: str) -> BeautifulSoup:
    # query for EDGAR filings
    search_url = get_search_url(term)
    results_page = requests.get(search_url)
    soup = BeautifulSoup(results_page.text, 'html.parser')
    if is_results_missing(soup):
        raise RuntimeError(f"EDGAR filings are not found for {term}")
    return soup


def get_holdings_document_url(filings_url: str) -> str:
    filings_page = requests.get(filings_url)
    filings_page_soup = BeautifulSoup(filings_page.text, 'html.parser')
    holdings_document_url = find_holdings_document_url(filings_page_soup)
    if not holdings_document_url:
        raise RuntimeError(f"no holdings document found")
    return holdings_document_url

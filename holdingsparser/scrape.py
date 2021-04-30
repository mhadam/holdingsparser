import json
import logging
import re
from itertools import chain
from json import JSONDecodeError
from typing import Iterable, Optional

import requests
from bs4 import BeautifulSoup, PageElement, Tag

logger = logging.getLogger(__name__)


def get_elements_from_soup(
    messages: Iterable[str], soup: BeautifulSoup
) -> Iterable[PageElement]:
    # check if any search results are found
    found_iterables = [soup.find_all(string=x) for x in set(messages)]
    return chain.from_iterable(found_iterables)


def is_results_missing(soup: BeautifulSoup) -> bool:
    messages = {"No matching Ticker Symbol.", "No matching CIK."}
    elements = get_elements_from_soup(messages, soup)
    return any(elements)


def get_filings_download_element(
    soup: BeautifulSoup, form, description
) -> Optional[Tag]:
    # find results table in page
    results_table = soup.find("table", attrs={"summary": "Results"})

    # find documents in search results
    def filter_search_results_entries(tag, form_type, description_text):
        """Returns true if the tag is a link in a row with text including form-type
        and description"""
        desc_re = re.compile(description_text, re.I)  # I: ignorecase
        form_re = re.compile(form_type, re.I)
        try:
            return (
                tag.parent.name == "td"
                and tag.name == "a"
                and tag["id"] == "documentsbutton"
                and tag.parent.parent.find(string=form_re)
                and tag.parent.parent.find(string=desc_re)
            )
        except (IndexError, KeyError):
            return False

    try:
        # result should be the <a> element containing holding documents link
        return results_table.find(
            lambda x: filter_search_results_entries(x, form, description)
        )
    except (TypeError, AttributeError):
        pass


def find_holdings_document_url(soup: BeautifulSoup) -> Optional[str]:
    # search entire soup for link to xml file
    any_information_table_xml_link = soup.find(
        "a", string=re.compile(r"^.+informationtable\.xml$")
    )
    try:
        return "https://www.sec.gov" + any_information_table_xml_link["href"]
    except (TypeError, KeyError):
        raise RuntimeError("failed to find holdings document URL")


def get_cleaned_information_table(soup: BeautifulSoup) -> str:
    # remove xmlns attribute
    information_table_re = re.compile("informationtable", re.I)
    soup.find(information_table_re).attrs = {}

    # remove namespace from all elements
    namespace_re = re.compile(r"^.+:.+$", re.I)
    tag_name_re = re.compile(r"^.+:(.+)$", re.I)

    for tag in soup.find_all(namespace_re):
        tag.name = tag_name_re.match(tag.name).group(1)

    information_table_soup = soup.find("informationtable")
    return information_table_soup.prettify()


def get_filings_url(cik: str) -> Optional[str]:
    submission_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    submissions_response = requests.get(submission_url)
    logger.debug(f"{submissions_response=}")
    try:
        payload = json.loads(submissions_response.text)
    except JSONDecodeError:
        return
    logger.debug(f"{payload=}")
    try:
        response_cik = payload["cik"]
        first_accession_number_formatted = payload["filings"]["recent"][
            "accessionNumber"
        ][0]
        accession_number = first_accession_number_formatted.replace("-", "")
        path = f"Archives/edgar/data/{response_cik}/{accession_number}/{first_accession_number_formatted}-index.htm"
        return f"https://www.sec.gov/{path}"
    except KeyError:
        pass

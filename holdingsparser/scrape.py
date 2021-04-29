import re
from itertools import chain
from typing import Iterable, Optional

from bs4 import BeautifulSoup, PageElement, Tag


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
    except AttributeError:
        pass


def find_holdings_document_url(soup: BeautifulSoup) -> Optional[str]:
    # given holding page,
    # select the appropriate holding document format
    def is_information_table_and_xml_entry(tag):
        """Returns true if the tag is a link in the same row as an xml file
        and the phrase 'information table'"""
        xml_re = re.compile(r"^.+\.xml$", re.I)
        info_re = re.compile("information table", re.I)
        try:
            return (
                tag.parent.parent.parent.name == "table"
                and tag.name == "a"
                and xml_re.match(tag.string)
                and tag.parent.parent.find(string=info_re)
            )
        except AttributeError:
            return False

    # search for specific element with xml file link
    information_table_xml_entry = soup.find(is_information_table_and_xml_entry)
    if information_table_xml_entry:
        return "http://www.sec.gov" + information_table_xml_entry.get("href")

    # search entire soup for link to xml file
    any_information_table_xml_link = soup.find(
        "a", string=re.compile(r".+informationtable\.xml$")
    )
    try:
        return any_information_table_xml_link["href"]
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


def get_filings_url(soup: BeautifulSoup) -> str:
    download_element = get_filings_download_element(soup, "13F-HR", "holdings")
    try:
        return "http://www.sec.gov" + download_element["href"]
    except (TypeError, KeyError):
        raise RuntimeError(f"no filings found")

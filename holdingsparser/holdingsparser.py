import sys, re, urllib.request, csv, io
import lxml.etree as et
from bs4 import BeautifulSoup

def search_edgar(query):
    # url to make search query
    search_url = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK=' + query + '&Find=Search&owner=exclude&action=getcompany'

    # download search results for the CIK/ticker requested
    with urllib.request.urlopen(search_url) as response:
        results_page = response.read()

    soup = BeautifulSoup(results_page, 'html.parser')

    # check if any search results are found
    if (any(soup.find_all(string='No matching Ticker Symbol.')) or
        any(soup.find_all(string='No matching CIK.'))):
        return None
    else:
        return search_url

def get_filings_download_url(search_url, form, description):
    # download search results
    with urllib.request.urlopen(search_url) as response:
        results_page = response.read()

    # parse results and search for holdings files
    soup = BeautifulSoup(results_page, 'html.parser')
    # find results table in page
    results_table = soup.find('table', attrs={'summary' : 'Results'})

    # find documents in search results
    def filter_search_results_entries(tag, form_type, description_text):
        """Returns true if the tag is a link in a row with text including form-type
        and description"""
        desc_re = re.compile(description_text, re.I)
        form_re = re.compile(form_type, re.I)
        try:
            return (tag.parent.name == 'td' and
                tag.name == 'a' and
                tag['id'] == 'documentsbutton' and
                tag.parent.parent.find(string=form_re) and
                tag.parent.parent.find(string=desc_re))
        except:
            return False

    # result should be the <a> element containing holding documents link
    result = results_table.find(lambda x: filter_search_results_entries(x, form, description))

    if not result:
        return None
    else:
        return 'http://www.sec.gov' + result.get('href')

def get_holdings_document_url(filings_url):
    # download holdings documents page
    with urllib.request.urlopen(filings_url) as response:
        filings_page = response.read()

    soup = BeautifulSoup(filings_page, 'html.parser')

    # select the appropriate holding document format
    def is_information_table_and_xml_entry(tag):
        """Returns true if the tag is a link in the same row as an xml file
        and the phrase 'information table'"""
        xml_re = re.compile('^.+\.xml$', re.I)
        info_re = re.compile('information table', re.I)
        try:
            return (tag.parent.parent.parent.name == 'table' and
                tag.name == 'a' and
                xml_re.match(tag.string) and
                tag.parent.parent.find(string=info_re))
        except:
            return False

    if soup.find(is_information_table_and_xml_entry):
        info_table_path = soup.find(is_information_table_and_xml_entry).get('href')
        info_table_url = 'http://www.sec.gov' + info_table_path
    elif soup.find('a', string=re.compile(".+informationtable.xml$")):
        info_table_url = 'http://www.sec.gov' + soup.find('a', string=re.compile(".+informationtable\.xml$", re.I)).get('href')
    else:
        return None

    return info_table_url

def parse_holdings_document(holdings_document_url, xsl_file_location):
    # download the information table
    with urllib.request.urlopen(holdings_document_url) as response:
        info_table = response.read()

    # parse the information table
    soup = BeautifulSoup(info_table, 'lxml')

    # remove xmlns attribute
    informationtable_re = re.compile('informationtable', re.I)
    soup.find(informationtable_re).attrs = {}

    # remove namespace from all elements
    namespace_re = re.compile('^.+\:.+$', re.I)
    tag_name_re = re.compile('^.+\:(.+)$', re.I)

    for tag in soup.find_all(namespace_re):
        tag.name = tag_name_re.match(tag.name).group(1)

    soup = soup.find('informationtable')

    with open(xsl_file_location, 'r') as xsl_file:
        xslt = et.parse(xsl_file)

    dom = et.parse(io.StringIO(soup.prettify()))
    transform = et.XSLT(xslt)
    transformed_output = transform(dom)

    return transformed_output
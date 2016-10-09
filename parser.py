#!/usr/bin/env python

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

    # check if no results where found, and exit program if so
    if (any(soup.find_all(string='No matching Ticker Symbol.')) or
        any(soup.find_all(string='No matching CIK.'))):
        return None
    else:
        return results_page       

def find_form_download_url(results, form):
    # parse results and search for holdings files
    reports_table = soup.find('table', attrs={'summary' : 'Results'})

    # find holdings document in search results
    def filter_search_result_entries(tag, form_type, description):
        """Returns true if the tag is a link in a row with text including form-type
        and description"""
        desc_re = re.compile(description, re.I)
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
    result = reports_table.find(lambda x: filter_search_result_entries(x, '13F-HR', 'holding'))

    if result:
        pass
    else:
        print("No holdings reports found.")
        sys.exit()

    documents_url = 'http://www.sec.gov' + result.get('href')

print("Documents URL:")
print(documents_url + "\n")

# download holding documents page
with urllib.request.urlopen(documents_url) as response:
    documents_page = response.read()

soup = BeautifulSoup(documents_page, 'html.parser')

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
    print("Cannot find appropriate holding document.")
    print("Investigate here:\n" + documents_url)
    sys.exit()

print("Information Table URL:\n" + info_table_url)

# download the information table
with urllib.request.urlopen(info_table_url) as response:
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

# write the information table for debugging
with open("./downloaded.xml", 'w') as output:
    output.write(soup.prettify())
soup = soup.find('informationtable')

with open("./13F-HR.xsl", 'r') as xsl_file:
    xslt = et.parse(xsl_file)

dom = et.parse(io.StringIO(soup.prettify()))
transform = et.XSLT(xslt)
new_dom = transform(dom)

with open('output.tsv', 'w') as tsvfile:
    tsvfile.write(str(new_dom))
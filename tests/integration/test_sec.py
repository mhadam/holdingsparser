from holdingsparser.sec import get_holdings_document_url


def test_get_holdings_document_url():
    documents_url = "https://www.sec.gov/Archives/edgar/data/1166559/000110465921021959/0001104659-21-021959-index.htm"

    result = get_holdings_document_url(documents_url)

    expected = "https://www.sec.gov/Archives/edgar/data/1166559/000110465921021959/a21-6498_1informationtable.xml"
    assert result == expected

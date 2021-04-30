from holdingsparser.scrape import get_filings_url


def test_get_filings_url_missing():
    result = get_filings_url("missing")
    assert result is None

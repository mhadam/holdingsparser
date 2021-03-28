import pytest

from holdingsparser.sec import get_edgar_filing


def test_symbol_search_missing():
    with pytest.raises(Exception):
        get_edgar_filing("not present")


def test_symbol_search_exists():
    get_edgar_filing("0001166559")

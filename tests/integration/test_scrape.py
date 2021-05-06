from pathlib import Path

import requests
import requests_random_user_agent
import untangle

from holdingsparser.application import get_row_mapping
from holdingsparser.file import Holding, ShrsOrPrnAmt, VotingAuthority
from holdingsparser.scrape import get_filings_url, get_holdings


def test_get_filings_url():
    result = get_filings_url("0001166559")
    assert (
        result
        == "https://www.sec.gov/Archives/edgar/data/1166559/000110465921021959/0001104659-21-021959-index.htm"
    )


def test_get_filings_url_missing():
    result = get_filings_url("missing")
    assert result is None


def test_parse_xml():
    with open(Path(__file__).parent / "sample_response.xml") as f:
        o = untangle.parse(f)
        assert len(o.informationTable.children) == 21


def test_get_holdings():
    path = (
        "Archives/edgar/data/1166559/000110465921021959/a21-6498_1informationtable.xml"
    )
    holdings_document_url = f"https://www.sec.gov/{path}"
    holdings_document = requests.get(holdings_document_url)

    result = get_holdings(holdings_document.text)

    information_table = list(result)
    assert len(information_table) == 21
    assert information_table[0] == Holding(
        name_of_issuer="ALPHABET INC",
        title_of_class="CAP STK CL A",
        cusip="02079K305",
        value=37776,
        shrs_or_prn_amt=ShrsOrPrnAmt(amt=21554, amt_type="SH"),
        investment_discretion="SOLE",
        voting_authority=VotingAuthority(sole=21554, shared=0, none=0),
    )


def test_get_line():
    holding = Holding(
        name_of_issuer="ALPHABET INC",
        title_of_class="CAP STK CL A",
        cusip="02079K305",
        value=37776,
        shrs_or_prn_amt=ShrsOrPrnAmt(amt=21554, amt_type="SH"),
        investment_discretion="SOLE",
        voting_authority=VotingAuthority(sole=21554, shared=0, none=0),
    )

    result = get_row_mapping(holding)

    assert result == {
        "Cusip": "02079K305",
        "InvestmentDiscretion": "SOLE",
        "Name": "ALPHABET INC",
        "SshPrnAmt": 21554,
        "SshPrnType": "SH",
        "TitleOfClass": "CAP STK CL A",
        "Value": 37776,
        "VotingAuthorityNone": 0,
        "VotingAuthorityShared": 0,
        "VotingAuthoritySole": 21554,
    }

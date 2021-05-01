import csv
import dataclasses
import logging
import shutil
from io import StringIO
from typing import Mapping

import requests

from holdingsparser.file import Holding
from holdingsparser.scrape import get_holdings, get_filings_url
from holdingsparser.sec import get_holdings_document_url

logger = logging.getLogger(__name__)


def replace_keys(original: Mapping, replacements: Mapping) -> Mapping:
    result = dict(original)
    for old_key, new_key in replacements.items():
        if old_key in result:
            result[new_key] = result.pop(old_key)
    return result


def camelcase(value: str) -> str:
    return "".join(x for x in value.title() if x.isalpha())


def get_tsv_line(holding: Holding) -> Mapping:
    result = {}
    for k, v in dataclasses.asdict(holding).items():
        if isinstance(v, dict):
            for inner_k, inner_v in v.items():
                result[inner_k] = inner_v
        else:
            result[k] = v
    if result.get("put_call") is None:
        result.pop("put_call")
    replaced = replace_keys(
        result,
        {
            "shared": "voting_authority_shared",
            "sole": "voting_authority_sole",
            "none": "voting_authority_none",
            "amt": "ssh_prn_amt",
            "amt_type": "ssh_prn_type",
            "name_of_issuer": "name",
        },
    )
    return {camelcase(k): v for (k, v) in replaced.items()}


def search(term: str):
    # find 13F-HR filings
    filings_url = get_filings_url(term)
    logger.info(f"filings url is {filings_url}")

    if filings_url is None:
        raise RuntimeError("failed to get filings URL")

    # find holdings document url
    holdings_document_url = get_holdings_document_url(filings_url)
    logger.info(f"holdings document url is {holdings_document_url}")

    # retrieve holdings document and transform to TSV
    holdings_document = requests.get(holdings_document_url)
    holdings = get_holdings(holdings_document.text)
    holdings_list = list(holdings)

    # write TSV file
    result = StringIO()
    first_line = get_tsv_line(holdings_list[0])
    arbitrary_order = [
        "Name",
        "TitleOfClass",
        "Cusip",
        "Value",
        "SshPrnAmt",
        "SshPrnType",
        "InvestmentDiscretion",
        "VotingAuthoritySole",
        "VotingAuthorityShared",
        "VotingAuthorityNone",
    ]
    order = dict((key, idx) for idx, key in enumerate(arbitrary_order))
    column_names = sorted(first_line, key=order.get)
    w = csv.DictWriter(result, column_names, delimiter="\t")
    w.writeheader()
    for holding in holdings_list:
        line = get_tsv_line(holding)
        w.writerow(line)
    print(result.getvalue(), end="")

    with open(f"{term}_holdings.tsv", "w") as tsvfile:
        result.seek(0)
        shutil.copyfileobj(result, tsvfile)

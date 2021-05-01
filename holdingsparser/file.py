from dataclasses import dataclass
from enum import Enum, unique, auto
from typing import Optional


@dataclass
class ShrsOrPrnAmt:
    amt: int
    amt_type: str


@dataclass
class VotingAuthority:
    sole: int
    shared: int
    none: int


@unique
class OptionType(Enum):
    PUT = auto()
    Call = auto()


@dataclass
class Holding:
    name_of_issuer: str
    title_of_class: str
    cusip: str
    value: int
    shrs_or_prn_amt: ShrsOrPrnAmt
    investment_discretion: str
    voting_authority: VotingAuthority
    put_call: Optional[OptionType] = None

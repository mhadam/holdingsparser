# Holdings Parser

Parses 13F reports filed with the SEC regarding mutual fund holdings. The report detailing holders, stakes, etc. is parsed into TSV data, output to the command line and saved in the execution directory.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisities

The code was developed with Python 3.5.2 on Ubuntu 16.04. There's a requirements.txt file that contains all the libraries and versions needed to run the code.

### Run Instructions

First install the libraries from the requirements.txt file (otherwise install the libraries on your own):
```
pip install -r quovo-challenge/requirements.txt
```

The project can then be run with:
```
python -m holdingsparser (CIK or ticker symbol)
```

Example commands:
```
python -m holdingsparser 0001166559
```
Output:
```
Filings URL:
http://www.sec.gov/Archives/edgar/data/1166559/000110465916139781/0001104659-16-139781-index.htm

Holdings document URL:
http://www.sec.gov/Archives/edgar/data/1166559/000110465916139781/a16-16809_1informationtable.xml

Name	TitleofClass	Cusip	Value	ShrsOrPrnAmt	SshPrnAmt	SshPrnType	InvestmentDiscretion	VotingAuthoritySole	VotingAuthorityShared	VotingAuthorityNone
ARCOS DORADOS HOLDINGS INC	SHS CLASS -A -	G0457F107	14599	3060500SH	SOLE	3060500	0	0
AUTONATION INC	COM	05329W102	89202	1898717	SH	SOLE	189871700
BERKSHIRE HATHAWAY INC DEL	CL B NEW	084670702	9321804	64381548SH	SOLE	64381548	0	0
CANADIAN NATL RY CO	COM	136375102	1011513	17126874	SH	SOLE	17126874	0	0
CATERPILLAR INC DEL	COM	149123101	853686	11260857	SH	SOLE	11260857	0	0
COCA COLA FEMSA SAB DE CV	SPON ADR REP L	191241108	515573	6214719SH	SOLE	6214719	0	0
CROWN CASTLE INTL CORP NEW	COM	22822V101	540916	5332900	SH	SOLE	5332900	0	0
ECOLAB INC	COM	278865100	517858	4366426	SH	SOLE	436642600
FEDEX CORP	COM	31428X106	459134	3024999	SH	SOLE	302499900
GRUPO TELEVISA SA	SPON ADR REP ORD	40049J206	439532	16879104SH	SOLE	16879104	0	0
LIBERTY GLOBAL PLC	SHS CL A	G5480U104	61593	2119515	SH	SOLE	2119515	0	0
LIBERTY GLOBAL PLC	SHS CL C	G5480U120	104267	3639349	SH	SOLE	3639349	0	0
LIBERTY GLOBAL PLC	LILAC SHS CL A	G5480U138	11950	370424	SH	SOLE	370424	0	0
LIBERTY GLOBAL PLC	LILAC SHS CL C	G5480U153	20665	636044	SH	SOLE	636044	0	0
UNITED PARCEL SERVICE INC	CL B	911312106	487468	4525329	SH	SOLE	4525329	0	0
WALGREENS BOOTS ALLIANCE INC	COM	931427108	289396	3475398	SH	SOLE	3475398	0	0
WAL-MART STORES INC	COM	931142103	847251	11603000	SH	SOLE	11603000	0	0
WASTE MGMT INC DEL	COM	94106L109	1234853	18633672	SH	SOLE	18633672	0	0
```
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

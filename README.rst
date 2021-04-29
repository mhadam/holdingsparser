holdingsparser
--------------

.. image:: https://img.shields.io/pypi/v/holdingsparser.svg
    :target: https://pypi.org/project/holdingsparser
    :alt: PyPI badge

.. image:: https://img.shields.io/pypi/pyversions/holdingsparser.svg
    :target: https://pypi.org/project/holdingsparser
    :alt: PyPI versions badge

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Black formatter badge

.. image:: https://img.shields.io/pypi/l/transmission-clutch.svg
    :target: https://en.wikipedia.org/wiki/MIT_License
    :alt: License badge

.. image:: https://img.shields.io/pypi/dm/holdingsparser.svg
    :target: https://pypistats.org/packages/holdingsparser
    :alt: PyPI downloads badge

Background
==========
From `investor.gov`_ (educational website from the SEC):

    An institutional investment manager that uses the U.S. mail (or other means or instrumentality of interstate commerce) in the course of its business, and exercises investment discretion over $100 million or more in Section 13(f) securities (explained below) must report its holdings quarterly on Form 13F with the Securities and Exchange Commission (SEC).

``holdingsparser`` fetches 13-F filings from `EDGAR`_ and outputs the holding entries in a TSV file.

Quick start
===========

Install the package:

.. code-block:: console

    pip install --user holdingsparser

Upgrade the package:

.. code-block:: console

    pip install --user --pre -U holdingsparser

Search for a filing with the CIK:

.. code-block:: console

    holdingsparser 0001166559

Alternatively:

.. code-block:: console

    python -m holdingsparser 0001166559

.. _investor.gov: https://www.investor.gov/introduction-investing/investing-basics/glossary/form-13f-reports-filed-institutional-investment
.. _EDGAR: https://www.sec.gov/edgar/searchedgar/companysearch.html

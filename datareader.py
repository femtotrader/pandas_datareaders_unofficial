#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implements some DataReader like
classical Python Pandas DataReader
but with requests
(so it's easy to have cache)
moreover it's easy to implement your own DataReaderBase
on top of this.

http://pandas.pydata.org/pandas-docs/stable/remote_data.html
https://github.com/pydata/pandas/blob/master/pandas/io/data.py
"""

import pandas as pd

import logging
import traceback

from StringIO import StringIO

from datareaders.base import DataReaderBase

from datareaders.google_finance_daily import DataReaderGoogleFinanceDaily
from datareaders.google_finance_intraday import DataReaderGoogleFinanceIntraday
from datareaders.google_finance_options import DataReaderGoogleFinanceOptions
from datareaders.yahoo_finance_daily import DataReaderYahooFinanceDaily
from datareaders.yahoo_finance_quotes import DataReaderYahooFinanceQuotes
from datareaders.yahoo_finance_options import DataReaderYahooFinanceOptions
from datareaders.fred import DataReaderFRED
from datareaders.fama_french import DataReaderFamaFrench
from datareaders.world_bank import DataReaderWorldBank


class DataReaderFactory(object):
    def __init__(self):
        self._d_factory = {}

        # === Google Finance ===
        self.add('google', DataReaderGoogleFinanceDaily)
        self.add('GoogleFinanceDaily', DataReaderGoogleFinanceDaily)

        self.add('GoogleFinanceIntraday', DataReaderGoogleFinanceIntraday)

        self.add('GoogleFinanceOptions', DataReaderGoogleFinanceOptions)

        # === Yahoo Finance ===
        self.add('yahoo', DataReaderYahooFinanceDaily)
        self.add('YahooFinanceDaily', DataReaderYahooFinanceDaily)

        self.add('YahooFinanceQuotes', DataReaderYahooFinanceQuotes)

        self.add('YahooFinanceOptions', DataReaderYahooFinanceOptions)

        # === FRED ===
        self.add('fred', DataReaderFRED)

        # === FamaFrench ===
        self.add('ff', DataReaderFamaFrench)
        self.add('FamaFrench', DataReaderFamaFrench)

        # === WorldBank ===
        self.add('wb', DataReaderWorldBank)
        self.add('WorldBank', DataReaderWorldBank)

    def add(self, name, cls):
        self._d_factory[name.lower()] = cls

    def factory(self, name, *args, **kwargs):
        try:
            return(self._d_factory[name.lower()](*args, **kwargs))
        except:
            logging.error(traceback.format_exc())
            raise(NotImplementedError("DataReader '%s' not implemented" % name))

#DATA_READER_FACTORY = DataReaderFactory()

#def MyDataReader(name):
#    return(DATA_READER_FACTORY.factory(name))

def MyDataReader(name, *args, **kwargs):
    """
    Imports data from a number of online sources.

    Currently supports 
        * [Google Finance](https://www.google.com/finance) (daily, intraday, options)
        * [Yahoo Finance](https://finance.yahoo.com) (daily, quotes, options)
        * [Federal Reserve Economic Data - FRED - St. Louis Fed](http://research.stlouisfed.org/fred2/)
        * [Fama-French](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
        * [World Bank](http://data.worldbank.org/)

    Parameters
    ----------
    name : str or list of strs
        the name of the dataset. Some data sources (yahoo, google, fred) will
        accept a list of names.
    data_source: str
        the data source ("yahoo", "google", "fred", or "ff")
    start : {datetime, None}
        left boundary for range (defaults to 1/1/2010)
    end : {datetime, None}
        right boundary for range (defaults to today)

    start, end = _sanitize_dates(start, end)

    """
    return(DataReaderFactory().factory(name, *args, **kwargs))

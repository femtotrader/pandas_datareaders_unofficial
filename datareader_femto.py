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


ToDo:
get OHLCV Google Finance Intraday with start_date, end_date, period
-> chunksize ?

"""

import pandas as pd

import logging
import traceback

from StringIO import StringIO

from datareaders.base import DataReaderBase

from datareaders.google_finance import DataReaderGoogleFinanceDaily, DataReaderGoogleFinanceIntraday
from datareaders.yahoo_finance import DataReaderYahooFinanceDaily, DataReaderYahooFinanceOptions
from datareaders.fred import DataReaderFRED
from datareaders.fama_french import DataReaderFamaFrench
from datareaders.world_bank import DataReaderWorldBank

"""
def DataReader_femto(name, data_source=None, start=None, end=None,
               retry_count=3, pause=0.001):

    # see Pandas DataReader
    # see get_pricing sur Quantopian Research

    # frequency?

    Imports data from a number of online sources.

    Currently supports 


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

    raise(NotImplementedError)
"""



class DataReaderFactory(object):
    def __init__(self):
        self._d_factory = {}

        self.add('google', DataReaderGoogleFinanceDaily)
        self.add('GoogleFinanceDaily', DataReaderGoogleFinanceDaily)

        self.add('GoogleFinanceIntraday', DataReaderGoogleFinanceIntraday)

        self.add('yahoo', DataReaderYahooFinanceDaily)
        self.add('YahooFinanceDaily', DataReaderYahooFinanceDaily)

        self.add('YahooFinanceOptions', DataReaderYahooFinanceOptions)

        self.add('fred', DataReaderFRED)

        self.add('ff', DataReaderFamaFrench)
        self.add('FamaFrench', DataReaderFamaFrench)

        self.add('wb', DataReaderWorldBank)
        self.add('WorldBank', DataReaderWorldBank)

    def add(self, name, cls):
        self._d_factory[name.lower()] = cls

    def factory(self, name):
        try:
            return(self._d_factory[name.lower()]())
        except:
            logging.error(traceback.format_exc())
            raise(NotImplementedError("DataReader '%s' not implemented" % name))

#DATA_READER_FACTORY = DataReaderFactory()

#def MyDataReader(name):
#    return(DATA_READER_FACTORY.factory(name))

def MyDataReader(name):
    return(DataReaderFactory().factory(name))



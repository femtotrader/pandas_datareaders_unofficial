#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    pandas_datareaders.datareader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements some DataReaders like
    classical Python Pandas DataReader
    but with requests
    (so it's easy to have cache)
    moreover it's easy to implement your own DataReaderBase
    on top of this.

    http://pandas.pydata.org/pandas-docs/stable/remote_data.html
    https://github.com/pydata/pandas/blob/master/pandas/io/data.py

    This file contains factory class and method to build DataReader

"""

import pandas as pd

import logging
import traceback

from six.moves import cStringIO as StringIO

from pandas_datareaders_unofficial.datareaders.base import DataReaderBase

from pandas_datareaders_unofficial.datareaders.google_finance_daily import DataReaderGoogleFinanceDaily
from pandas_datareaders_unofficial.datareaders.google_finance_intraday import DataReaderGoogleFinanceIntraday
from pandas_datareaders_unofficial.datareaders.google_finance_options import DataReaderGoogleFinanceOptions

from pandas_datareaders_unofficial.datareaders.yahoo_finance_daily import DataReaderYahooFinanceDaily
from pandas_datareaders_unofficial.datareaders.yahoo_finance_quotes import DataReaderYahooFinanceQuotes
from pandas_datareaders_unofficial.datareaders.yahoo_finance_options import DataReaderYahooFinanceOptions
from pandas_datareaders_unofficial.datareaders.yahoo_finance_intraday import DataReaderYahooFinanceIntraday

from pandas_datareaders_unofficial.datareaders.fred import DataReaderFRED

from pandas_datareaders_unofficial.datareaders.fama_french import DataReaderFamaFrench

from pandas_datareaders_unofficial.datareaders.world_bank import DataReaderWorldBank

from pandas_datareaders_unofficial.datareaders.openexchangerates import DataReaderOpenExchangeRates

from pandas_datareaders_unofficial.tools import RemoteDataError

class DataReaderFactory(object):
    """
    DataReaderFactory

    Factory of DataReader

    Only ONE factory need to be defined : DATA_READER_FACTORY

    Additional DataReader can be add using:

    DATA_READER_FACTORY.add('datareadername', DataReaderClassName)
    """
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

        self.add('YahooFinanceIntraday', DataReaderYahooFinanceIntraday)

        # === FRED ===
        self.add('fred', DataReaderFRED)

        # === FamaFrench ===
        self.add('ff', DataReaderFamaFrench)
        self.add('FamaFrench', DataReaderFamaFrench)

        # === WorldBank ===
        self.add('wb', DataReaderWorldBank)
        self.add('WorldBank', DataReaderWorldBank)

        # === OpenExchangeRates ===
        self.add('OpenExchangeRates', DataReaderOpenExchangeRates)

    def add(self, name, cls):
        self._d_factory[name.lower()] = cls

    def factory(self, name, *args, **kwargs):
        try:
            return(self._d_factory[name.lower()](*args, **kwargs))
        except:
            logging.error(traceback.format_exc())
            raise(NotImplementedError("DataReader '%s' not implemented - should be in %s" % (name, self._d_factory.keys())))

DATA_READER_FACTORY = DataReaderFactory()

def DataReader(name, *args, **kwargs):
    """
    Creates a DataReader to fetch data from a number of online sources.

    Currently supports 
        * [Google Finance](https://www.google.com/finance) (daily, intraday, options)
        * [Yahoo Finance](https://finance.yahoo.com) (daily, quotes, options)
        * [Federal Reserve Economic Data - FRED - St. Louis Fed](http://research.stlouisfed.org/fred2/)
        * [Fama-French](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
        * [World Bank](http://data.worldbank.org/)

    Parameters
    ----------

    :param name: data source
    :type name: str

        * "YahooFinanceDaily" (can also be simply "yahoo"),
        * "YahooFinanceQuotes"
        * "YahooFinanceOptions"
        * "GoogleFinanceDaily" (can also be simply "google"),
        * "GoogleFinanceIntraday",
        * "GoogleFinanceOptions",
        * "fred",
        * "FamaFrench" (or "ff")
        * "WorldBank" (or "wb")

    :param *args: positional arguments (can depends of datasource)
    :param **kwargs: keywords arguments (can depends of datasource)

    :param cache_name: for ``sqlite`` backend: cache file will start with this prefix,
                       e.g ``cache.sqlite``
                       for ``mongodb``: it's used as database name
                       
                       for ``redis``: it's used as the namespace. This means all keys
                       are prefixed with ``'cache_name:'``
    :param backend: cache backend name e.g ``'sqlite'``, ``'mongodb'``, ``'redis'``, ``'memory'``.
                    (see :ref:`persistence`). Or instance of backend implementation.
                    Default value is ``None``, which means use ``'sqlite'`` if available,
                    otherwise fallback to ``'memory'``.
    :param expire_after: number of seconds after cache will be expired
                         or `None` (default) to ignore expiration
    :type expire_after: float

    (see also `requests-cache` doc)

    """
    return(DATA_READER_FACTORY.factory(name, *args, **kwargs))

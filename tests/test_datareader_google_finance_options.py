#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run unit tests using
nosetests -s -v
"""

import time
import datetime

from datareader_femto import *

from pandas.io.data import Options

import requests_cache
expire_after = 60*5 # seconds

def test_google_finance_options():

    filename = "google_finance_options"

    if expire_after>=0:
        requests_cache.install_cache(filename, backend='sqlite', expire_after=expire_after) # expiration seconds
        logging.info("Installing cache '%s.sqlite' with expire_after=%d (seconds)" % (filename, expire_after))
    if expire_after==0:
        logging.warning("expire_after==0 no cache expiration!")

    symbol = 'NASDAQ:AAPL'
    #symbol = 'NASDAQ:GOOG'
    #symbol = ['NASDAQ:AAPL', 'NASDAQ:GOOG'] # ToFix: get returns now a dict not a DataFrame

    option = MyDataReader("GoogleFinanceOptions").get(symbol)
    print(option)
    #print(option['options'].dtypes)
    #option = option.rename(items={
    #    'NASDAQ:AAPL': 'NASDAQ_AAPL',
    #    'NASDAQ:GOOG': 'NASDAQ_GOOG'
    #})
    option['options'].to_excel("google_options.xls")
    #data = option.get_all_data() # get all data
    #print(data)
    #data = option.get_call_data(expiry=expiry) # get call data


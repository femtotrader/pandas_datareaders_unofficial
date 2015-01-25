#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run unit tests using
nosetests -s -v
"""

import time
import datetime
from datetime import timedelta

import pandas as pd
from pandas_datareaders_unofficial import DataReader

from pandas.io.data import Options

expire_after = timedelta(hours=1) # 0:no cache - None:no cache expiration

def test_google_finance_options():

    #symbol = 'NASDAQ:AAPL'
    symbol = 'NASDAQ:GOOG'
    option = DataReader("GoogleFinanceOptions", expire_after=expire_after).get(symbol)
    print(option)
    assert(isinstance(option, dict))

    symbol = ['NASDAQ:AAPL', 'NASDAQ:GOOG'] # ToFix: get returns now a dict not a DataFrame
    option = DataReader("GoogleFinanceOptions", expire_after=expire_after).get(symbol)
    print(option)
    assert(isinstance(option, dict))


    #print(option['options'].dtypes)
    #option = option.rename(items={
    #    'NASDAQ:AAPL': 'NASDAQ_AAPL',
    #    'NASDAQ:GOOG': 'NASDAQ_GOOG'
    #})
    #option['options'].to_excel("google_options.xls")
    #data = option.get_all_data() # get all data
    #print(data)
    #data = option.get_call_data(expiry=expiry) # get call data

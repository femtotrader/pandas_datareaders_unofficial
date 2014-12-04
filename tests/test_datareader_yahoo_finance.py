#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run unit tests using
nosetests -s -v
"""

import time
import datetime

from datareader_femto import *

import pandas.io.data as web

import requests_cache
expire_after = 60*5 # seconds

def test_yahoo_finance_daily():

    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2013, 1, 27)

    symbol = "F"
    symbol = "AAPL"
    #symbol = ["AAPL", 'F']

    data = MyDataReader("YahooFinanceDaily").get(symbol, start, end)
    print(data)
    print(type(data))
    print(data.dtypes)

    f = web.DataReader(symbol, 'yahoo', start, end)
    print(f)
    print(type(f))
    print(f.ix['2010-01-04'])
    print(f.dtypes)

    diff = f-data
    
    assert(diff.sum().sum()==0)


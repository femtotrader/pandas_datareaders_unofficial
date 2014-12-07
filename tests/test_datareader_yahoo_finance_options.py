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

def test_yahoo_finance_options():
    symbol = 'aapl'
    #symbol = ["AAPL", 'F']

    #data = MyDataReader("YahooFinanceDaily").get(symbol, start, end)
    #print(data)
    #print(type(data))
    #print(data.dtypes)

    aapl = Options(symbol, 'yahoo')
    data = aapl.get_all_data()

    print(data.iloc[0:5, 0:5])

    print(data.loc[(100, slice(None), 'put'),'Vol'].head())

    expiry = datetime.date(2016, 1, 1)
    data = aapl.get_call_data(expiry=expiry)

    print(data)

    print(aapl.expiry_dates)

    data = aapl.get_call_data(expiry=aapl.expiry_dates[0])
    print(data.iloc[0:5:, 0:5])

    data = aapl.get_near_stock_price(expiry=aapl.expiry_dates[0:3])
    print(data.iloc[0:5:, 0:5])

    #diff = f-data
    
    #assert(diff.sum().sum()==0)


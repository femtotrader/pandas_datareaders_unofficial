#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run unit tests using
nosetests -s -v
"""

import time
import datetime

from datareader import *

import pandas.io.data as web

expire_after = 60*60 # seconds - 0:no cache - None:no cache expiration

def test_yahoo_finance_quotes():

    symbol = "F"
    #symbol = "AAPL"
    #symbol = ["AAPL", 'F']

    print("="*5 + "New DataReader" + "="*5)
    data = MyDataReader("YahooFinanceQuotes", expire_after=expire_after).get(symbol)
    print(data)
    #print(type(data))
    #print(data.dtypes)

    #print("="*5 + "Pandas original DataReader" + "="*5)
    #f = web.get_quote_yahoo(symbol)
    #print(f)
    #print(type(f))
    #print(f.dtypes)

    #diff = f-data
    
    #assert(diff.sum().sum()==0)

    print("="*5 + "New DataReader with multi symbols" + "="*5)
    symbol = ["AAPL", 'F']
    data = MyDataReader("YahooFinanceQuotes", expire_after=expire_after).get(symbol)
    print(data)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run unit tests using
nosetests -s -v
"""

import time
import datetime

from datareader import *

from pandas.io.data import Options

import requests_cache
expire_after = 60*60 # seconds - 0:no cache - None:no cache expiration

def test_yahoo_finance_options():

    #filename = "yahoo_finance_options"
    #if expire_after>=0:
    #    requests_cache.install_cache(filename, backend='sqlite', expire_after=expire_after) # expiration seconds
    #    logging.info("Installing cache '%s.sqlite' with expire_after=%d (seconds)" % (filename, expire_after))
    #if expire_after==0:
    #    logging.warning("expire_after==0 no cache expiration!")
    
    symbol = 'AAPL'
    #symbol = 'F'
    #symbol = '^spxpm'
    #symbol = ["AAPL", 'F']
    
    option = MyDataReader("YahooFinanceOptions", expire_after=expire_after).get(symbol)
    data = option.get_all_data() # get all data
    print(data)
    #data = option.get_call_data(expiry=expiry) # get call data

    """
    aapl = Options(symbol, 'yahoo')
    data = aapl.get_all_data()
    print(data.iloc[0:5, 0:5])
    """

    """
    print(data.loc[(100, slice(None), 'put'),'Vol'].head())

    expiry = datetime.date(2016, 1, 1)
    data = aapl.get_call_data(expiry=expiry)

    print(data)

    print(aapl.expiry_dates)

    data = aapl.get_call_data(expiry=aapl.expiry_dates[0])
    print(data.iloc[0:5:, 0:5])

    data = aapl.get_near_stock_price(expiry=aapl.expiry_dates[0:3])
    print(data.iloc[0:5:, 0:5])
    """

    #diff = f-data
    
    #assert(diff.sum().sum()==0)


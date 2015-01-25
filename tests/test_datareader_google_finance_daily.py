#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run unit tests using
nosetests -s -v
"""

import time
import datetime
from datetime import timedelta

from pandas_datareaders_unofficial import DataReader
from pandas_datareaders_unofficial.tools import to_float, to_int

import pandas.io.data as web

expire_after = timedelta(hours=1) # 0:no cache - None:no cache expiration

import logging
#import logging.config
#import os

def test_google_finance_daily():

    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2013, 1, 27)

    symbol = "F"
    #symbol = "GOOG"

    print("="*5 + "New DataReader" + "="*5)

    dr_gfd = DataReader("GoogleFinanceDaily", expire_after=expire_after)
    data = dr_gfd.get(symbol, start, end)
    print(data)
    print(type(data))
    print(data.dtypes)

    print("="*5 + "Pandas original DataReader" + "="*5)

    f = web.DataReader(symbol, 'google', start, end)
    print(f)
    print(type(f))
    print(f.ix['2010-01-04'])
    print(f.dtypes)

    for col in ['Open', 'High', 'Low', 'Close']:
        f[col] = f[col].map(to_float)

    f['Volume'] = f['Volume'].map(to_int)
    print(f.dtypes)

    diff = f - data

    print(diff)
    assert(diff.sum().sum()==0)

    print("="*5 + "New DataReader with multi symbols" + "="*5)
    symbol = ["F", "GOOG"]
    dr_gfd = DataReader("GoogleFinanceDaily", expire_after=expire_after)
    data = dr_gfd.get(symbol, start, end)
    print(data)
    print(type(data))
    print(data.dtypes)

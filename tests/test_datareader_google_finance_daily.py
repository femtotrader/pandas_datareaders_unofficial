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
expire_after = 60*60 # seconds - 0:no cache - None:no cache expiration

import logging
#import logging.config
#import os

from datareaders.tools import to_float, to_int

def test_google_finance_daily():

    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2013, 1, 27)

    symbol = "F"

    dr_gfd = MyDataReader("GoogleFinanceDaily", expire_after=expire_after)
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

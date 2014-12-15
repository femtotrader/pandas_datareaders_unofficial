#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run unit tests using
nosetests -s -v
"""

import time
import datetime

from pandas_datareaders.datareader import DataReader

import pandas.io.data as web

import requests_cache
expire_after = 60*60 # seconds - 0:no cache - None:no cache expiration

import logging
#import logging.config
#import os

from pandas_datareaders.tools import to_float, to_int

def test_google_finance_intraday():

    symbol = "GOOG"
    #symbol = ["GOOG", "AAPL"]
    interval_seconds = 60
    num_days = 3
    data = DataReader("GoogleFinanceIntraday", expire_after=expire_after).get(symbol, exchange="NASD", interval_seconds=interval_seconds, num_days=num_days)
    print(data)

    symbol = ["GOOG", "AAPL"]
    interval_seconds = 60
    num_days = 3
    data = DataReader("GoogleFinanceIntraday", expire_after=expire_after).get(symbol, exchange="NASD", interval_seconds=interval_seconds, num_days=num_days)
    print(data)


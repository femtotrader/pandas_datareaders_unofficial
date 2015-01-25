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
from pandas_datareaders_unofficial.tools import to_float, to_int

import pandas.io.data as web

expire_after = timedelta(hours=1) # 0:no cache - None:no cache expiration

import logging
#import logging.config
#import os

def test_google_finance_intraday():

    symbol = "GOOG"
    #symbol = ["GOOG", "AAPL"]
    interval_seconds = 60
    num_days = 3
    data = DataReader("GoogleFinanceIntraday", expire_after=expire_after).get(symbol, exchange="NASD", interval=interval_seconds, num_days=num_days)
    print(data)
    assert(isinstance(data, pd.DataFrame))

    symbol = ["GOOG", "AAPL"]
    interval_seconds = 60
    num_days = 3
    data = DataReader("GoogleFinanceIntraday", expire_after=expire_after).get(symbol, exchange="NASD", interval=interval_seconds, num_days=num_days)
    print(data)
    assert(isinstance(data, pd.Panel))

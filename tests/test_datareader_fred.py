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

import logging
#import logging.config
#import os

def test_fred():

    filename = "fred"

    if expire_after>=0:
        requests_cache.install_cache(filename, backend='sqlite', expire_after=expire_after) # expiration seconds
        logging.info("Installing cache '%s.sqlite' with expire_after=%d (seconds)" % (filename, expire_after))
    if expire_after==0:
        logging.warning("expire_after==0 no cache expiration!")

    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2013, 1, 27)

    #name = "GDP"
    #name = "CPIAUCSL"
    #name = "CPILFESL"
    name = ["CPIAUCSL", "CPILFESL"]
    #name = ["CPIAUCSL", "CPILFESL", "ERROR"]


    data = MyDataReader("FRED").get(name, start, end)
    print(data)

    gdp = web.DataReader(name, "fred", start, end)

    print(gdp)
    print(type(gdp))
    print(gdp.ix['2013-01-01'])
    print(gdp.dtypes)

    diff = gdp - data
    assert(diff.sum().sum()==0)
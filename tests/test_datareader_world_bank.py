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

from datareaders import world_bank as wb

def test_datareader_world_bank():

    filename = "wb"

    if expire_after>=0:
        requests_cache.install_cache(filename, backend='sqlite', expire_after=expire_after) # expiration seconds
        logging.info("Installing cache '%s.sqlite' with expire_after=%d (seconds)" % (filename, expire_after))
    if expire_after==0:
        logging.warning("expire_after==0 no cache expiration!")

    dat = wb.search('gdp.*capita.*const')
    print(dat.iloc[:,:2])

    dat = wb.download(indicator='NY.GDP.PCAP.KD', country=['US', 'CA', 'MX'], start=2005, end=2008)
    print(dat)
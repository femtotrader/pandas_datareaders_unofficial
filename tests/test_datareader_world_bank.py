#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run unit tests using
nosetests -s -v
"""

import time
import datetime

from pandas_datareaders.datareader import *

import pandas.io.data as web

import requests_cache
expire_after = 60*60 # seconds - 0:no cache - None:no cache expiration

import logging
#import logging.config
#import os

from pandas_datareaders.datareaders import world_bank as wb

def test_datareader_world_bank():

    print("="*5 + "Pandas original DataReader" + "="*5)

    #dat = wb.search('gdp.*capita.*const')
    #print(dat.iloc[:,:2])

    #dat = wb.download(indicator=u'NY.GDP.PCAP.KD', country=['US', 'CA', 'MX'], start=2005, end=2008)
    #print(dat)

    #assert(isinstance(wb.country_codes, list))

    world_bank = MyDataReader("WorldBank", expire_after=expire_after)
    assert(isinstance(world_bank.country_codes, list))

    dat = world_bank.search('gdp.*capita.*const')
    print(dat.iloc[:,:2])

    dat = world_bank.download(indicator='NY.GDP.PCAP.KD', country=['US', 'CA', 'MX'], start=2005, end=2008)
    print(dat)

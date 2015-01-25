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
from pandas_datareaders_unofficial.datareaders import world_bank as wb

import pandas.io.data as web

expire_after = timedelta(hours=1) # 0:no cache - None:no cache expiration

import logging
#import logging.config
#import os


def test_datareader_world_bank():

    print("="*5 + "Pandas original DataReader" + "="*5)

    #dat = wb.search('gdp.*capita.*const')
    #print(dat.iloc[:,:2])

    #dat = wb.download(indicator=u'NY.GDP.PCAP.KD', country=['US', 'CA', 'MX'], start=2005, end=2008)
    #print(dat)

    #assert(isinstance(wb.country_codes, list))

    world_bank = DataReader("WorldBank", expire_after=expire_after)
    assert(isinstance(world_bank.country_codes, list))

    data = world_bank.search('gdp.*capita.*const')
    print(data.iloc[:,:2])
    assert(isinstance(data, pd.DataFrame))

    data = world_bank.download(indicator='NY.GDP.PCAP.KD', country=['US', 'CA', 'MX'], start=2005, end=2008)
    print(data)
    assert(isinstance(data, pd.DataFrame))

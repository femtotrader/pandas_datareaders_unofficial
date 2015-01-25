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

import pandas.io.data as web

expire_after = timedelta(hours=1) # 0:no cache - None:no cache expiration

import logging
#import logging.config
#import os

def test_famafrench():

    #name = "5_Industry_Portfolios"
    name = "10_Industry_Portfolios"
    #name = ["5_Industry_Portfolios", "10_Industry_Portfolios"]

    print("="*5 + "New DataReader" + "="*5)

    data = DataReader("FamaFrench", expire_after=expire_after).get(name)
    print(data)

    print("="*5 + "Pandas original DataReader" + "="*5)

    ip = web.DataReader(name, "famafrench")
    print(ip)

    diff = {}
    for key, val in ip.items():
        diff[key] = data[key] - ip[key]
        diff[key] = diff[key].sum().sum()
        assert(diff[key]==0.0)

    print("="*5 + "New DataReader with multi symbols" + "="*5)
    name = ["5_Industry_Portfolios", "10_Industry_Portfolios"]
    data = DataReader("FamaFrench", expire_after=expire_after).get(name)
    print(data)

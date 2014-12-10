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

def test_famafrench():

    #name = "5_Industry_Portfolios"
    name = "10_Industry_Portfolios"
    #name = ["5_Industry_Portfolios", "10_Industry_Portfolios"]

    data = MyDataReader("FamaFrench", expire_after=expire_after).get(name)
    print(data)

    print("="*5 + "Pandas original DataReader" + "="*5)

    ip = web.DataReader(name, "famafrench")
    print(ip)

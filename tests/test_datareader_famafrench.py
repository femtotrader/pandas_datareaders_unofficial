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

    filename = "famafrench"

    if expire_after>=0:
        requests_cache.install_cache(filename, backend='sqlite', expire_after=expire_after) # expiration seconds
        logging.info("Installing cache '%s.sqlite' with expire_after=%d (seconds)" % (filename, expire_after))
    if expire_after==0:
        logging.warning("expire_after==0 no cache expiration!")


    #name = "5_Industry_Portfolios"
    name = "10_Industry_Portfolios"
    #name = ["5_Industry_Portfolios", "10_Industry_Portfolios"]

    ip = web.DataReader(name, "famafrench")

    print(ip)

    data = MyDataReader("FamaFrench").get(name)

    print(data)
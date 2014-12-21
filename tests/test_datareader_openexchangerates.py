#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run unit tests using
nosetests -s -v
"""

import time
import datetime
import yaml
from pandas_datareaders import DataReader
import os

expire_after = 60*60 # seconds - 0:no cache - None:no cache expiration


def test_openexchangerates():
    print(os.environ['OPEN_EXCHANGE_RATES_API_KEY'])
    #here = os.path.abspath(path.dirname(__file__))
    #filename = os.path.join(here, 'tests.config.yml')
    filename = 'tests.config.yml'
    with open(filename) as f:
        config = yaml.load(f)
    app_id = config['tests']['datareaders']['OpenExchancheRates']['app_id']
    dr = DataReader("OpenExchangeRates", expire_after=expire_after, app_id=app_id)
    #data = dr.get()
    #print(data)
    #print(type(data))
    #print(data["matrix"])
    #data["matrix"].to_excel("rates_matrix.xls")

    currencies = ["EUR", "GBP", "CHF", "USD", "AUD", "CAD", "HKD", "INR", "JPY", "SAR", "SGD", "ZAR", "SEK", "AED"]
    data = dr.get(currencies)
    print(data["matrix"])

    print(dr.convert(100, "EUR", "USD"))
    print(dr.convert(100, "USD", "EUR"))
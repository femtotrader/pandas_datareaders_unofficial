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
import os
import yaml

from pandas_datareaders_unofficial import DataReader

expire_after = timedelta(hours=1) # 0:no cache - None:no cache expiration

def test_openexchangerates():
    app_id = os.environ['OPEN_EXCHANGE_RATES_API_KEY']
    print(app_id)
    dr = DataReader("OpenExchangeRates", expire_after=expire_after, app_id=app_id)
    #data = dr.get()
    #print(data)
    #print(type(data))
    #print(data["matrix"])
    #data["matrix"].to_excel("rates_matrix.xls")

    currencies = ["EUR", "GBP", "CHF", "USD", "AUD", "CAD", "HKD", "INR", "JPY", "SAR", "SGD", "ZAR", "SEK", "AED"]
    data = dr.get(currencies)

    #print(data)
    assert(isinstance(data, dict))

    print(data["matrix"])
    assert(isinstance(data["matrix"], pd.DataFrame))

    print(dr.convert(100, "EUR", "USD"))
    print(dr.convert(100, "USD", "EUR"))

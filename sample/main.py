#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

import os
import datetime

import numpy as np
import pandas as pd

import logging
import logging.config

import requests
import requests_cache

#import matplotlib.pyplot as plt

#import ts_charting as charting #https://github.com/dalejung/ts-charting

from pandas_datareaders import DataReader

@click.command()
@click.option('--expire_after', default=60*15, help=u"Cache expiration (-1: no cache, 0: no expiration, d: d seconds expiration cache)")
def main(expire_after):
    #filename = os.path.join(basepath, "request_cache")
    #if expire_after>=0:
    #    requests_cache.install_cache(filename, backend='sqlite', expire_after=expire_after) # expiration seconds
    #    logging.info("Installing cache '%s.sqlite' with expire_after=%d (seconds)" % (filename, expire_after))
    #if expire_after==0:
    #    logging.warning("expire_after==0 no cache expiration!")

    """
    # Google Finance Daily
    #symbol = "GOOG"
    #symbol = "AAPL"
    symbol = ["GOOG", "AAPL", "MSFT"]
    end_date = datetime.datetime.now()
    num_days = 200
    start_date = end_date - datetime.timedelta(days=num_days)
    data = DataReader("GoogleFinanceDaily", expire_after=expire_after).get(symbol, start_date, end_date)
    print(data)
    """

    """
    # Google Finance Intraday
    #symbol = "GOOG"
    symbol = ["GOOG", "AAPL"]
    interval_seconds = 60
    num_days = 3
    data = DataReader("GoogleFinanceIntraday", expire_after=expire_after).get(symbol, exchange="NASD", interval_seconds=interval_seconds, num_days=num_days)
    print(data)
    """

    # Yahoo Finance Daily
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2013, 1, 27)

    symbol = "F"
    symbol = "AAPL"
    #symbol = ["AAPL", 'F']

    data = DataReader("YahooFinanceDaily", expire_after=expire_after).get(symbol, start, end)
    print(data)
    print(type(data))
    print(data.dtypes)

    # FRED
    """
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2013, 1, 27)

    #name = "GDP"
    #name = "CPIAUCSL"
    #name = "CPILFESL"
    name = ["CPIAUCSL", "CPILFESL"]
    #name = ["CPIAUCSL", "CPILFESL", "ERROR"]

    data = DataReader("FRED", expire_after=expire_after).get(name, start, end)
    print(data)
    """

    """
    # Yahoo Finance Options
    symbol = "AAPL"
    option = DataReader("YahooFinanceOptions", expire_after=expire_after).get(symbol)
    data = option.get_all_data() # get all data
    print(data)
    #data = option.get_call_data(expiry=expiry) # get call data
    """

    """
    # Google Finance Options
    """

    """
    # FamaFrench
    name = "5_Industry_Portfolios"
    #name = "10_Industry_Portfolios"
    #name = ["5_Industry_Portfolios", "10_Industry_Portfolios"]
    data = DataReader("FamaFrench").get(name)
    print(data)
    """

    #fig = charting.figure(1)
    #df.tail(50).ohlc_plot()
    #plt.show()


if __name__ == '__main__':
    basepath = os.path.dirname(__file__)
    logging.config.fileConfig(os.path.join(basepath, "logging.conf"))
    logger = logging.getLogger("simpleExample")
    main()
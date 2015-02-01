#!/usr/bin/env python
#-*- coding:utf-8 -*-

import click

import os

import requests
import requests_cache

import logging
import traceback

import pandas as pd
from pandas.io.common import ZipFile
from pandas.tseries.frequencies import to_offset
from pandas.io.common import urlencode

import datetime
from datetime import timedelta

from six.moves import cStringIO as StringIO

def download_data(dt, symbol, session):    
    base_url = "http://hopey.netfonds.no"
    endpoint = "/tradedump.php"
    url = base_url + endpoint
    params = {
        'date': dt.strftime("%Y%m%d"),
        'paper': symbol,
        'csv_format': 'csv'
    }
    s_url = url+'?'+urlencode(params)
    print("Request %r" % s_url)
    response = session.get(url, params=params)
    return(response)

def get_data(dt, symbol, session):
    response = download_data(dt, symbol, session)
    data = StringIO(response.text)
    df = pd.read_csv(data, parse_dates=['time'])
    df = df.rename(columns={
        'time': 'Date',
        'price': 'Price',
        'quantity': 'Volume',
        'board': 'Board',
        'source': 'Source',
        'buyer': 'Buyer',
        'seller': 'Seller',
        'initiator': 'Initiator'

    })
    df = df.set_index('Date')
    return(df)

@click.command()
@click.option('--dt', default='', help="Date")
@click.option('--symbols', default='AAPL.O', help="Symbols list (separated with ','")
@click.option('--expire_after', default='24:00:00.0', \
    help=u"Cache expiration (-1: no cache, 0: no expiration, 00:15:00.0: expiration delay)")
def main(dt, symbols, expire_after):
    if expire_after=='-1':
        expire_after = None
    else:
        expire_after = pd.to_timedelta(expire_after, unit='s')
    session = requests_cache.CachedSession(cache_name='cache', expire_after=expire_after)
    if dt=='':
        dt = pd.to_datetime(datetime.datetime.utcnow())
    else:
        dt = pd.to_datetime(dt)
    data = get_data(dt, symbols, session)
    print(data)
    print(data.dtypes)

if __name__ == "__main__":
    main()

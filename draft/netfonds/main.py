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

def _convert(data, f_conv):
    return(f_conv(data))

def convert(arg, mod):
    def actual_convert(fn):
        if arg not in fn.__code__.co_varnames:
            return fn
        else:
            def new_function(*args, **kwargs):
                l_args = list(args)
                index = fn.__code__.co_varnames.index(arg)
                l_args[index] = mod(l_args[fn.__code__.co_varnames.index(arg)])
                args = tuple(l_args)
                return fn(*args, **kwargs)
            return new_function
    return actual_convert

def to_date(dt):
    if dt=='':
        return(pd.to_datetime(datetime.datetime.utcnow().date()))
    else:
        return(pd.to_datetime(dt))

d_exchange = {
    'NASDAQ': 'O',
    'NYSE': 'N',
    'AMEX': 'A'
}

def download_data(endpoint, params, session):
    base_url = "http://hopey.netfonds.no"
    url = base_url + endpoint
    s_url = url+'?'+urlencode(params)
    print("Request %r" % s_url)
    response = session.get(url, params=params)
    return(response)

@convert("dt", to_date)
def get_data(dt, symbol, depth, session):
    #dt = convert(dt, to_date)

    if not depth:
        endpoint = "/tradedump.php"
    else:
        endpoint = "/posdump.php"

    params = {
        'date': dt.strftime("%Y%m%d"),
        'paper': symbol,
        'csv_format': 'csv'
    }
    response = download_data(endpoint, params, session)
    data = StringIO(response.text)
    df = pd.read_csv(data, parse_dates=['time'])
    df.columns = df.columns.map(lambda col: col.title())
    df = df.rename(columns={
        'Time': 'Date',
    })
    df = df.set_index('Date')
    return(df)

@click.command()
@click.option('--dt', default='', help="Date")
@click.option('--symbols', default='AAPL.O', help="Symbols list (separated with ','")
@click.option('--depth/--no-depth', default=False)
@click.option('--expire_after', default='24:00:00.0', \
    help=u"Cache expiration (-1: no cache, 0: no expiration, 00:15:00.0: expiration delay)")
def main(dt, symbols, depth, expire_after):
    if expire_after=='-1':
        expire_after = None
    else:
        expire_after = pd.to_timedelta(expire_after, unit='s')
    session = requests_cache.CachedSession(cache_name='cache', expire_after=expire_after)
    data = get_data(dt, symbols, depth, session)
    print(data)
    print(data.dtypes)

if __name__ == "__main__":
    main()

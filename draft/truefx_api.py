#!/usr/bin/env python
# -*- coding: utf-8 -*-

from truefx_config import config
#class config(object):
#    username = "" # put your own TrueFX username
#    password = "" # put your own TrueFX password

import requests
import requests_cache
import datetime
import pandas as pd
from datetime import timedelta
from pandas.io.common import urlencode
from six.moves import cStringIO as StringIO

def send_request(session, params):
    base_url = "http://webrates.truefx.com/rates"
    endpoint = "/connect.html"
    url = base_url + endpoint
    #print("Request to '%s' with '%s' using '%s'" % (url, params, url+'?'+urlencode(params)))
    response = session.get(url, params=params)
    return(response)

def connect(session, username, password, qualifier, lst_symbols, format='csv', snapshot=True):
    if snapshot:
        s = 'y'
    else:
        s = 'n'

    params = {
        'u': username,
        'p': password,
        'q': qualifier,
        'c': ','.join(lst_symbols),
        'f': format,
        's': s
    }

    response = send_request(session, params)
    if response.status_code != 200:
        raise(NotImplementedError)
    
    session_data = response.text
    session_data = session_data.strip()

    return(session_data)

def disconnect(session, session_data):
    params = {
        'di': session_data,
    }
    response = send_request(session, params)
    return(response)

def query(session, session_data):
    params = {
        'id': session_data,
    }
    response = send_request(session, params)
    return(response)

def parse_data(data):
    data_io = StringIO(data)
    df = pd.read_csv(data_io, header=None, names=['Symbol', 'Date', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df = df.set_index('Symbol')
    return(df)

if __name__ == "__main__":
    #session = requests.Session()

    expire_after = timedelta(hours=1)
    session = requests_cache.CachedSession(cache_name='cache', expire_after=expire_after)
    
    symbols = "EUR/USD,USD/JPY"
    symbols = symbols.split(',')
    #symbols = ["EUR/USD", "USD/JPY"]
    #symbols = ["EUR/USD", "USD/JPY", "GBP/USD", "EUR/GBP", "USD/CHF", \
    #"EUR/JPY", "EUR/CHF", "USD/CAD", "AUD/USD", "GBP/JPY", \
    #"AUD/JPY", "AUD/NZD", "CAD/JPY", "CHF/JPY", "NZD/USD"]

    qualifier = 'default'

    format = 'csv'
    snapshot = True

    print("Connect")
    session_data = connect(session, config.username, config.password, qualifier, symbols, format, snapshot)

    response = query(session, session_data)
    data = response.text
    print("Query response:\n%s" % data)
    df = parse_data(data)
    print(df)

    print("Disconnect")
    response = disconnect(session, session_data)
    data = response.text
    print(data)

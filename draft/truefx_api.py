#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API to get FX prices from TrueFX

http://www.truefx.com/
http://www.truefx.com/?page=download&description=api
http://www.truefx.com/dev/data/TrueFX_MarketDataWebAPI_DeveloperGuide.pdf
"""

#from truefx_config import config
#class config(object):
#    username = "" # put your own TrueFX username
#    password = "" # put your own TrueFX password

import click

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
    print("Request to '%s' with '%s' using '%s'" % (url, params, url+'?'+urlencode(params)))
    response = session.get(url, params=params)
    return(response)

def connect(session, username, password, lst_symbols, qualifier='default', format='csv', snapshot=True):
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
        raise(Exception("Can't connect"))
    
    session_data = response.text
    session_data = session_data.strip()

    return(session_data)

def disconnect(session, session_data):
    params = {
        'di': session_data,
    }
    response = send_request(session, params)
    return(response)

def query_auth_send(session, session_data):
    params = {
        'id': session_data,
    }
    response = send_request(session, params)
    return(response)

def parse_data(data):
    data_io = StringIO(data)
    df = pd.read_csv(data_io, header=None, names=['Symbol', 'Date', 'Bid', 'Bid_point', 'Ask', 'Ask_point', 'High', 'Low', 'Open'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df = df.set_index('Symbol')
    return(df)

def query_not_auth(session, lst_symbols, format='csv', snapshot=True):
    if snapshot:
        s = 'y'
    else:
        s = 'n'

    params = {
        'c': ','.join(lst_symbols),
        'f': format,
        's': s
    }

    response = send_request(session, params)
    if response.status_code != 200:
        raise(Exception("Can't connect"))

    return(response)

def registered(username, password):
    return(not (username=='' and password==''))

SYMBOLS_NOT_AUTH = "EUR/USD,USD/JPY,GBP/USD,EUR/GBP,USD/CHF,EUR/JPY,EUR/CHF"
SYMBOLS_NOT_AUTH = "," + "USD/CAD,AUD/USD,GBP/JPY"

SYMBOLS_ALL = "EUR/USD,USD/JPY,GBP/USD,EUR/GBP,USD/CHF,AUD/NZD,CAD/CHF,CHF/JPY,EUR/AUD"
SYMBOLS_ALL = SYMBOLS_ALL + "," + "EUR/CAD,EUR/JPY,EUR/CHF,USD/CAD,AUD/USD,GBP/JPY,AUD/CAD"
SYMBOLS_ALL = SYMBOLS_ALL + "," + "AUD/CHF,AUD/JPY,EUR/NOK,EUR/NZD,GBP/CAD,GBP/CHF,NZD/JPY"
SYMBOLS_ALL = SYMBOLS_ALL + "," + "NZD/USD,USD/NOK,USD/SEK"

@click.command()
@click.option('--symbols', default='', help="Symbols list (serated with ','")
@click.option('--username', default='', help="Username")
@click.option('--password', default='', help="Password")
def main(symbols, username, password):
    #session = requests.Session()

    expire_after = timedelta(hours=1)
    session = requests_cache.CachedSession(cache_name='cache', expire_after=expire_after)

    is_registered = registered(username, password)
    if not is_registered:
        print("""You should register to TrueFX
and pass username and password using CLI flag
--username your_username
--password your_password""")

    if symbols == '':
        if not is_registered:
            symbols = SYMBOLS_NOT_AUTH
        else:
            symbols = SYMBOLS_ALL
    
    symbols = symbols.split(',')

    qualifier = 'default'

    format = 'csv'
    snapshot = True

    if not is_registered:
        response = query_not_auth(session, symbols, format, snapshot)
        data = response.text
        print("Query response:\n%s" % data)
        df = parse_data(data)
        print("Query parsed response:\n%s" % df)
        print(df)
    else:
        print("Connect")
        #(username, password) = (config.username, config.password)
        #(username, password) = ('', '')
        session_data = connect(session, username, password, symbols, qualifier, format, snapshot)
        error_msg = 'not authorized'
        if error_msg in session_data:
            raise(Exception(error_msg))

        response = query_auth_send(session, session_data)
        data = response.text
        print("Query response:\n%s" % data)
        df = parse_data(data)
        print("Query parsed response:\n%s" % df)
        print(df)

        print("Disconnect")
        response = disconnect(session, session_data)
        data = response.text
        print(data)

if __name__ == "__main__":
    main()

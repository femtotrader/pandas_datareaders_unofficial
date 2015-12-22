#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API to get FX prices from TrueFX

http://www.truefx.com/
http://www.truefx.com/?page=download&description=api
http://www.truefx.com/dev/data/TrueFX_MarketDataWebAPI_DeveloperGuide.pdf
"""

import logging
logger = logging.getLogger(__name__)

import click

import os
import requests
import requests_cache
import datetime

import pandas as pd
#pd.set_option('max_rows', 10)
pd.set_option('expand_frame_repr', False)
pd.set_option('max_columns', 8)

from datetime import timedelta
from pandas.io.common import urlencode
import pandas.compat as compat

def send_request(session, params, debug):
    base_url = "http://webrates.truefx.com/rates"
    endpoint = "/connect.html"
    url = base_url + endpoint
    s_url = url+'?'+urlencode(params)
    logging.debug("Request to '%s' with '%s' using '%s'" % (url, params, s_url))
    response = session.get(url, params=params)
    return(response)

def connect(session, username, password, lst_symbols, qualifier, \
        api_format, snapshot, debug):

    s = 'y' if snapshot else 'n'

    params = {
        'u': username,
        'p': password,
        'q': qualifier,
        'c': ','.join(lst_symbols),
        'f': api_format,
        's': s
    }

    response = send_request(session, params, debug)
    if response.status_code != 200:
        raise(Exception("Can't connect"))
    
    session_data = response.text
    session_data = session_data.strip()

    return(session_data)

def disconnect(session, session_data, debug):
    params = {
        'di': session_data,
    }
    response = send_request(session, params, debug)
    return(response)

def query_auth_send(session, session_data, debug):
    params = {
        'id': session_data,
    }
    response = send_request(session, params, debug)
    return(response)

def parse_data(data):
    data_io = compat.StringIO(data)
    df = pd.read_csv(data_io, header=None, \
        names=['Symbol', 'Date', 'Bid', 'Bid_point', \
            'Ask', 'Ask_point', 'High', 'Low', 'Open'])

    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df = df.set_index('Symbol')
    return(df)

def query_not_auth(session, lst_symbols, api_format, snapshot, debug):
    s = 'y' if snapshot else 'n'

    params = {
        'c': ','.join(lst_symbols),
        'f': api_format,
        's': s
    }

    response = send_request(session, params, debug)
    if response.status_code != 200:
        raise(Exception("Can't connect"))

    return(response)

def registered(username, password):
    return(not (username=='' and password==''))

def get_session(session=None):
    if session is None:
        return(requests.Session())
    else:
        return(session)

def query(symbols='', qualifier='default', api_format='csv', snapshot=True, \
        username='', password='', force_unregistered=False, flag_parse_data=True, session=None, debug=True):

    (username, password) = credentials(username, password)
    session = get_session(session)

    is_registered = registered(username, password)

    if isinstance(symbols, compat.string_types):
        symbols = symbols.upper()
        symbols = symbols.split(',')
    else:
        symbols = list(map(lambda s: s.upper(), symbols))

    if symbols == ['']:
        if not is_registered:
            symbols = SYMBOLS_NOT_AUTH
        else:
            symbols = SYMBOLS_ALL
    
    if not is_registered or force_unregistered:
        response = query_not_auth(session, symbols, api_format, snapshot, debug)
        data = response.text
        if flag_parse_data:
            df = parse_data(data)
            return(df)
        else:
            return(data)
    else:
        session_data = connect(session, username, password, symbols, qualifier, \
            api_format, snapshot, debug)
        error_msg = 'not authorized'
        if error_msg in session_data:
            raise(Exception(error_msg))

        response = query_auth_send(session, session_data, debug)
        data = response.text

        response = disconnect(session, session_data, debug)

        if flag_parse_data:
            df = parse_data(data)
            return(df)
        else:
            return(data)

def credentials(username='', password=''):
    if username=='':
        username = os.getenv('TRUEFX_USERNAME')
    if password=='':
        password = os.environ['TRUEFX_PASSWORD']
    return(username, password)

SYMBOLS_NOT_AUTH = ['EUR/USD', 'USD/JPY', 'GBP/USD', 'EUR/GBP', 'USD/CHF', \
    'EUR/JPY', 'EUR/CHF', 'USD/CAD', 'AUD/USD', 'GBP/JPY']

SYMBOLS_ALL = ['EUR/USD', 'USD/JPY', 'GBP/USD', 'EUR/GBP', 'USD/CHF', 'AUD/NZD', \
    'CAD/CHF', 'CHF/JPY', 'EUR/AUD', 'EUR/CAD', 'EUR/JPY', 'EUR/CHF', 'USD/CAD', \
    'AUD/USD', 'GBP/JPY', 'AUD/CAD', 'AUD/CHF', 'AUD/JPY', 'EUR/NOK', 'EUR/NZD', \
    'GBP/CAD', 'GBP/CHF', 'NZD/JPY', 'NZD/USD', 'USD/NOK', 'USD/SEK']

@click.command()
@click.option('--symbols', default='', help="Symbols list (separated with ','")
@click.option('--username', default='', help="TrueFX username")
@click.option('--password', default='', help="TrueFX password")
@click.option('--force-unregistered/--no-force-unregistered', default=False, \
    help=u"Force unregistered")
@click.option('--expire_after', default='00:15:00.0', \
    help=u"Cache expiration (-1: no cache, 0: no expiration, 00:15:00.0: expiration delay)")
def main(symbols, username, password, force_unregistered, expire_after):

    print("""TrueFX - Python API call
========================
""")

    if expire_after=='-1':
        expire_after = None
    else:
        expire_after = pd.to_timedelta(expire_after, unit='s')

    #session = requests.Session()
    session = requests_cache.CachedSession(\
        cache_name='cache_truefx', expire_after=expire_after)

    (username, password) = credentials(username, password)
    is_registered = registered(username, password)
    
    if not is_registered or force_unregistered:
        print("""You should register to TrueFX at
http://www.truefx.com/
and pass username and password using CLI flag
--username your_username
--password your_password

or setting environment variables using:
export TRUEFX_USERNAME="your_username"
export TRUEFX_PASSWORD="your_password"
""")

    qualifier = 'default'
    api_format = 'csv'
    snapshot = True
    flag_parse_data = True
    debug = True

    data = query(symbols, qualifier, api_format, snapshot, username, password, \
        force_unregistered, flag_parse_data, session, debug)

    print(data)

if __name__ == "__main__":
    main()

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

SYMBOLS_NOT_AUTH = ['EUR/USD', 'USD/JPY', 'GBP/USD', 'EUR/GBP', 'USD/CHF', \
    'EUR/JPY', 'EUR/CHF', 'USD/CAD', 'AUD/USD', 'GBP/JPY']

SYMBOLS_ALL = ['EUR/USD', 'USD/JPY', 'GBP/USD', 'EUR/GBP', 'USD/CHF', 'AUD/NZD', \
    'CAD/CHF', 'CHF/JPY', 'EUR/AUD', 'EUR/CAD', 'EUR/JPY', 'EUR/CHF', 'USD/CAD', \
    'AUD/USD', 'GBP/JPY', 'AUD/CAD', 'AUD/CHF', 'AUD/JPY', 'EUR/NOK', 'EUR/NZD', \
    'GBP/CAD', 'GBP/CHF', 'NZD/JPY', 'NZD/USD', 'USD/NOK', 'USD/SEK']

def _send_request(session, params):
    base_url = "http://webrates.truefx.com/rates"
    endpoint = "/connect.html"
    url = base_url + endpoint
    s_url = url+'?'+urlencode(params)
    logging.debug("Request to '%s' with '%s' using '%s'" % (url, params, s_url))
    response = session.get(url, params=params)
    return(response)

def _connect(session, username, password, lst_symbols, qualifier, \
        api_format, snapshot):

    s = 'y' if snapshot else 'n'

    params = {
        'u': username,
        'p': password,
        'q': qualifier,
        'c': ','.join(lst_symbols),
        'f': api_format,
        's': s
    }

    response = _send_request(session, params)
    if response.status_code != 200:
        raise(Exception("Can't connect"))
    
    session_data = response.text
    session_data = session_data.strip()

    return(session_data)

def _disconnect(session, session_data):
    params = {
        'di': session_data,
    }
    response = _send_request(session, params)
    return(response)

def _query_auth_send(session, session_data):
    params = {
        'id': session_data,
    }
    response = _send_request(session, params)
    return(response)

def _parse_data(data):
    data_io = compat.StringIO(data)
    df = pd.read_csv(data_io, header=None, \
        names=['Symbol', 'Date', 'Bid', 'Bid_point', \
            'Ask', 'Ask_point', 'High', 'Low', 'Open'])

    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df = df.set_index('Symbol')
    return(df)

def _query_not_auth(session, lst_symbols, api_format, snapshot):
    s = 'y' if snapshot else 'n'

    params = {
        'c': ','.join(lst_symbols),
        'f': api_format,
        's': s
    }

    response = _send_request(session, params)
    if response.status_code != 200:
        raise(Exception("Can't connect"))

    return(response)

def _is_registered(username, password):
    return(not (username=='' and password==''))

def _init_session(session=None):
    if session is None:
        return(requests.Session())
    else:
        return(session)

def _query(symbols='', qualifier='default', api_format='csv', snapshot=True, \
        username='', password='', force_unregistered=False, flag_parse_data=True, session=None):

    (username, password) = _init_credentials(username, password)
    session = _init_session(session)

    is_registered = _is_registered(username, password)

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
        response = _query_not_auth(session, symbols, api_format, snapshot)
        data = response.text
    else:
        session_data = _connect(session, username, password, symbols, qualifier, \
            api_format, snapshot)
        error_msg = 'not authorized'
        if error_msg in session_data:
            raise(Exception(error_msg))

        response = _query_auth_send(session, session_data)
        data = response.text

        response = _disconnect(session, session_data)

    if flag_parse_data:
        df = _parse_data(data)
        return(df)
    else:
        return(data)

def read(symbols, username, password, force_unregistered, session):

    qualifier = 'default'
    api_format = 'csv'
    snapshot = True
    flag_parse_data = True

    data = _query(symbols, qualifier, api_format, snapshot, username, password, \
        force_unregistered, flag_parse_data, session)

    return data

def _init_credentials(username='', password=''):
    if username=='':
        username = os.getenv('TRUEFX_USERNAME')
    if password=='':
        password = os.getenv('TRUEFX_PASSWORD')
    return(username, password)

def _get_session(expire_after, cache_name='cache'):
    """
    Returns a `requests.Session` or a `requests_cache.CachedSession`

    Parameters
    ----------
    expire_after : `str`    
        cache expiration delay
                    '-1' : no cache
                     '0' : no expiration
            '00:15:00.0' : expiration delay

    cache_filename : `str`
        Name of cache file

    """
    if expire_after=='-1':
        expire_after = None
        logger.debug("expire_after==0 no cache")
        session = requests.Session()
    else:
        if expire_after=='0':
            expire_after = 0
            logger.debug("Installing cache '%s.sqlite' without expiration" % cache_name)
        else:
            expire_after = pd.to_timedelta(expire_after, unit='s')
            logger.debug("Installing cache '%s.sqlite' with expire_after=%s (d days hh:mm:ss)" % (cache_name, expire_after))
        session = requests_cache.CachedSession(\
            cache_name=cache_name, expire_after=expire_after)
    return session

@click.command()
@click.option('--symbols', default='', help="Symbols list (separated with ','")
@click.option('--username', default='', help="TrueFX username")
@click.option('--password', default='', help="TrueFX password")
@click.option('--force-unregistered/--no-force-unregistered', default=False, \
    help=u"Force unregistered")
@click.option('--expire_after', default='00:15:00.0', \
    help=u"Cache expiration (-1: no cache, 0: no expiration, 00:15:00.0: expiration delay)")
def main(symbols, username, password, force_unregistered, expire_after):
    logging.basicConfig(level=logging.DEBUG)

    print("""TrueFX - Python API call
========================
""")

    session = _get_session(expire_after)

    (username, password) = _init_credentials(username, password)
    is_registered = _is_registered(username, password)
    
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

    data = read(symbols, username=username, password=password, force_unregistered=force_unregistered, session=session)

    print(data)

if __name__ == "__main__":
    main()

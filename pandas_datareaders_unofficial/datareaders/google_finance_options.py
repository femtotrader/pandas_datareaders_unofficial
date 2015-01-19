#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import DataReaderBase
from ..tools import COL, _get_dates, to_float, to_int

import pandas as pd
#from pandas.tseries.frequencies import to_offset
from six.moves import cStringIO as StringIO
import logging
import traceback
import datetime

import json
import token, tokenize


def ymd_to_date(y, m, d):
    """
    Returns date

    >>> expiration = {u'd': 1, u'm': 12, u'y': 2014}
    >>> ymd_to_date(**expiration)
    datetime.date(2014, 12, 1)

    >>> ymd_to_date(2014, 3, 1)
    datetime.date(2014, 3, 1)

    """
    return(datetime.date(year=y, month=m, day=d))

def date_to_ymd(date):
    """
    Returns dict like {'y': ..., 'm': ..., 'd': ...}

    >>> date_to_ymd(datetime.date(year=2010, month=1, day=3))
    {'y': 2010, 'm': 1, 'd': 3}
    """
    d = {
        'y': date.year,
        'm': date.month,
        'd': date.day
    }
    return(d)

def fix_lazy_json(in_text):
    """
    Handle lazy JSON - to fix expecting property name
    this function fixes the json output from google
    http://stackoverflow.com/questions/4033633/handling-lazy-json-in-python-expecting-property-name
    """
    tokengen = tokenize.generate_tokens(StringIO(in_text).readline)

    result = []
    for tokid, tokval, _, _, _ in tokengen:
        # fix unquoted strings
        if (tokid == token.NAME):
            if tokval not in ['true', 'false', 'null', '-Infinity', 'Infinity', 'NaN']:
                tokid = token.STRING
                tokval = u'"%s"' % tokval

        # fix single-quoted strings
        elif (tokid == token.STRING):
            if tokval.startswith ("'"):
                tokval = u'"%s"' % tokval[1:-1].replace ('"', '\\"')

        # remove invalid commas
        elif (tokid == token.OP) and ((tokval == '}') or (tokval == ']')):
            if (len(result) > 0) and (result[-1][1] == ','):
                result.pop()

        # fix single-quoted strings
        elif (tokid == token.STRING):
            if tokval.startswith ("'"):
                tokval = u'"%s"' % tokval[1:-1].replace ('"', '\\"')

        result.append((tokid, tokval))

    return tokenize.untokenize(result)

def json_decode(json_string):
    try:
        ret = json.loads(json_string)
    except:
        json_string = fix_lazy_json(json_string)
        ret = json.loads(json_string)
    return ret

class DataReaderGoogleFinanceOptions(DataReaderBase):
    """
    DataReader to fetch data from Google Finance Options

    see https://www.google.com/finance/option_chain
    https://github.com/makmac213/python-google-option-chain
    http://www.drtomstarke.com/index.php/option-chains-from-google-finance-api
    """
    def init(self, *args, **kwargs):
        self._get_multi = self._get_multi_todict

    def _get_one(self, name, *args, **kwargs):
        return(self._get_one_raw(name, 'All', 'json'))

    def _get_one_raw(self, symbol, typ='All', output='json', y='2014', m='12', d='1'):
        url = "https://www.google.com/finance/option_chain"

        params = {
            'q': symbol,
            'type': typ,
            'output': output,
        }

        data = self._get_content(url, params)

        d = {}
        lst = []
        for typ in [u'puts', u'calls']:
            df_typ = pd.DataFrame(data[typ])
            df_typ['Type'] = typ
            lst.append(df_typ)    
            del data[typ]

        for i, expiration in enumerate(data['expirations']):
            params = {
                'q': symbol,
                'output': output,
                'expy': expiration['y'],
                'expm': expiration['m'],
                'expd': expiration['d'],
            }
            data = self._get_content(url, params)
            for typ in [u'puts', u'calls']:
                df_typ = pd.DataFrame(data[typ])
                df_typ['Type'] = typ
                lst.append(df_typ)
                del data[typ]
            lst.append(df_typ)
      
        df = pd.concat(lst, axis=0, ignore_index=True)

        d_cols = {
            "a": "Ask",
            "b": "Bid",
            "p": "Last",
            "strike": "Strike",
            "expiry": "Expiry",
            "vol": "Volume",
            "name": "Name"
        }

        df = df.rename(columns=d_cols)

        """
        d_cols = {
            "a": "ask",
            "b": "bid",
            "c": "change",
            "cid": "identity code",
            "cp": "cp"
            "cs": change direction.  "chg" = up, "chr" = down, "chg"?
            "e":  # I think this tells us something about what country where the stock is traded. "OPRA" means USA.
            "expiry": expiration date for this option
            "name": I don't know.  I have never seen a value for this
            "oi": open interest. How many of these are currently being held by others. 
                See, http://www.investopedia.com/terms/o/openinterest.asp
            "p": price, last
            "s": option code.
                 Basically, Stock Symbol + 7 if mini option + date + "C" or "P" + price
            "strike": "strike price for this option"
            "vol": "the volume of options traded."
        }
        """

        for col in ['Ask', 'Bid', 'c', 'cp', 'Last', 'Strike']:
            df[col] = df[col].map(to_float)

        for col in ['Volume', 'oi', 'cid']:
            df[col] = df[col].map(to_int)

        df['Expiry'] = pd.to_datetime(df['Expiry'])
        
        data['options'] = df

        data['underlying_id'] = int(data['underlying_id'])
        data['expiry'] = ymd_to_date(**data['expiry'])

        for i, expiration in enumerate(data['expirations']):
            data['expirations'][i] = ymd_to_date(**expiration)            

        #for col in ['Volume']:
        #    df[col] = df[col].fillna(0)

        #d = {}
        #d["options"] = df
        #return(d)

        return(data)

    def _get_content(self, url, params):
        #response = requests.get(url, params=params)
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            content_json = response.text
            data = json_decode(content_json)
            return(data)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

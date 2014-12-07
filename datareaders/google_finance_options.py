#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datareaders.base import DataReaderBase
from datareaders.tools import COL, _get_dates, to_float, to_int
import pandas as pd
#from pandas.tseries.frequencies import to_offset
from StringIO import StringIO
import logging
import traceback


import json
import token, tokenize

from StringIO import StringIO


# using below solution fixes the json output from google
# http://stackoverflow.com/questions/4033633/handling-lazy-json-in-python-expecting-property-name
def fixLazyJson (in_text):
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
        json_string = fixLazyJson(json_string)
        ret = json.loads(json_string)
    return ret


class DataReaderGoogleFinanceOptions(DataReaderBase):
    """
    see https://www.google.com/finance/option_chain
    https://github.com/makmac213/python-google-option-chain
    """

    def _get_one(self, name, *args, **kwargs):
        return(self._get_one_raw(name, 'All', 'json'))

    def _get_one_raw(self, symb, typ='All', output='json'):
        url = "https://www.google.com/finance/option_chain"
        params = {
            'q': symb,
            'type': typ,
            'output': output
        }
        data = self._get_content(url, params)

        d = {}
        lst = []
        for typ in [u'puts', u'calls']:
            df_typ = pd.DataFrame(data[typ])
            df_typ['Type'] = typ
            lst.append(df_typ)            

        df = pd.concat(lst, axis=0, ignore_index=True)

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

        for col in ['a', 'b', 'c', 'cp', 'p', 'strike']:
            df[col] = df[col].map(to_float)

        for col in ['vol', 'oi', 'cid']:
            df[col] = df[col].map(to_int)

        df['expiry'] = pd.to_datetime(df['expiry'])
        
        return(df)

    def _get_content(self, url, params):
        response = self.s.get(url, params=params)
        if response.status_code == 200:
            content_json = response.content
            data = json_decode(content_json)
            return(data)

    def _get_multi(self, names, *args, **kwargs):
        lst_data = []
        lst_failed = []

        for name in names:
            try:
                df_one = self._get_one(name, *args, **kwargs)
                df_one['Symbol'] = name
                lst_data.append(df_one)
            except IOError:
                logging.warning("Failed to read symbol: {0!r}, replacing with 'NaN.".format(name))
                lst_failed.append(sym)

        df = pd.concat(lst_data, axis=0)
        #df = df.sort(['Symbol', 'Type', 'strike'])
        df = df.set_index(['Symbol', 'Type', 'cid'])

        return(df)
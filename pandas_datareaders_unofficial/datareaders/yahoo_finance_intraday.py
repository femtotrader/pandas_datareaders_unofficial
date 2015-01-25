#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import DataReaderBase
from ..tools import COL, _get_dates, to_float, to_int, timestamp_to_unix

import pandas as pd
#from pandas.tseries.frequencies import to_offset
from six.moves import cStringIO as StringIO
import logging
import traceback
import json
#import re

class DataReaderYahooFinanceIntraday(DataReaderBase):
    """
    DataReader to fetch data from Yahoo Finance Intraday

    Url example: http://chartapi.finance.yahoo.com/instrument/1.0/GOOG/chartdata;type=quote;range=1d/json

    Ref:
    http://www.quantshare.com/sa-426-6-ways-to-download-free-intraday-and-tick-data-for-the-us-stock-market
    """
    def init(self, *args, **kwargs):
        self._get_multi = self._get_multi_topanel

    def _get_one(self, name, *args, **kwargs):
        try:
            num_days = kwargs['duration']
        except:
            num_days = 1

        period = "%dd" % num_days

        return(get_raw(name, period, self.session))


#from requests import Session
#session = Session()

def get_raw(symbol, period, session):
    url = "http://chartapi.finance.yahoo.com/instrument/1.0/{symbol}/chartdata;type=quote;range={period}/json".format(symbol=symbol, period=period)
    response = session.get(url)
    data = response.text
    data = data.replace('finance_charts_json_callback( ','')[:-1]  # strip away the javascript
    #data = data.replace("\n", "")
    #pattern = "^finance_charts_json_callback\( (.*) \)$"
    #data = re.match(pattern, data).group(1)
    data = json.loads(data)['series']
    df = pd.DataFrame(data)
    df = df.rename(columns={
        'Timestamp': 'Date',
        'close': 'Close',
        'high': 'High',
        'low': 'Low',
        'open': 'Open',
        'volume': 'Volume'
    })
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Date'] = pd.to_datetime(df['Date'], unit='s')
    df = df.set_index('Date')
    return(df)

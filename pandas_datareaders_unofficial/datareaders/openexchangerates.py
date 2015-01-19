#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import DataReaderBase
from ..tools import COL, _get_dates

import pandas as pd
from six.moves import cStringIO as StringIO
import logging
import traceback
import json

class DataReaderOpenExchangeRates(DataReaderBase):
    """
    DataReader to fetch currencies rates from OpenExchangeRates
    https://openexchangerates.org/
    """

    BASE_URL = 'http://openexchangerates.org/api'

    def init(self, *args, **kwargs):
        try:
            self.app_id = kwargs['app_id']
        except:
            raise(NotImplementedError("app_id missing"))

    def _get_raw(self, currencies, *args, **kwargs):
        endpoint = '/latest.json'
        url = self._url(endpoint)
        params = {
            'app_id': self.app_id
        }
        response = self.session.get(url, params=params)
        raw_data = response.text
        self._data = json.loads(raw_data)
        self._data["timestamp"] = pd.to_datetime(self._data['timestamp']*1000000000)
        base = self._data["base"]
        cur1 = base
        d = self._data["rates"]
        if currencies is None:
            currencies = sorted(d.keys())
        df = pd.DataFrame(columns=currencies, index=currencies)

        for cur1 in currencies:
            for cur2 in currencies:
                df[cur1][cur2] = d[cur1] / d[cur2]

        self._data["matrix"] = df
        return(self._data)

    def _get_one(self, currencies, *args, **kwargs):
        return(self._get_raw(currencies, *args, **kwargs))

    def _get_multi(self, currencies, *args, **kwargs):
        return(self._get_raw(currencies, *args, **kwargs))

    def convert(self, amount, from_cur, to_cur):
        return(self._data["matrix"][to_cur][from_cur]*amount)

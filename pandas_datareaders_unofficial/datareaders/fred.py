#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import DataReaderBase
from ..tools import _get_dates

import pandas as pd
from six.moves import cStringIO as StringIO
import logging
import traceback
import requests

class DataReaderFRED(DataReaderBase):
    """
    DataReader to fetch data from FRED
    """

    def init(self, *args, **kwargs):
        pass

    def _get_one(self, name, *args, **kwargs):
        """
        Get data for the given name from the St. Louis FED (FRED).
        Date format is datetime
        Returns a DataFrame.
        If multiple names are passed for "series" then the index of the
        DataFrame is the outer join of the indicies of each series.
        """
        start, end = _get_dates(0, *args, **kwargs)

        url = "http://research.stlouisfed.org/fred2/series/" \
            "{name}/downloaddata/{name}.csv".format(name=name)

        #response = requests.get(url)
        response = self.session.get(url)
        data = response.text
        if response.status_code!=200:
            raise IOError("Failed to get the data. Check that {0!r} is "
                          "a valid FRED series.".format(name))

        df = pd.read_csv(StringIO(data), sep=',', index_col=0, parse_dates=True, \
            skiprows=0, na_values='.')
        df.index.name = 'Date'
        s = df['VALUE']
        s.name = name

        return(s.truncate(start, end))
    

    def _get_multi(self, names, *args, **kwargs):
        lst_data = []
        lst_failed = []

        for name in names:
            try:
                data = self._get_one(name, *args, **kwargs)
                lst_data.append(data)
            except:
                logging.error(traceback.format_exc())
                lst_failed.append(name)

        df = pd.concat(lst_data, axis=1, join='outer')

        for name in lst_failed:
            df[name] = np.nan

        return(df)


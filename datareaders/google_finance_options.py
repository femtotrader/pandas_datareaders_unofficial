#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datareaders.base import DataReaderBase
from datareaders.tools import COL, _get_dates, to_float, to_int
import pandas as pd
#from pandas.tseries.frequencies import to_offset
from StringIO import StringIO
import logging
import traceback

class DataReaderGoogleFinanceOptions(DataReaderBase):
    pass
    """
    see https://www.google.com/finance/option_chain
    https://github.com/makmac213/python-google-option-chain
    """

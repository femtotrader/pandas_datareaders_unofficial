#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pandas.core.common import PandasError
import logging
import traceback
import numpy as np
import datetime

class COL():
    DATE = 'Date'
    OPEN = 'Open'
    HIGH = 'High'
    LOW = 'Low'
    CLOSE = 'Close'
    VOLUME = 'Volume'
    
    @staticmethod
    def LST_PRICE():
        return([COL.OPEN, COL.HIGH, COL.LOW, COL.CLOSE])

    @staticmethod
    def LST_ALL():
        return([COL.DATE, COL.OPEN, COL.HIGH, COL.LOW, COL.CLOSE, COL.VOLUME])

    @staticmethod
    def LST():
        return([COL.OPEN, COL.HIGH, COL.LOW, COL.CLOSE, COL.VOLUME])

class RemoteDataError(PandasError, IOError):
    pass

class SymbolWarning(UserWarning):
    pass

DATETIME_START_DEFAULT = datetime.datetime(2010, 1, 1)

def _sanitize_dates(start_date, end_date):
    from pandas.core.datetools import to_datetime
    start_date = to_datetime(start_date)
    end_date = to_datetime(end_date)
    if start_date is None:
        start_date = DATETIME_START_DEFAULT
    if end_date is None:
        end_date = datetime.datetime.today()
    return start_date, end_date

def _get_dates(i, *args, **kwargs):
    try:
        start_date = kwargs['start_date']
    except:
        try:
            start_date = args[i]
        except:
            start_date = None

    try:
        end_date = kwargs['end_date']
    except:
        try:
            end_date = args[i+1]
        except:
            end_date = None

    start_date, end_date = _sanitize_dates(start_date, end_date)

    return(start_date, end_date)

def to_float(x):
    try:
        return(float(x))
    except:
        return(np.nan)

def to_int(x):
    try:
        return(int(x))
    except:
        return(np.nan)
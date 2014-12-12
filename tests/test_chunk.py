#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from chunk import *
from chunk import _in_chunks
import math

def chunks_number(start, end, period, chunksize):
    """
    Return number of chunks for a given period
    """
    try:
        return(int(math.ceil((end-start).total_seconds()/(period.total_seconds()*chunksize))))
    except:
        return(1)

def chunks_period(start, end, period, chunksize):
    """
    Return period of a chunk
    """
    try:
        return(chunksize*period)
    except:
        return(datetime.timedelta(0))

def test_chunks_start_end_date():
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2011, 6, 1)
    period = datetime.timedelta(days=1)
    chunksize = 100

    n = chunks_number(start, end, period, chunksize)

    for i, (dt1, dt2) in enumerate(gen_chunks_start_end_date(start, end, period, chunksize)):
        td = dt2 - dt1
        print(i, dt1, dt2, td)
        td_chunks_period = chunks_period(start, end, period, chunksize)
        
        if i!=n-1:
            assert(td==td_chunks_period)
        else:
            assert(td<=td_chunks_period)
        assert(td<=chunksize*period)

def test_chunk_in_chunks():
    lst =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
    lst_chunks = _in_chunks(lst, 3)
    for chunk in lst_chunks:
        print(chunk)

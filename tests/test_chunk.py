#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from chunk import *
import math

def chunks(start, end, period, chunksize):
    try:
        return(int(math.ceil((end-start).total_seconds()/(period.total_seconds()*chunksize))))
    except:
        return(1)

def chunks_period(start, end, period, chunksize):
    try:
        return(chunksize*period)
    except:
        return(datetime.timedelta(0))

def test_chunk():
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2011, 6, 1)
    period = datetime.timedelta(days=1)
    chunksize = 0

    nb_chunks = chunks(start, end, period, chunksize)

    for i, (dt1, dt2, td) in enumerate(gen_date(start, end, period, chunksize)):
        print(i, dt1, dt2, td)
        td_chunks_period = chunks_period(start, end, period, chunksize)
        if i!=nb_chunks-1:
            assert(td==td_chunks_period)
        else:
            assert(td<=td_chunks_period)
        #assert(td<=chunksize*period)

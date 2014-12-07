#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from chunk import *
import math

def test_chunk():
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2011, 6, 1)
    period = datetime.timedelta(days=1)
    chunksize = 2

    chunks = int(math.ceil((end-start).total_seconds()/(period.total_seconds()*chunksize)))

    for i, (dt1, dt2, td) in enumerate(gen_date(start, end, period, chunksize)):
        print(i, dt1, dt2, td)
        if i!=chunks-1:
            assert(td==chunksize*period)
        else:
            assert(td<=chunksize*period)

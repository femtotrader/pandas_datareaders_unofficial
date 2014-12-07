#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from chunk import *

def test_chunk():
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2011, 6, 1)
    period = datetime.timedelta(days=1)
    chunksize = 10
    for (dt1, dt2, td) in gen_date(start, end, period, chunksize):
        print(dt1, dt2, td)

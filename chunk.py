#!/usr/bin/env python
# -*- coding: utf-8 -*-

def gen_date(start, end, period, chunksize):
    offset = 0

    dt = start

    try:
        if chunksize>0:
            while True:
                dt1 = start + offset * period
                dt2 = dt1 + chunksize * period
                if dt2>=end:
                    dt2 = end
                    yield(dt1, dt2, dt2-dt1)
                    break
                yield(dt1, dt2, dt2-dt1)
                offset += chunksize
        else:
            yield(start, end, end-start)
    except:
        yield(start, end, end-start)

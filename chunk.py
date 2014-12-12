#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

def gen_chunks_start_end_date(start, end, period, chunksize):
    """
    Generator which returns start, end date for each chunk
    """
    offset = 0

    dt = start

    try:
        if chunksize>0:
            while True:
                dt1 = start + offset * period
                dt2 = dt1 + chunksize * period
                if dt2>=end:
                    dt2 = end
                    yield(dt1, dt2)
                    break
                yield(dt1, dt2)
                offset += chunksize
        else:
            yield(start, end)
    except:
        yield(start, end)


def _in_chunks(seq, size):
    """
    Return sequence in 'chunks' of size defined by size
    """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


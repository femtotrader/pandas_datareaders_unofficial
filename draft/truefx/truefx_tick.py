#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_cache
import datetime
import pandas as pd
from datetime import timedelta

import pandas as pd
from pandas.io.common import ZipFile
from pandas.compat import BytesIO, StringIO, PY2

def main():
    expire_after = timedelta(days=1)
    if PY2:
        filename = 'cache_py2'    
    else:
        filename = 'cache'
    session = requests_cache.CachedSession(cache_name=filename, expire_after=expire_after)

    dt = pd.to_datetime("2014-01-01")
    symbol = "AUD/USD"
    symbol = symbol.replace("/", "").upper()
    year = dt.year
    month = dt.month
    month_name = datetime.datetime(year=1970, month=month, day=1).strftime('%B').upper()
    #url = "http://www.truefx.com/dev/data/2014/JANUARY-2014/AUDUSD-2014-01.zip"
    url = "http://www.truefx.com/dev/data/{year:04d}/{month_name}-{year:04d}/{symbol}-{year:04d}-{month:02d}.zip".format(year=year, month=month, symbol=symbol, month_name=month_name)
    response = session.get(url)
    zip_data = BytesIO(response.content)
    filename = "{symbol}-{year:04d}-{month:02d}.csv".format(year=year, month=month, symbol=symbol)

    with ZipFile(zip_data, 'r') as zf:
        #filename = zf.namelist()[0]
        zfile = zf.open(filename)
        #print(zfile)
        #(symb, dt, ask, bid) = zfile.read().split(',')        
        #print(zfile.__dict__)
        data = zfile.readlines()
        #df = pd.read_csv(zfile._fileobj)  # ToFix: can't make it work correctly

    #return
    df = pd.DataFrame(data)
    #df = df[:100] # just for test
    df[0] = df[0].str.decode('utf8')
    df[0] = df[0].str.replace('\n', '')
    df[0] = df[0].map(lambda s: s.split(','))
    df['Symbol'] = df[0].map(lambda t: t[0])
    df['Date'] = df[0].map(lambda t: pd.to_datetime(t[1]))
    df['Bid'] = df[0].map(lambda t: t[2]).astype(float)
    df['Ask'] = df[0].map(lambda t: t[3]).astype(float)
    del df[0]
    df = df.set_index('Date')
    print(df)

if __name__ == "__main__":
    main()

Pandas DataReaders with support of requests and requests-cache

[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/femtotrader/pandas_datareaders?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## What is it ?
[**pandas**](http://pandas.pydata.org/) is a Python package providing fast, flexible, and expressive data
structures designed to make working with "relational" or "labeled" data both
easy and intuitive.

DataReaders are objects to fetch data from remote source (Google Finance, Yahoo Finance, FRED, FamaFrench, World Bank...)
see http://pandas.pydata.org/pandas-docs/stable/remote_data.html

This project is an unofficial rewrite of DataReaders using [requests](http://www.python-requests.org/) also called "HTTP for Humans". But it can be easy to use classic `urlopen` using this code.

see https://github.com/pydata/pandas/issues/8713

Thanks to [requests-cache](https://readthedocs.org/projects/requests-cache/) we can now use SQLite as cache db to avoid too much requests to remote servers.

    import requests_cache
    expire_after = 60*5 # seconds
    filename = 'req_cache'
    requests_cache.install_cache(filename, backend='sqlite', expire_after=expire_after)
    
    symbol = ["GOOG", "AAPL", "MSFT"]
    end_date = datetime.datetime.now()
    num_days = 200
    start_date = end_date - datetime.timedelta(days=num_days)
    data = MyDataReader("GoogleFinanceDaily").get(symbol, start_date, end_date)
    print(data)

This is still very experimental. Not every DataReaders are functionnal.

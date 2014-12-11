Pandas DataReaders with support of `requests` and `requests-cache`

[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/femtotrader/pandas_datareaders?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![status](https://sourcegraph.com/api/repos/github.com/femtotrader/pandas_datareaders/.badges/status.png)](https://sourcegraph.com/github.com/femtotrader/pandas_datareaders)

## What is it ?
[**pandas**](http://pandas.pydata.org/) is a Python package providing fast, flexible, and expressive data
structures designed to make working with "relational" or "labeled" data both
easy and intuitive.

DataReaders are objects to fetch data from remote source:

* [Google Finance](https://www.google.com/finance)
* [Yahoo Finance](https://finance.yahoo.com)
* [Federal Reserve Economic Data - FRED - St. Louis Fed](http://research.stlouisfed.org/fred2/)
* [Fama-French](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
* [World Bank](http://data.worldbank.org/)
* ...


see http://pandas.pydata.org/pandas-docs/stable/remote_data.html

This project is an unofficial rewrite of DataReaders using [requests](http://www.python-requests.org/) also called "HTTP for Humans". But it can be easy to use classic `urlopen` using this code.

see https://github.com/pydata/pandas/issues/8713

Thanks to [requests-cache](https://readthedocs.org/projects/requests-cache/) we can now use [SQLite](http://www.sqlite.org/), [mongoDB](http://www.mongodb.org/), [Redis](http://redis.io/) or memory as cache database (backend) and expiration time to avoid too much requests to remote servers (and speed-up execution of sprits when they are run several times).

    expire_after = 60*5 # seconds - 0: no cache - None: no cache expiration
    
    symbol = ["GOOG", "AAPL", "MSFT"]
    end_date = datetime.datetime.now()
    num_days = 200
    start_date = end_date - datetime.timedelta(days=num_days)
    data = MyDataReader("GoogleFinanceDaily", expire_after=expire_after).get(symbol, start_date, end_date)
    print(data)

This is still very experimental. Not every DataReaders are functional.

Pandas DataReaders with support of [`requests`](http://www.python-requests.org/) and [`requests-cache`](http://requests-cache.readthedocs.org/)

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/femtotrader/pandas_datareaders?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![status](https://sourcegraph.com/api/repos/github.com/femtotrader/pandas_datareaders/.badges/status.png)](https://sourcegraph.com/github.com/femtotrader/pandas_datareaders)

[![Documentation Status](https://readthedocs.org/projects/pandas-datareaders/badge/?version=latest)](https://readthedocs.org/projects/pandas-datareaders/?badge=latest)

[![Build Status](https://travis-ci.org/femtotrader/pandas_datareaders.svg)](https://travis-ci.org/femtotrader/pandas_datareaders)

## What is it ?
[**pandas**](http://pandas.pydata.org/) is a Python package providing fast, flexible, and expressive data
structures designed to make working with "relational" or "labeled" data both
easy and intuitive.

DataReaders are objects to fetch data from remote source:

* [Google Finance](https://www.google.com/finance) (daily, intraday, options)
* [Yahoo Finance](https://finance.yahoo.com) (daily, quotes, options)
* [Federal Reserve Economic Data - FRED - St. Louis Fed](http://research.stlouisfed.org/fred2/)
* [Fama-French](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
* [World Bank](http://data.worldbank.org/)
* ...


see [pandas-docs / remote data](http://pandas.pydata.org/pandas-docs/stable/remote_data.html)

This project is an unofficial rewrite of DataReaders using [requests](http://www.python-requests.org/) also called "HTTP for Humans". But it can be easy to use classic `urlopen` using this code.

see [pandas/issues/8713](https://github.com/pydata/pandas/issues/8713)

Thanks to [requests-cache](http://requests-cache.readthedocs.org/) 
we can now use [SQLite](http://www.sqlite.org/), [mongoDB](http://www.mongodb.org/), 
[Redis](http://redis.io/) or memory as cache database (backend) and expiration time 
to avoid too much requests to remote servers 
(and speed-up execution of sprits when they are run several times). 
It make also possible to use some remote API calls offline (if same query was performed before).

    from pandas_datareaders.datareader import DataReader
    import datetime

    expire_after = 60*60 # seconds - 0: no cache - None: no cache expiration
    
    symbol = ["GOOG", "AAPL", "MSFT"]
    end_date = datetime.datetime.now()
    num_days = 200
    start_date = end_date - datetime.timedelta(days=num_days)
    data = DataReader("GoogleFinanceDaily", expire_after=expire_after).get(symbol, start_date, end_date)
    print(data)

It should return a [Pandas Panel](http://pandas.pydata.org/pandas-docs/dev/dsintro.html#panel) with OHLCV data like:

    <class 'pandas.core.panel.Panel'>
    Dimensions: 3 (items) x 141 (major_axis) x 5 (minor_axis)
    Items axis: AAPL to MSFT
    Major_axis axis: 2014-05-27 00:00:00 to 2014-12-12 00:00:00
    Minor_axis axis: Open to Volume

We can get a [Pandas DataFrame](http://pandas.pydata.org/pandas-docs/dev/dsintro.html#dataframe) with OHLCV data of "GOOG" using:

    print(data["GOOG"])

It should display:

                  Open    High     Low   Close   Volume
    Date
    2014-05-27  556.00  566.00  554.35  565.95  2100298
    2014-05-28  564.57  567.84  561.00  561.68  1647717
    2014-05-29  563.35  564.00  558.71  560.08  1350657
    2014-05-30  560.80  561.35  555.91  559.89  1766794
    2014-06-02  560.70  560.90  545.73  553.93  1434989
    ...            ...     ...     ...     ...      ...
    2014-12-08  527.13  531.00  523.79  526.98  2327127
    2014-12-09  522.14  534.19  520.50  533.37  1871268
    2014-12-10  533.08  536.33  525.56  526.06  1716835
    2014-12-11  527.80  533.92  527.10  528.34  1610964
    2014-12-12  523.51  528.50  518.66  518.66  1989117

    [141 rows x 5 columns]


Caution! This project is still experimental.

## Links
* Documentation can be found at [Read The Docs](http://pandas-datareaders.readthedocs.org/) ;
* Source code and issue tracking can be found at [GitHub](https://github.com/femtotrader/pandas_datareaders).

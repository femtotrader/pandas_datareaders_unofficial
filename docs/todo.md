* Doc
    * Write doc
    * see Read The Docs <https://readthedocs.org/>
    * Sphinx (reStructuredText) or MkDocs <http://www.mkdocs.org/> (Markdown)
    * One file per DataReader
    * Custom :
 
See code:

    from pandas_datareaders.datareaders.base import DataReaderBase
    import pandas as pd
    import json
    from StringIO import StringIO
    dr = DataReaderBase(expire_after=60*60)
    BASE_URL = 'http://openexchangerates.org/api'
    endpoint = '/latest.json'
    url = BASE_URL + endpoint
    params = {
        'app_id': ''
    }
    response = dr.session.get(url, params=params)
    raw_data = response.text # or .content if binary data is expected
    data = json.loads(raw_data)
    ...


* Create pip package
    * https://pypi.python.org/pypi

* Yahoo Options
    * current version is using lxml to parse web page
    * maybe there is better to do (YQL ?)

* Yahoo Quotes
    * add other codes as parameter

* Yahoo Query Language YQL
    * <https://developer.yahoo.com/yql/>
    * <https://github.com/pydata/pandas/issues/7104>
    * <https://github.com/femtotrader/StockScraper/blob/master/stockretriever.py>
    * <https://www.datatables.org/>
    * <https://github.com/project-fondue/python-yql> (see forks)
    * Yahoo Finance via YQL
      * <http://www.jarloo.com/get-near-real-time-stock-data-from-yahoo-finance/>
      * <http://www.jarloo.com/get-yahoo-finance-api-data-via-yql/>
      * <http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22AAPL%22)&env=store://datatables.org/alltableswithkeys&format=json>
      * <http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Ffinance.yahoo.com%2Fq%2Fop%3Fs%3DC%26m%3D2011-02%22%20and%20xpath%3D%22%2F%2Ftable%5B%40class%3D%27yfnc_datamodoutline1%27%5D%2Ftr%2Ftd%2Ftable%2Ftr%5Btd%5B%40class%3D%27yfnc_h%27%20or%20%40class%3D%27yfnc_tabledata1%27%5D%5D%22&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&format=json>

* use chunksize (when several symbols or when large number of data for a given symbol)

* Original Pandas DataReader
    * Google Analytics

* Other data provider to consider

    * EOD Data <http://www.eoddata.com/download.aspx>
    * BATS
        * <http://www.batstrading.com/market_data/symbol_listing/xml/>
        * or <http://www.batstrading.com/market_data/symbol_listing/csv/>
    * CBOE - Option Chain Download
        * <http://www.cboe.com/DelayedQuote/QuoteTableDownload.aspx>
    * Quandl
        * <https://github.com/quandl/Python/>
        * convert to requests / requests-cache

    * OpenExchangeRates
        * <http://openexchangerates.org/api/latest.json?app_id=...>

    * TrueFX

* Continuous Integration

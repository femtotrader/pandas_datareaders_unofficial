* pb unzip memory FamaFrench

* WorldBank - class

* _get_multi for FRED DataReader

  try to share the code in DataReaderBase
  if we get a serie when we ask data for a symbol,
  for several symbols, we must return a dataframe (this is the case for FRED)

  if we get a dataframe when we ask data for a symbol
  for several symbols, we must return a Panel (this is the case for Google or Yahoo Finance Daily)

* Yahoo Options
  current version is using lxml to parse web page
  maybe there is better to do (YQL ?)

* Google Options
  http://www.google.com/finance/option_chain?q=AAPL&expd=4&expm=4&expy=2014&output=json
  see https://github.com/makmac213/python-google-option-chain
  see draft/gopt.py http://www.drtomstarke.com/index.php/option-chains-from-google-finance-api

* Yahoo Quotes

* Yahoo Query Language YQL

  https://developer.yahoo.com/yql/
  
  https://github.com/pydata/pandas/issues/7104
  
  https://github.com/femtotrader/StockScraper/blob/master/stockretriever.py
  
  https://www.datatables.org/
  
  https://github.com/project-fondue/python-yql (see forks)

Yahoo Finance via YQL
http://www.jarloo.com/get-near-real-time-stock-data-from-yahoo-finance/
http://www.jarloo.com/get-yahoo-finance-api-data-via-yql/
http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22AAPL%22)&env=store://datatables.org/alltableswithkeys&format=json
http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Ffinance.yahoo.com%2Fq%2Fop%3Fs%3DC%26m%3D2011-02%22%20and%20xpath%3D%22%2F%2Ftable%5B%40class%3D%27yfnc_datamodoutline1%27%5D%2Ftr%2Ftd%2Ftable%2Ftr%5Btd%5B%40class%3D%27yfnc_h%27%20or%20%40class%3D%27yfnc_tabledata1%27%5D%5D%22&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&format=json

* use chunksize

* CBOE - Option Chain Download
  http://www.cboe.com/DelayedQuote/QuoteTableDownload.aspx

* Fix caching mechanism using requests_cache monkey patch method
and my own requests Session (RequestsSessionWithLog)
for now I'm using RequestsCachedSessionWithLog and I'm passing paramaters
to DataReaders


* Other data provider to consider
http://www.eoddata.com/download.aspx

http://www.batstrading.com/market_data/symbol_listing/xml/
ou http://www.batstrading.com/market_data/symbol_listing/csv/

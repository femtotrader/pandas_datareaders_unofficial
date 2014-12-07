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

* Yahoo Quotes

* Yahoo Query Language YQL

  https://developer.yahoo.com/yql/
  
  https://github.com/pydata/pandas/issues/7104
  
  https://github.com/femtotrader/StockScraper/blob/master/stockretriever.py
  
  https://www.datatables.org/
  
  https://github.com/project-fondue/python-yql (see forks)


* use chunsize

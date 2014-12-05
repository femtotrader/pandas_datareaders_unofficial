* pb unzip memory FamaFrench

* WorldBank - class

* _get_multi for FRED DataReader

  try to share the code in DataReaderBase
  if we get a serie when we ask data for a symbol,
  for several symbols, we must return a dataframe (this is the case for FRED)

  if we get a dataframe when we ask data for a symbol
  for several symbols, we must return a Panel (this is the case for Google or Yahoo Finance Daily)

* Yahoo Options
* Yahoo Quotes

* Yahoo Query Language YQL
  https://developer.yahoo.com/yql/
  https://github.com/pydata/pandas/issues/7104
  https://github.com/femtotrader/StockScraper/blob/master/stockretriever.py
  https://www.datatables.org/
  https://github.com/project-fondue/python-yql (see forks)

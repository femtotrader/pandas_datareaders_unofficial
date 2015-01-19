#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import DataReaderBase
from ..tools import COL, _get_dates
import pandas as pd
from six.moves import cStringIO as StringIO
import logging
import traceback
import pandas.compat as compat
from collections import defaultdict

class DataReaderYahooFinanceQuotes(DataReaderBase):
    """
    DataReader to fetch data from Yahoo Finance Quotes
    """

    _yahoo_codes = {'symbol': 's', 'last': 'l1', 'change_pct': 'p2', 'PE': 'r',
                'time': 't1', 'short_ratio': 's7'}

    _YAHOO_QUOTE_URL = 'http://finance.yahoo.com/d/quotes.csv?'
    BASE_URL = 'http://finance.yahoo.com'

    def init(self, *args, **kwargs):
        pass

    def _get_one(self, symbol, *args, **kwargs):
        """
        Get current Yahoo Quote for a symbol
        Returns a DataFrame
        """
        
        # ['symbol', 'last', 'change_pct', 'PE', 'time', 'short_ratio']
        # for codes see: http://www.gummy-stuff.org/Yahoo-data.htm
        request = ''.join(compat.itervalues(self._yahoo_codes))  # code request string
        header = list(self._yahoo_codes.keys())
        
        data = defaultdict(list)
        
        url = self._url('/d/quotes.csv')
        params = {
            's': symbol,
            'f': request
        }
        
        response = self.session.get(url, params=params, stream=True)
        
        for line in response.iter_lines():
            fields = line.decode('utf-8').strip().split(',')
            for i, field in enumerate(fields):
                if field[-2:] == '%"':
                    v = float(field.strip('"%'))
                elif field[0] == '"':
                    v = field.strip('"')
                else:
                    try:
                        v = float(field)
                    except ValueError:
                        v = field
                data[header[i]].append(v)

        idx = data.pop('symbol')
        return pd.DataFrame(data, index=idx)

    def _get_multi(self, symbols, *args, **kwargs):
        """
        Get current Yahoo Quote for several symbols
        Returns a DataFrame
        """
        if isinstance(symbols, compat.string_types):
            sym_list = symbols
        else:
            sym_list = '+'.join(symbols)
        return(self._get_one(sym_list, *args, **kwargs))



    """

        params = {
            's': symbol,
            'l1': last,
            'p2': change_pct,
            'r': PE,
            't1': time,
            's7': short_ratio
        }


_YAHOO_QUOTE_URL = 'http://finance.yahoo.com/d/quotes.csv?'
http://www.gummy-stuff.org/Yahoo-data.htm
http://www.jarloo.com/yahoo_finance/
    """

#def get_quote_yahoo(symbols):
    """
    if isinstance(symbols, compat.string_types):
        sym_list = symbols
    else:
        sym_list = '+'.join(symbols)

    """


"""
http://finance.yahoo.com/d/quotes.csv?s=AAPL+GOOG+MSFT&f=nab

url = self._url('/d/quotes.csv')
params = {
    's': symb,
    'f': form
}

Financial Data you can Download
Pricing	Dividends
a: Ask	y: Dividend Yield
b: Bid	d: Dividend per Share
b2: Ask (Realtime)	r1: Dividend Pay Date
b3: Bid (Realtime)	q: Ex-Dividend Date
p: Previous Close	
o: Open	
Date
c1: Change	d1: Last Trade Date
c: Change & Percent Change	d2: Trade Date
c6: Change (Realtime)	t1: Last Trade Time
k2: Change Percent (Realtime)	
p2: Change in Percent	
Averages
c8: After Hours Change (Realtime)	m5: Change From 200 Day Moving Average
c3: Commission	m6: Percent Change From 200 Day Moving Average
g: Day’s Low	m7: Change From 50 Day Moving Average
h: Day’s High	m8: Percent Change From 50 Day Moving Average
k1: Last Trade (Realtime) With Time	m3: 50 Day Moving Average
l: Last Trade (With Time)	m4: 200 Day Moving Average
l1: Last Trade (Price Only)	
t8: 1 yr Target Price	
Misc
w1: Day’s Value Change	g1: Holdings Gain Percent
w4: Day’s Value Change (Realtime)	g3: Annualized Gain
p1: Price Paid	g4: Holdings Gain
m: Day’s Range	g5: Holdings Gain Percent (Realtime)
m2: Day’s Range (Realtime)	g6: Holdings Gain (Realtime)
52 Week Pricing	Symbol Info
k: 52 Week High	v: More Info
j: 52 week Low	j1: Market Capitalization
j5: Change From 52 Week Low	j3: Market Cap (Realtime)
k4: Change From 52 week High	f6: Float Shares
j6: Percent Change From 52 week Low	n: Name
k5: Percent Change From 52 week High	n4: Notes
w: 52 week Range	s: Symbol
s1: Shares Owned
x: Stock Exchange
j2: Shares Outstanding
Volume
v: Volume	
a5: Ask Size	
b6: Bid Size	Misc
k3: Last Trade Size	t7: Ticker Trend
a2: Average Daily Volume	t6: Trade Links
i5: Order Book (Realtime)
Ratios	l2: High Limit
e: Earnings per Share	l3: Low Limit
e7: EPS Estimate Current Year	v1: Holdings Value
e8: EPS Estimate Next Year	v7: Holdings Value (Realtime)
e9: EPS Estimate Next Quarter	s6 Revenue
b4: Book Value	
j4: EBITDA	
p5: Price / Sales	
p6: Price / Book	
r: P/E Ratio	
r2: P/E Ratio (Realtime)	
r5: PEG Ratio	
r6: Price / EPS Estimate Current Year	
r7: Price / EPS Estimate Next Year	
s7: Short Ratio	





Country	Exchange	Suffix	Delay	Data Provider
United States of America	American Stock Exchange	N/A	15 min	Direct from Exchange
United States of America	BATS Exchange	N/A	Real-time	Direct from Exchange
United States of America	Chicago Board of Trade	.CBT	10 min	Interactive Data Real-Time Services
United States of America	Chicago Mercantile Exchange	.CME	10 min	Interactive Data Real-Time Services
United States of America	Dow Jones Indexes	N/A	Real-time	Interactive Data Real-Time Services
United States of America	NASDAQ Stock Exchange	N/A	15 min	Direct from Exchange
United States of America	New York Board of Trade	.NYB	30 min	Interactive Data Real-Time Services
United States of America	New York Commodities Exchange	.CMX	30 min	Interactive Data Real-Time Services
United States of America	New York Mercantile Exchange	.NYM	30 min	Interactive Data Real-Time Services
United States of America	New York Stock Exchange	N/A	15 min	Direct from Exchange
United States of America	OTC Bulletin Board Market	.OB	20 min	Direct from Exchange
United States of America	Pink Sheets	.PK	15 min	Direct from Exchange
United States of America	S & P Indices	N/A	Real-time	Interactive Data Real-Time Services
Argentina	Buenos Aires Stock Exchange	.BA	30 min	Interactive Data Real-Time Services
Austria	Vienna Stock Exchange	.VI	15 min	Telekurs
Australia	Australian Stock Exchange	.AX	20 min	Interactive Data Real-Time Services
Belgium	Brussels Stocks	.BR	15 min	
Brazil	BOVESPA – Sao Paolo Stock Exchange	.SA	15 min	Interactive Data Real-Time Services
Canada	Toronto Stock Exchange	.TO	15 min	Interactive Data Real-Time Services
Canada	TSX Venture Exchange	.V	15 min	Interactive Data Real-Time Services
Chile	Santiago Stock Exchange	.SN	15 min	Interactive Data Real-Time Services
China	Shanghai Stock Exchange	.SS	30 min	Interactive Data Real-Time Services
China	Shenzhen Stock Exchange	.SZ	30 min	Interactive Data Real-Time Services
Denmark	Copenhagen Stock Exchange	.CO	15 min	Telekurs
France	Euronext	.NX	15 min	Telekurs
France	Paris Stock Exchange	.PA	15 min	Telekurs
Germany	Berlin Stock Exchange	.BE	15 min	Telekurs
Germany	Bremen Stock Exchange	.BM	15 min	Telekurs
Germany	Dusseldorf Stock Exchange	.DU	15 min	Telekurs
Germany	Frankfurt Stock Exchange	.F	15 min	Telekurs
Germany	Hamburg Stock Exchange	.HM	15 min	Telekurs
Germany	Hanover Stock Exchange	.HA	15 min	Telekurs
Germany	Munich Stock Exchange	.MU	15 min	Telekurs
Germany	Stuttgart Stock Exchange	.SG	15 min	Telekurs
Germany	XETRA Stock Exchange	.DE	15 min	Telekurs
Hong Kong	Hong Kong Stock Exchange	.HK	15 min	Interactive Data Real-Time Services
India	Bombay Stock Exchange	.BO	15 min	Interactive Data Real-Time Services
India	National Stock Exchange of India	.NS	15 min	National Stock Exchange of India
Indonesia	Jakarta Stock Exchange	.JK	10 min	Interactive Data Real-Time Services
Israel	Tel Aviv Stock Exchange	.TA	20 min	Telekurs
Italy	Milan Stock Exchange	.MI	20 min	Telekurs
Japan	Nikkei Indices	N/A	30 min	Interactive Data Real-Time Services
Mexico	Mexico Stock Exchange	.MX	20 min	Telekurs
Netherlands	Amsterdam Stock Exchange	.AS	15 min	Telekurs
New Zealand	New Zealand Stock Exchange	.NZ	20 min	Interactive Data Real-Time Services
Norway	Oslo Stock Exchange	.OL	15 min	Telekurs
Portugal	Lisbon Stocks	.LS	15 min	
Singapore	Singapore Stock Exchange	.SI	20 min	Interactive Data Real-Time Services
South Korea	Korea Stock Exchange	.KS	20 min	Interactive Data Real-Time Services
South Korea	KOSDAQ	.KQ	20 min	Interactive Data Real-Time Services
Spain	Barcelona Stock Exchange	.BC	15 min	Telekurs
Spain	Bilbao Stock Exchange	.BI	15 min	Telekurs
Spain	Madrid Fixed Income Market	.MF	15 min	Telekurs
Spain	Madrid SE C.A.T.S.	.MC	15 min	Telekurs
Spain	Madrid Stock Exchange	.MA	15 min	Telekurs
Sweden	Stockholm Stock Exchange	.ST	15 min	Telekurs
Switzerland	Swiss Exchange	.SW	30 min	Telekurs
Taiwan	Taiwan OTC Exchange	.TWO	20 min	Interactive Data Real-Time Services
Taiwan	Taiwan Stock Exchange	.TW	20 min	Interactive Data Real-Time Services
United Kingdom	FTSE Indices	N/A	15 min	Telekurs
United Kingdom	London Stock Exchange	.L	20 min	Telekurs


"""
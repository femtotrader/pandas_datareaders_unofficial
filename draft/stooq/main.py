#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import click

import os

import requests
import requests_cache

import logging
import traceback

import pandas as pd
from pandas.io.common import ZipFile
from pandas.tseries.frequencies import to_offset

import datetime
from datetime import timedelta

from clint.textui import progress

#from six.moves import cStringIO as StringIO
import pandas.compat as compat

"""
from main import conv_resol, conv_geo, download_data, get_data
expire_after = timedelta(days=1)
session = requests_cache.CachedSession(cache_name='cache', expire_after=expire_after)
panel = get_data('poland', 'H', session)
"""

def conv_resol(resolution):
    d = {
        to_offset('5Min'): '5',
        to_offset('1H'): 'h',
        to_offset('D'): 'd',
    }
    try:
        return(d[to_offset(resolution)])
    except:
        logging.error(traceback.format_exc())
        logging.warning("conv_resol returns '%s'" % resolution)
        resolution = resolution.lower()
        return(resolution)

def conv_geo(geo):
    d_geo = {
        'world': 'world',
        'u.s.': 'us',
        'japan': 'jp',
        'germany': 'de',
        'poland': 'pl',
        'hungary': 'hu',
        'macroeconomy': 'macro',
        'all': 'all'
    }

    try:
        return(d_geo[geo.lower()])
    except:
        logging.error(traceback.format_exc())
        geo = geo.lower()
        logging.warning("conv_geo returns '%s'" % geo)
        return(geo)

def download_data(geo, resolution, session):    
    url = "http://s.stooq.com/db/h/{resolution}_{geo}_txt.zip".format(geo=geo, resolution=resolution)

    print("Request %r" % url)

    response = session.get(url, stream=True)
    #path = 'temp.tmp'
    #with open(path, 'wb') as f:
    #    total_length = int(response.headers.get('content-length'))
    #    for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
    #        if chunk:
    #            f.write(chunk)
    #            f.flush()

    total_length = int(response.headers.get('content-length'))
    for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
        pass

    return(response)

def get_data(geo, resolution, session):
    geo = conv_geo(geo)
    resolution = conv_resol(resolution)
    response = download_data(geo, resolution, session)
    logger.info("Request done")

    logger.info("Create stream file")
    zip_data = compat.BytesIO(response.content)

    logger.info("Creating a DataFrame per symbol")

    d = {}
    cols = None
    with ZipFile(zip_data, 'r') as zf:
        filelist = zf.filelist
        df_info = pd.DataFrame(filelist)
        df_info['filename'] = df_info[0].map(lambda x: x.filename)
        df_info['file_size'] = df_info[0].map(lambda x: x.file_size)
        df_info['date_time'] = df_info[0].map(lambda x: datetime.datetime(*x.date_time))
        del df_info[0]
        for zinfo in filelist:
            filename = zinfo.filename
            filename_short, filename_ext = os.path.splitext(filename)
            with zf.open(filename) as zfile:
                if filename_ext.lower() == '.txt':
                    file_exchange = filename.split('/')[3]
                    file_symbol = os.path.split(filename_short)[-1].upper()
                    #print("Building DataFrame for '%s' at '%s' from '%s'" % (file_symbol, file_exchange, filename))
                    if  zinfo.file_size>0:
                        try:
                            if resolution=='d':
                                df = pd.read_csv(zfile, parse_dates=0)
                            else:
                                df = pd.read_csv(zfile, parse_dates=[[0, 1]])
                                df = df.rename(columns={'Date_Time': 'Date'})
                            df = df.set_index('Date')
                            df['Exchange'] = file_exchange
                            d[file_symbol] = df
                            if cols is None:
                                cols = df.columns
                        except:
                            logger.error("Can't build DataFrame for '%s' at '%s' from '%s'" % (file_symbol, file_exchange, filename.replace(' ', '\ ')))
                            logger.error(traceback.format_exc())
                            d[file_symbol] = None
                            df['Exchange'] = file_exchange
                    else:
                        logger.error("Can't build DataFrame for '%s' at '%s' from '%s' (empty file)" % (file_symbol, file_exchange, filename.replace(' ', '\ ')))
                        d[file_symbol] = None
                        df['Exchange'] = file_exchange
    logger.info("Create Panel from DataFrame")
    panel = pd.Panel(d)
    panel = panel.transpose(2, 1, 0)
    panel.major_axis = panel.major_axis.map(lambda n: pd.to_datetime(str(n)))
    return(panel, df_info)

@click.command()
@click.option('--geo', default='HU', help='Geo')
@click.option('--resolution', default='D', help='resolution')
def main(geo, resolution):
    #geo, resolution = 'HU', 'D'
    expire_after = timedelta(days=1)
    session = requests_cache.CachedSession(cache_name='cache', expire_after=expire_after)
    panel, df_info = get_data(geo, resolution, session)
    print(panel)
    print(df_info)

if __name__ == "__main__":
    main()

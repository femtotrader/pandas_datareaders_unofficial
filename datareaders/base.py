#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from abc import ABCMeta, abstractmethod

try:
    import requests
except ImportError:
    _HAS_REQUESTS = False
else:
    _HAS_REQUESTS = True

try:
    import requests_cache
except ImportError:
    _HAS_REQUESTS_CACHE = False
else:
    _HAS_REQUESTS_CACHE = True


from cachecontrol import CacheControl

import logging
import traceback

from urllib import urlencode

import pandas as pd
from tools import RemoteDataError

#see http://requests-cache.readthedocs.org/en/latest/user_guide.html#usage
#cache_name='cache', backend=None, expire_after=None, allowable_codes=(200, ), allowable_methods=('GET', ), **backend_options

class RequestsSessionWithLog(requests.Session):
    #def __init__(self):
    #    super(RequestsSessionWithLog, self).__init__()

    def get(self, url, **kwargs):
        try:
            params = kwargs['params']
        except:
            params = {}
        if params=={}:
            logging.debug("Request to '%s'" % url)
        else:
            logging.debug("Request to '%s' with '%s' using '%s'" % (url, params, url+'?'+urlencode(params)))
        response = super(RequestsSessionWithLog, self).get(url, **kwargs)
        return(response)

class RequestsCachedSessionWithLog(requests_cache.CachedSession):
    def get(self, url, **kwargs):
        try:
            params = kwargs['params']
        except:
            params = {}
        if params=={}:
            logging.debug("Request to '%s'" % url)
        else:
            logging.debug("Request to '%s' with '%s' using '%s'" % (url, params, url+'?'+urlencode(params)))
        response = super(requests_cache.CachedSession, self).get(url, **kwargs)
        return(response)

class DataReaderBase(object):
    #__metaclass__ = ABCMeta

    MAX_RETRIES_DEFAULT = 3
    #PAUSE_DEFAULT = 0.001
    CHUNKSIZE_DEFAULT = 25

    BASE_URL = ""

    def __init__(self, *args, **kwargs):        
        try:
            cache_name = kwargs['cache_name']
        except:
            cache_name = 'cache'

        try:
            backend = kwargs['backend']
        except:
            backend = None

        try:
            expire_after = kwargs['expire_after']
        except:
            expire_after = 0 # 0: no cache - None: no cache expiration

        if not _HAS_REQUESTS:
            raise ImportError("requests not found, please install it")

        if expire_after==0:
            logging.debug("Requests without cache")
            self.session = RequestsSessionWithLog()
        else:
            if not _HAS_REQUESTS_CACHE:
                raise ImportError("requests_cache not found, please install it")
            logging.info("Installing cache '%s.sqlite' with expire_after=%s (seconds)" % (cache_name, expire_after))
            if expire_after is None:
                logging.warning("expire_after is None - no cache expiration!")
            self.session = RequestsCachedSessionWithLog(cache_name, backend, expire_after)

        try:
            self.max_retries = kwargs['max_retries']
        except:
            self.max_retries = self.MAX_RETRIES_DEFAULT

        try:
            self.chunksize = kwargs['chunksize']
        except:
            self.chunksize = self.CHUNKSIZE_DEFAULT

        a = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        b = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        self.session.mount('http://', a)
        self.session.mount('https://', b)

        self.init(*args, **kwargs)

    def get(self, name, *args, **kwargs):
        if isinstance(name, basestring):
            return(self._get_one(name, *args, **kwargs))
        else:
            return(self._get_multi(name, *args, **kwargs))

    #@abstractmethod
    def _get_one(self, name, *args, **kwargs):
        raise(NotImplementedError)

    def _get_multi_topanel(self, names, *args, **kwargs):
        d_data = {}
        lst_failed = []

        for name in names:
            try:
                d_data[name] = self._get_one(name, *args, **kwargs)
            except IOError:
                logging.warning("Failed to read symbol: {0!r}, replacing with 'NaN.".format(name))
                lst_failed.append(sym)

        try:
            if len(d_data) > 0 and len(lst_failed) > 0:
                df_na = d_data.values()[0].copy()
                df_na[:] = np.nan
                for name in lst_failed:
                    d_data[name] = df_na
            panel = pd.Panel(d_data)
            #panel = panel.transpose(2, 1, 0) or panel.swapaxes('items', 'minor')
            #panel = panel.swapaxes('items', 'minor')
            return(panel)
        except AttributeError:
            logging.error(traceback.format_exc())
            # cannot construct a panel with just 1D nans indicating no data
            raise RemoteDataError("No data fetched using "
                                  "{0!r}".format(type(self).__name__))

    def _get_multi_todict(self, names, *args, **kwargs):
        d_data = {}
        lst_failed = []

        for name in names:
            try:
                data_one = self._get_one(name, *args, **kwargs)
                d_data[name] = data_one
            except IOError:
                logging.warning("Failed to read symbol: {0!r}, replacing with 'NaN.".format(name))
                d_data[name] = None
                lst_failed.append(name)
        return(d_data)


    def _url(self, endpoint='/'):
        return(self.BASE_URL + endpoint)

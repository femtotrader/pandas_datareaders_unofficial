#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import traceback

from .base import DataReaderBase

import pandas as pd
import numpy as np

import tempfile

from pandas.io.common import ZipFile

from pandas.compat import(
    range, lmap, zip
)

from six.moves import cStringIO as StringIO

class DataReaderFamaFrench(DataReaderBase):
    """
    DataReader to fetch data from FamaFrench
    """

    def init(self, *args, **kwargs):
        self._get_multi = self._get_multi_todict

    def _get_one(self, name, *args, **kwargs):
        url = 'http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{name}.zip'\
            .format(name=name)

        response = self.session.get(url)
        raw = response.content # returns bytes (.text returns unicode ; .content returns byte)
        if response.status_code!=200:
            raise IOError("Failed to get the data. Check that {0!r} is "
                          "a valid FamaFrench dataset.".format(name))

        with tempfile.TemporaryFile() as tmpf:
            tmpf.write(raw)

            with ZipFile(tmpf, 'r') as zf:
                data = zf.open(zf.namelist()[0]).readlines()

        line_lengths = np.array(lmap(len, data))
        file_edges = np.where(line_lengths == 2)[0]

        datasets = {}
        edges = zip(file_edges + 1, file_edges[1:])
        for i, (left_edge, right_edge) in enumerate(edges):
            dataset = [d.split() for d in data[left_edge:right_edge]]
            if len(dataset) > 10:
                ncol_raw = np.array(lmap(len, dataset))
                ncol = np.median(ncol_raw)
                header_index = np.where(ncol_raw == ncol - 1)[0][-1]
                header = dataset[header_index]
                ds_header = dataset[header_index + 1:]
                # to ensure the header is unique
                header = ['{0} {1}'.format(j, hj) for j, hj in enumerate(header,
                                                                         start=1)]
                index = np.array([d[0] for d in ds_header], dtype=int)
                dataset = np.array([d[1:] for d in ds_header], dtype=float)
                datasets[i] = pd.DataFrame(dataset, index, columns=header)

        return datasets        

# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

STDIN = 0
STDOUT = 1


def read_data(fp):
    data = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        data += read
    return data


def write_data(fp, data):
    os.write(fp, data.encode('utf-8'))

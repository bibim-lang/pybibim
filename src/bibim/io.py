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
    # return data.decode('utf-8')  # todo: 왜인지 rpython에서 오류 생김. 수정할 것. stdin은 괜찮은데 runfile에서만 문제생김
    return data


def write_data(fp, data):
    os.write(fp, data.encode('utf-8'))

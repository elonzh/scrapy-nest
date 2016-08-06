# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import uniout
import json
import pprint
from school_info_spider import models

with open('../result.jsonlines', 'rb') as fp:
    for i in range(100):
        print('-' * 30, i)
        l = fp.readline()
        print (l)
        pprint.pprint(json.loads(l))

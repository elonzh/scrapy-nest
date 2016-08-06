# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
from . import items, models


class ItemStripPipeline(object):
    def process_item(self, item, spider):
        for k, v in item.items():
            if isinstance(v, basestring):
                item[k] = item[k].strip()
        return item


class NoneValuePipeline(object):
    def process_item(self, item, spider):
        for k, v in item.items():
            if isinstance(v, basestring) and (not v or v in ('暂无', '——', '暂无评级')):
                item[k] = None
        return item


class SerializerPipline(object):
    def serialize(self, item, keys, none_values=None, serializer=None):
        keys = keys if hasattr(keys, '__iter__') else (keys,)
        none_values = none_values if hasattr(none_values, '__iter__') else (none_values,)
        for k in keys:
            v = item[k]
            if not v or v in none_values:
                item[k] = None
            elif serializer:
                item[k] = serializer(v)

    def process_item(self, item, spider):
        if isinstance(item, items.RetrialAcceptingLineItem):
            keys = ('tp', 'politics', 'foreign_language', 'third_course', 'fourth_course')
            # 有分数格式不正确的情况
            # self.serialize(item, keys, '——', float)
            self.serialize(item, keys, '——')
        elif isinstance(item, items.AcceptanceRateItem):
            keys = ('plan', 'proposer', 'enrollment', 'acceptance_rate', 'push_avoid_unripe')
            self.serialize(item, keys, '暂无')
        elif isinstance(item, items.MajorItem):
            self.serialize(item, 'popularity', '暂无', int)
        elif isinstance(item, items.SchoolItem):
            keys = (
                'popularity', 'overall_rank', 'graduate_school_rank', 'academic_level_rank', 'academic_level_rank',
                'master_academic_degree_plan', 'master_professional_degree_plan', 'phd_academic_degree_plan',
                'phd_professional_degree_plan'
            )
            self.serialize(item, keys, '暂无', int)
            self.serialize(item, 'graduate_school_level', '暂无评级')
            self.serialize(item, 'star_level', '暂无', lambda v: v.count('★') or None)
        return item


# class DatabaseExportPipeline(object):
#     def process_item(self, item, spider):
#         session = models.DBSession()
#         if isinstance(item, items.SchoolItem):
#             obj = models.School(**item)
#         elif isinstance(item, items.MajorItem):
#             obj = models.Major(**item)
#         elif isinstance(item, items.SchoolMajorItem):
#             if not models.Major.query.get(item['major_code']):
#                 m = Major
#             obj = models.SchoolMajor(**item)
#         elif isinstance(item, items.RetrialAcceptingLineItem):
#             obj = models.RetrialAcceptingLine(**item)
#         elif isinstance(item, items.AcceptanceRateItem):
#             obj = models.AcceptanceRate(**item)
#         else:
#             raise TypeError(item)
#         session.add(obj)
#         session.commit()


class JsonLinesExportPipeline(object):
    fps = {}
    path = 'JsonLinesExport'

    def __init__(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        if spider.name == 'major' and isinstance(item, items.SchoolMajorItem):
            fp = self.fps['school_major']
        else:
            fp = self.fps[spider.name]
        line = json.dumps(dict(item), ensure_ascii=False) + os.linesep
        fp.write(line.encode('utf-8'))
        return item

    def open_spider(self, spider):
        name = spider.name
        self.fps[name] = open(os.path.join(self.path, name), 'wb')
        if name == 'major':
            name = 'school_major'
            self.fps[name] = self.fps[name] = open(os.path.join(self.path, name), 'wb')

    def close_spider(self, spider):
        name = spider.name
        fp = self.fps[name]
        fp.close()
        if name == 'major':
            name = 'school_major'
            fp = self.fps[name]
            fp.close()

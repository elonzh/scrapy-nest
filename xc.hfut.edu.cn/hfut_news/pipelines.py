# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from sys import exit
from db_create import DBSession, Post, Type


class HfutnewsPipeline(object):
    def process_item(self, item, spider):
        session = DBSession()
        try:
            post_type = Type(name=item["type"])
            news = Post(title=item["title"],
                        link=item["link"],
                        timestamp=item["timestamp"],
                        body=item["body"],
                        type=post_type)
            session.add(news)
            session.commit()
        except Exception as e:
            logging.error(e)
            session.rollback()
            session.close()
            exit()
        session.close()
        return item

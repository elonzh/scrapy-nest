# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import uniout
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.python import failure

from school_info_spider import spiders, models

configure_logging()
failure.startDebugMode()

process = CrawlerProcess(get_project_settings())
process.crawl(spiders.SchoolSpider)
process.crawl(spiders.MajorSpider)
process.crawl(spiders.RetrialAcceptingLineSpider)
process.crawl(spiders.AcceptanceRateSpider)
process.start()  # the script will block here until all crawling jobs are finished

# session = models.DBSession()
# with open(os.path.join('JsonLinesExport', spiders.SchoolSpider.name), 'rb') as fp:
#     for l in fp:
#         d = json.loads(l)
#         s = models.School(**d)
#         session.add(s)
# session.commit()
# with open(os.path.join('JsonLinesExport', spiders.MajorSpider.name), 'rb') as fp:
#     for l in fp:
#         d = json.loads(l)
#         s = models.Major(**d)
#         session.add(s)
# session.commit()
# with open(os.path.join('JsonLinesExport', spiders..name), 'rb') as fp:
#     for l in fp:
#         d = json.loads(l)
#         s = models.School(**d)
#         session.add(s)
# session.commit()
# with open(os.path.join('JsonLinesExport', spiders.SchoolSpider.name), 'rb') as fp:
#     for l in fp:
#         d = json.loads(l)
#         s = models.School(**d)
#         session.add(s)
# session.commit()

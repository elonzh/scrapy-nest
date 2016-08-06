# -*- coding: utf-8 -*-

# Scrapy settings for hfut_news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'hfut_news'

SPIDER_MODULES = ['hfut_news.spiders']
NEWSPIDER_MODULE = 'hfut_news.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hfut_news (+http://www.yourdomain.com)'

ITEM_PIPELINES = ['hfut_news.pipelines.HfutnewsPipeline']


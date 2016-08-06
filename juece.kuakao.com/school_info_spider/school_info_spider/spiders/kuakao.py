# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import scrapy
import urlparse
from ..items import MajorItem, SchoolMajorItem, RetrialAcceptingLineItem, AcceptanceRateItem, SchoolItem


def get_next_page_url(response):
    next_page_url_xpath = '//div[@class="recordPage"]//a[last()]/@href'
    next_page_url = response.selector.xpath(next_page_url_xpath).extract()
    next_page_url = next_page_url[0] if next_page_url else None
    return next_page_url if next_page_url != response.url else None


class MajorSpider(scrapy.Spider):
    """
    专业信息爬虫，返回 MajorItem 和 SchoolMajorItem
    """
    name = 'major'
    start_urls = (
        'http://juece.kuakao.com/index.php?m=yxk&c=school_search&a=sear_zy&page=1',
    )

    def parse(self, response):
        """
        @url http://juece.kuakao.com/index.php?m=yxk&c=school_search&a=sear_zy&page=1
        @returns requests 21 21
        @returns items 0 0
        """
        table = response.selector.xpath('//table[@id="rp_tab_x"]')
        trs = table.xpath('tbody//tr')
        keys = ('code', 'name', 'category', 'first_major', 'degree')
        for tr in trs:
            values = tr.xpath('.//td[position()<last()]').xpath('string(.)').extract()
            assert len(values) == len(keys)
            item = MajorItem(dict(zip(keys, values)))
            school_list_link = urlparse.urljoin(response.url, tr.xpath('./td[6]/a/@href').extract()[0])
            request = scrapy.Request(school_list_link, self.parse_school_major)
            request.meta['item'] = item
            yield request
        next_page_url = get_next_page_url(response)
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_school_major(self, response):
        item_for_popularity = response.meta.get('item')
        if item_for_popularity:
            # 专业人气
            item_for_popularity['popularity'] = response.selector.xpath(
                '/html/body/div[5]/div[1]/div[1]/div/div[1]/div[@class="topIndex"]/text()').extract()[0]
            yield item_for_popularity

        table = response.selector.xpath(
            '/html/body/div[5]/div[1]/div[2]/div[@class="recordTable setUpTable"]/table')
        trs = table.xpath('tbody//tr')
        for tr in trs:
            item = SchoolMajorItem()
            # 过了第一页就错了2B= =
            # item['code'] = item_for_popularity['code']
            item['year'] = tr.xpath('td[1]/text()').extract()[0]
            item['college'] = tr.xpath('td[4]/text()').extract()[0]
            school_major_link = urlparse.urljoin(response.url, tr.xpath('td[5]/a[1]/@href').extract()[0])
            yield scrapy.Request(school_major_link, self.parse_extra_school_major_info, meta=dict(item=item))
        next_page_url = get_next_page_url(response)
        if next_page_url:
            yield scrapy.Request(next_page_url, self.parse_school_major)

    def parse_extra_school_major_info(self, response):
        school_major_info_item = response.meta['item']
        msg = response.selector.xpath('/html/body/div[@class="showMsg"]/div[@class="content guery"]/text()').extract()
        if msg:
            del school_major_info_item
            self.logger.warning('Can\'t get extra major info of school. <URL %s>', response.url)
        else:
            school_major_info_item['major_code'] = response.selector.xpath(
                '/html/body/div[10]/div[@class="majorOpenCon clearfix finmajorCon mb20"]/h4/span/text()'
            ).extract()[0].strip('（）')
            school_major_info_item['school_code'] = response.selector.xpath(
                '/html/body/div[5]/div[2]/div[2]/div[1]/p[@class="schoolCode fl"]/text()'
            ).extract()[0].split('：')[1]
            table = response.selector.xpath(
                '/html/body/div[11]/div[1]/div[2]/div[3]/div[@class="subjectList enroDetai"]/table'
            )
            keys = ('research_direction', 'enrollment_plan', 'exam_course', 'reference', 'remarks')
            values = table.xpath('.//tr/td[2]').xpath('string(.)').extract()
            assert len(values) == len(keys)
            school_major_info_item.update(zip(keys, values))
            yield school_major_info_item


class RetrialAcceptingLineSpider(scrapy.Spider):
    """
    分数线爬虫，返回的 Item 包括招生年份，学校，学院，专业代码，专业名称，总分数线，政治分数线，外语分数线，第三科目分数线，第四科目分数线等字段
    """
    name = 'retrial_accepting_line'
    start_urls = (
        'http://juece.kuakao.com/index.php?m=yxk&c=school_search&a=sear_fsx&page=1',
    )

    def parse(self, response):
        """
        @url http://juece.kuakao.com/index.php?m=yxk&c=school_search&a=sear_fsx&page=1,
        @returns requests 1 1
        @returns items 20 20
        """
        table = response.selector.xpath('//table[@class="record_tab_x"]')
        # keys = table.xpath('thead/tr//td[position()<last()]/text()').extract()
        trs = table.xpath('tbody//tr')
        keys = ('year', 'school_name', 'school_college', 'major_code', 'major_name',
                'tp', 'politics', 'foreign_language', 'third_course', 'fourth_course')
        for tr in trs:
            values = tr.xpath('.//td[position()<last()]').xpath('string(.)').extract()
            assert len(values) == len(keys)
            item = RetrialAcceptingLineItem(zip(keys, values))
            yield item
        next_page_url = get_next_page_url(response)
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)


class AcceptanceRateSpider(scrapy.Spider):
    """
    报录比爬虫，返回的 Item 包括招生年份，学校，学院，专业代码，专业名称，计划人数，报考人数，录取人数，报录比，推免人数
    """
    name = 'acceptance_rate'
    start_urls = (
        'http://juece.kuakao.com/index.php?m=yxk&c=school_search&a=sear_blb&page=1',
    )

    def parse(self, response):
        """
        @url http://juece.kuakao.com/index.php?m=yxk&c=school_search&a=sear_blb&page=1
        @returns requests 1 1
        @returns items 20 20
        """
        table = response.selector.xpath('//table[@class="record_tab_x"]')
        # keys = table.xpath('thead/tr//td[position()<last()]/text()').extract()
        trs = table.xpath('tbody//tr')
        keys = ('year', 'school_name', 'school_college', 'major_code', 'major_name',
                'plan', 'proposer', 'enrollment', 'acceptance_rate', 'push_avoid_unripe')
        for tr in trs:
            values = tr.xpath('.//td[position()<last()]').xpath('string(.)').extract()
            assert len(values) == len(keys)
            item = AcceptanceRateItem(zip(keys, values))
            yield item
        next_page_url = get_next_page_url(response)
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)


class SchoolSpider(scrapy.Spider):
    name = 'school'
    start_urls = (
        'http://juece.kuakao.com/index.php?m=yxk&c=school_search&a=sear_yx&page=1',
    )

    def parse(self, response):
        """
        @url http://juece.kuakao.com/index.php?m=yxk&c=school_search&a=sear_yx&page=1
        @returns requests 11 11
        """
        ul = response.xpath('/html/body/div[2]/div[1]/div[2]/div/div[2]/ul[@class="information_x"]')
        lis = ul.xpath('.//li')
        for li in lis:
            item = SchoolItem()
            left = li.xpath('./div[1]')
            item['logo'] = left.xpath('./a/img/@src').extract()[0]
            item['name'] = left.xpath('./a[2]/p/text()').extract()[0]
            right = li.xpath('./div[2]')
            values = right.xpath('./p[@class="information_R_Titlex"]//span[position()<=2]').xpath('string(.)').extract()
            region_and_type = [v.split('：', 1)[-1] for v in values]
            keys = ('region', 'type')
            assert len(region_and_type) == len(keys)
            item.update(zip(keys, region_and_type))
            request = scrapy.Request(
                urlparse.urljoin(response.url, left.xpath('./a/@href').extract()[0]),
                self.parse_extra_school_info
            )
            request.meta['item'] = item
            yield request
        next_page_url = get_next_page_url(response)
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_extra_school_info(self, response):
        school_item = response.meta['item']
        top_div = response.selector.xpath('/html/body/div[5]/div[2]/div[@class="shoolWords"]')
        attrs_div = top_div.xpath('./div[1]')
        attrs = attrs_div.xpath('./p//span/text()').extract()
        school_item['belong_to'] = attrs.pop()
        school_item['is_211'] = '211' in attrs
        school_item['is_985'] = '985' in attrs
        school_item['is_autonomous_accepting_line'] = '自划线' in attrs
        school_item['code'] = attrs_div.xpath('./p[2]/text()').extract()[0].split('：', 1)[-1]
        school_item['popularity'] = top_div.xpath('./div[2]/div[@class="fl popWords"]/text()').extract()[0]

        rank_ul = response.selector.xpath('/html/body/div[10]/div[1]/div/ul[@class="clearfix schoolRank"]')
        keys = (
            'overall_rank',
            'graduate_school_rank',
            'graduate_school_level',
            'academic_level_rank',
            'star_level',
            'school_level'
        )
        values = rank_ul.xpath('.//li/h4').xpath('string(.)').extract()
        assert len(values) == len(keys)
        school_item.update(zip(keys, values))
        # school_item['star_level'] = school_item['star_level'].count('★') or None
        enrollment_plan_ul = response.selector.xpath(
            '/html/body/div[10]/div[1]/div/div[2]/ul[@class="diagram clearfix"]'
        )
        master_div = enrollment_plan_ul.xpath('./li/div[@class="diagramPK diagramPK1"]')
        # 硕士研究生学术学位招生人数
        school_item['master_academic_degree_plan'] = master_div.xpath('./div/@data-dimension').extract()[0]
        # 硕士研究生专业学位招生人数
        school_item['master_professional_degree_plan'] = master_div.xpath('./div[2]/@data-dimension').extract()[0]
        phd_div = enrollment_plan_ul.xpath('./li[2]/div[@class="diagramPK diagramPK2"]')
        # 博士研究生学术学位招生人数
        school_item['phd_academic_degree_plan'] = phd_div.xpath('./div/@data-dimension').extract()[0]
        # 博士研究生专业学位招生人数
        school_item['phd_professional_degree_plan'] = phd_div.xpath('./div[2]/@data-dimension').extract()[0]
        yield school_item

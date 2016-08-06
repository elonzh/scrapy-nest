# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# todo: 使用 url_hash 过滤重复

class MajorItem(scrapy.Item):
    # 人气指数
    popularity = scrapy.Field()
    # 专业代码
    code = scrapy.Field()
    # 专业名称
    name = scrapy.Field()
    # 学科门类
    category = scrapy.Field()
    # 一级学科
    first_major = scrapy.Field()
    # 学位类型
    degree = scrapy.Field()
    # 外语类型
    # 数学类型


class SchoolMajorItem(scrapy.Item):
    # 专业代码
    major_code = scrapy.Field()
    # 学校代码
    school_code = scrapy.Field()
    # 招生年份
    year = scrapy.Field()
    # 学院名称
    college = scrapy.Field()

    # 研究方向
    research_direction = scrapy.Field()
    # 招生人数
    enrollment_plan = scrapy.Field()
    # 考试科目
    exam_course = scrapy.Field()
    # 参考书目
    reference = scrapy.Field()
    # 备注
    remarks = scrapy.Field()


class CommonItem(scrapy.Item):
    year = scrapy.Field()
    # 数据库中使用 school_major_id 代替下面四个字段
    school_name = scrapy.Field()
    school_college = scrapy.Field()
    major_code = scrapy.Field()
    major_name = scrapy.Field()


class RetrialAcceptingLineItem(CommonItem):
    tp = scrapy.Field()
    politics = scrapy.Field()
    foreign_language = scrapy.Field()
    third_course = scrapy.Field()
    fourth_course = scrapy.Field()


class AcceptanceRateItem(CommonItem):
    plan = scrapy.Field()
    proposer = scrapy.Field()
    enrollment = scrapy.Field()
    acceptance_rate = scrapy.Field()
    push_avoid_unripe = scrapy.Field()


class SchoolItem(scrapy.Item):
    logo = scrapy.Field()
    # 学校名称
    name = scrapy.Field()
    # 地区
    region = scrapy.Field()
    # 类型
    type = scrapy.Field()

    # 是否是211
    is_211 = scrapy.Field()
    # 是否是985
    is_985 = scrapy.Field()
    # 是否是自主划线
    is_autonomous_accepting_line = scrapy.Field()
    # 隶属于
    belong_to = scrapy.Field()
    # 学校代码
    code = scrapy.Field()
    # 人气指数
    popularity = scrapy.Field()

    # 综合实力排名
    overall_rank = scrapy.Field()
    # 研究生院综合实力排名
    graduate_school_rank = scrapy.Field()
    # 研究生院综合实力评级
    graduate_school_level = scrapy.Field()
    # 教师平均学术水平排名
    academic_level_rank = scrapy.Field()
    # 星级排名
    star_level = scrapy.Field()
    # 办学层次
    school_level = scrapy.Field()

    # 硕士研究生学术学位招生人数
    master_academic_degree_plan = scrapy.Field()
    # 硕士研究生专业学位招生人数
    master_professional_degree_plan = scrapy.Field()
    # 博士研究生学术学位招生人数
    phd_academic_degree_plan = scrapy.Field()
    # 博士研究生专业学位招生人数
    phd_professional_degree_plan = scrapy.Field()

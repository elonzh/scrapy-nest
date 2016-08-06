# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime, ForeignKey, VARCHAR, Table, SmallInteger, \
    PrimaryKeyConstraint, UniqueConstraint, CheckConstraint, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

SQLALCHEMY_DATABASE_URI = "postgresql://dbuser:postgres&sql@localhost/school_info"

Base = declarative_base()


class Major(Base):
    __tablename__ = 'major'
    # 人气指数
    popularity = Column(Integer())
    # 专业代码
    code = Column(String(), primary_key=True)
    # 专业名称
    name = Column(String())
    # 学科门类
    category = Column(String())
    # 一级学科
    first_major = Column(String())
    # 学位类型
    degree = Column(String())

    school_majors = relationship('SchoolMajor', backref='major', lazy='dynamic')
    update_at = Column(DateTime(), onupdate=datetime.now)

    def __repr__(self):
        return "<Major [%r]%r>" % (self.major_code, self.major_name)


class SchoolMajor(Base):
    __tablename__ = 'school_major'
    __table_args__ = (
        UniqueConstraint('major_code', 'school_code', 'year'),
    )
    id = Column(Integer(), primary_key=True)
    # 专业代码
    major_code = Column(String(), ForeignKey('major.code'))
    # 学校代码
    school_code = Column(String(), ForeignKey('school.code'))
    # 招生年份
    year = Column(String())
    # 学院名称
    college = Column(String())

    # 研究方向
    research_direction = Column(String())
    # 招生人数
    enrollment_plan = Column(String())
    # 考试科目
    exam_course = Column(String())
    # 参考书目
    reference = Column(String())
    # 备注
    remarks = Column(String())

    update_at = Column(DateTime(), onupdate=datetime.now)
    retrial_accepting_lines = relationship('RetrialAcceptingLine', backref='school_major', lazy='dynamic')
    acceptance_rates = relationship('AcceptanceRate', backref='school_major', lazy='dynamic')

    def __repr__(self):
        return "<SchoolMajor [%r]%r>" % (self.major_code, self.major_name)


class RetrialAcceptingLine(Base):
    __tablename__ = 'retrial_accepting_line'
    id = Column(Integer(), primary_key=True)
    school_major_id = Column(Integer(), ForeignKey('school_major.id'))

    year = Column(String())
    tp = Column(String())
    politics = Column(String())
    foreign_language = Column(String())
    third_course = Column(String())
    fourth_course = Column(String())

    update_at = Column(DateTime(), onupdate=datetime.now)


class AcceptanceRate(Base):
    __tablename__ = 'acceptance_rate'
    id = Column(Integer(), primary_key=True)
    school_major_id = Column(Integer(), ForeignKey('school_major.id'))

    year = Column(String())
    plan = Column(String())
    proposer = Column(String())
    enrollment = Column(String())
    acceptance_rate = Column(String())
    push_avoid_unripe = Column(String())

    update_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class School(Base):
    __tablename__ = 'school'
    logo = Column(String(), unique=True)
    # 学校名称
    name = Column(String())
    # 地区
    region = Column(String())
    # 类型
    type = Column(String())

    # 是否是211
    is_211 = Column(Boolean())
    # 是否是985
    is_985 = Column(Boolean())
    # 是否是自主划线
    is_autonomous_accepting_line = Column(Boolean())
    # 隶属于
    belong_to = Column(String())
    # 学校代码
    code = Column(String(), primary_key=True)
    # 人气指数
    popularity = Column(Integer())

    # 综合实力排名
    overall_rank = Column(Integer())
    # 研究生院综合实力排名
    graduate_school_rank = Column(Integer())
    # 研究生院综合实力评级
    graduate_school_level = Column(String())
    # 教师平均学术水平排名
    academic_level_rank = Column(Integer())
    # 星级排名
    star_level = Column(Integer())
    # 办学层次
    school_level = Column(String())

    # 硕士研究生学术学位招生人数
    master_academic_degree_plan = Column(Integer())
    # 硕士研究生专业学位招生人数
    master_professional_degree_plan = Column(Integer())
    # 博士研究生学术学位招生人数
    phd_academic_degree_plan = Column(Integer())
    # 博士研究生专业学位招生人数
    phd_professional_degree_plan = Column(Integer())

    update_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    school_majors = relationship('SchoolMajor', backref='school', lazy='dynamic')


engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True, pool_size=20, max_overflow=100)
DBSession = sessionmaker(bind=engine)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

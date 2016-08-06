#!flask/bin/python
# -*- coding: utf-8 -*-
__author__ = 'erliang'

from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime, ForeignKey, VARCHAR, Table, SmallInteger
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = "mysql://root:mysqladmin@localhost:3306/hfut_news?charset=utf8"

Base = declarative_base()
ROLE_USER = 0
ROLE_ADMIN = 1

type_followers = Table("type_followers", Base.metadata,
                       Column("user_id", Integer, ForeignKey("user.id")),
                       Column("type_id", Integer, ForeignKey("type.id"))
                       )


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)

    account = Column(String(32), index=True, nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    role = Column(SmallInteger, default=ROLE_USER)

    posts = relationship("Post", backref="author", lazy="dynamic")
    about_me = Column(String(140))
    last_seen = Column(DateTime)
    followed_types = relationship("Type",
                                  secondary=type_followers,
                                  # primaryjoin = (type_followers.c.user_id == id),
                                  # secondaryjoin = (type_followers.c.type_id == Type().id),
                                  backref=backref("followers", lazy="dynamic"),
                                  lazy="dynamic")

    def __repr__(self):
        return "<User %r>" % (self.nickname)


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String(32), nullable=False)
    body = Column(Text(), nullable=False)
    link = Column(String(180))
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey("user.id"))
    type_id = Column(Integer, ForeignKey("type.id"))

    def __repr__(self):
        return "<Post('%s','%s')>" % (self.title, self.timestamp)


class Type(Base):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(45), nullable=False, unique=True)
    posts = relationship("Post", backref="type", lazy="dynamic")

    def __repr__(self):
        return "<Type %r>" % (self.name)


engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True, pool_size=20, max_overflow=100)
DBSession = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

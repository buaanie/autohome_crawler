# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AutohomeClubItem(Item):
    elite = Field() #是否是精华帖
    reply = Field() #围观回复数
    title = Field() #帖子标题
    link = Field() #帖子链接，主要用于还原车型ID与帖子ID
    uname = Field() #用户昵称
    content = Field() #帖子内容
    date = Field() #发布时间
    uid = Field() #用户ID
    ulevel = Field() #用户等级
    utime = Field() #用户注册时间
    ubbs = Field() #用户帖子数(精华/发帖/回帖)
    uloc = Field() #用户地区
    floor = Field() #楼层数


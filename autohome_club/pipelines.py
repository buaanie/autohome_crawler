# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

# s = 'http://club.autohome.com.cn/bbs/forum-c-3298-2.html?qaType=-1#pvareaid=101061'
# print s.split('-')[-1].split('\.')[0]

class AutohomeClubPipeline(object):
    def __init__(self):
        self.count = 0
        self.file = codecs.open('bbs-1.txt', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        if item != {} and item['content'].strip() != "":
            item['content']=item['content'].replace("\n","")
            line = json.dumps(dict(item)) + '\n'
            self.file.write(line.decode("unicode_escape"))
            self.count = self.count + 1
            if(self.count % 100 == 0):
                print self.count
        pass

    def close_spider(self,spider):
        self.file.close()

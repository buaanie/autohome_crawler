#!/usr/bin/env python
# encoding: utf-8
"""
@author: chenchuan@autohome.com.cn
@time: 2017/03/13
"""
import traceback

from scrapy.spiders import Spider
from scrapy.selector import Selector
import sys
from time import sleep
from scrapy.http import Request
from autohome_club.items import AutohomeClubItem
from autohome_club.spiders.cssspider import get_bbs_main_floor

default_encoding = 'utf-8'
domain = 'http://club.autohome.com.cn'
domain_bbs = 'http://club.autohome.com.cn/bbs/'

if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class AutohomeSpider(Spider):
    name = "HFH9"
    allowed_domains = ["autohome.com.cn"]

    start_urls = [
        # "http://club.autohome.com.cn/bbs/forum-c-3298-1.html?type=101"
        # "http://club.autohome.com.cn/bbs/forum-c-3298-1.html"
        "http://club.autohome.com.cn/bbs/forum-c-526-2.html?orderby=dateline&qaType=-1"
    ]

    def completeUrl(self, _url):
        if not _url.startswith('http', 0, 4):
            _url = domain + _url
        _url = _url.replace('threadqa','thread').replace('?qaType=-1#pvareaid=101061','')
        return _url

    def completeBBSUrl(self, _url):
        if not _url.startswith('/bbs', 0, 4):
            _url = domain_bbs + _url
        _url = _url.replace('threadqa','thread')
        return _url

    def getLevel(self,_levelurl):
        _level  = _levelurl.split('_')[1]
        return _level

    def getUid(self,_userlink):
        _uid = _userlink.split('/')[3]
        return _uid
    def getArtID(self,_link):
        _artid = _link.split('-')[2]+'-'+_link.split('-')[3]
        return _artid

    # 车系帖子列表页
    def parse(self, response):
        hxs = Selector(response)
        urls = hxs.xpath('//div[@id="subcontent"]//a[@class="a_topic"]/@href')
        for url in urls:
            _url = self.completeUrl(url.extract())
            print _url
            yield Request(_url, callback=self.parse_item)
        # 车系列表页分页，注意单篇帖子分页要到帖子也去完成
        page = hxs.xpath('//div[@class="pages"]//a[@class="afpage"]/@href')
        if page:
            next_page = self.completeUrl(page.extract()[0])
            print next_page, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<----- ',int(next_page.split('-')[3].split('.')[0])
            if int(next_page.split('-')[3].split('.')[0]) < 10: #爬取前十页
                yield Request(next_page, callback=self.parse)

    # 车系列表页 -> 帖子详情页面
    def parse_item(self, response):
        all =  response.body.decode('gbk').encode('utf-8')
        items = []
        link = response.url

        hxs = Selector(response)
        title = hxs.xpath('//title/text()').extract()
        title = title[0].decode(default_encoding)

        contents = hxs.xpath('//div[@class= "clearfix contstxt outer-section"]')
        for n,con in enumerate(contents):
            page = int(str(link).split('-')[4].split('.')[0])
            if page==1:
                m = n
            else:
                m = page*10+n+1
            print str(link).split('-')[3],m
            item = AutohomeClubItem()
            try:
                if(m==0):
                    _text = get_bbs_main_floor(all)
                    _text = _text.replace('\\','/').replace('\n','')
                    reply = hxs.xpath('//*[@id="consnav"]/span[1]')[0].xpath('string(.)').extract()[0].strip()
                    reply = reply.decode(default_encoding)
                    _elite = con.xpath('./span[@id="seal"]').extract()
                    if not 0==len(_elite):
                        item['elite'] = 'jing'
                    item['reply'] = reply
                    item['title'] = title
                else:
                    _text = self.getContext(con)
                if("\"" in _text):
                    _text = _text.replace("\""," ")
                _user_name = con.xpath('.//a[@xname="uname"]/text()').extract()[0]
                _user_name.decode(default_encoding)
                _userid= self.getUid(con.xpath('.//a[@xname="uname"]/@href').extract()[0])
                if str(_userid) == '21233556':
                    return
                _level = self.getLevel(con.xpath('.//div[@class="lv_card"]//img/@src').extract()[0])
                _user_time = con.xpath('.//ul[@class="leftlist"]/li[5]/text()').extract()[0].strip()
                _user_bbs = con.xpath('.//ul[@class="leftlist"]/li[3]')[0].xpath('string(.)').extract()[0].strip()+' | '+con.xpath('.//ul[@class="leftlist"]/li[4]')[0].xpath('string(.)').extract()[0].strip()
                _user_loc = con.xpath('.//ul[@class="leftlist"]/li[6]')[0].xpath('string(.)').extract()[0].strip()

                _date = con.xpath('.//span[@xname="date"]/text()').extract()[0]

                item['link'] = self.getArtID(link)
                item['uid']= _userid
                item['ulevel']= _level
                item['utime']=_user_time
                item['ubbs']=_user_bbs
                item['uloc']=_user_loc
                item['uname'] = _user_name
                item['content'] = _text
                item['date'] = _date
                item['floor'] = m
                items.append(item)
            except :
                print traceback.print_exc() ,": ",link,m
            yield item

        #帖子页分页
        sleep(2)
        page = hxs.xpath('//div[@class="pages"]//a[@class="afpage"]/@href')
        if page:
            next_page = self.completeBBSUrl(page.extract()[0])
            if int(next_page.split('-')[-1].split('.')[0]) < 4:  # 爬取前十页
                print '-------->>>>>>>>>>>>>>>>>>>>>>',next_page
                yield Request(next_page, callback=self.parse_item)


    def getContext(self, con):
        if 0 != len(con.xpath('.//div[@class="w740"]//div[@class="yy_reply_cont"]').extract()):
            _text = con.xpath('.//div[@class="w740"]//div[@class="yy_reply_cont"]')[0].xpath('string(.)').extract()
            if(len(_text)>0):
                _text=_text[0]
            elif 0 != len(con.xpath('.//div[@class="w740"]//img/@src').extract()):
                _text = con.xpath('.//div[@class="w740"]//img/@src').extract()[0]
            elif 0 != len(con.xpath('.//div[@class="w740"]/div').extract()):
                _text = con.xpath('.//div[@class="w740"]')[0].xpath('string(.)').extract()[0].strip()
            else:
                _text=''
        elif 0 == len(con.xpath('.//div[@class="w740"]/child::p').extract()):
            if( 0 ==  len(con.xpath('.//div[@class="w740"]').extract())):
                _text = '本楼已被管理员删除'
            elif 0 != len(con.xpath('.//div[@class="w740"]//img/@src').extract()):
                _text = con.xpath('.//div[@class="w740"]//img/@src').extract()[0]
            elif 0 != len(con.xpath('.//div[@class="w740"]/div').extract()):
                _text = con.xpath('.//div[@class="w740"]')[0].xpath('string(.)').extract()[0].strip()
            else:
                _text = con.xpath('.//div[@class="w740"]/text()').extract()
                if(len(_text)!=0):
                    _text=_text[0]
                else:
                    _text=''
        else:
            _text = con.xpath('.//div[@class="w740"]/child::p/text()').extract()
            if 0 != len(_text):
                _text=con.xpath('.//div[@class="w740"]')[0].xpath('string(.)').extract()[0].strip()
            else:
                _text = '本楼已被管理员删除'
        _text.decode(default_encoding)
        return _text.replace('\n','')

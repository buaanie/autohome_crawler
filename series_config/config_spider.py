#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by ACT-NJ on 2017/5/19.
from urllib2 import urlopen
import time,sys,os,json

reload(sys)
sys.setdefaultencoding('utf-8')

urls = set()
filepath=('murl.txt')
with open(filepath,"r") as filer:
	string = filer.readline()
	filer.close()
urlsu = string.split(',')
for u in urlsu:
	urls.add(u)
# filer.close
print len(urls)

path=os.getcwd()
path=os.path.join(path,'config')

for id in urls:
	filepath = os.path.join(path, id + '.json')
	url = 'http://car.m.autohome.com.cn/ashx/car/GetModelConfigNew.ashx?seriesId='+id
	try:
		html = urlopen(url).read().decode('utf-8', 'ignore')
		with open(filepath, 'w') as txt_file:
			txt_file.write(html)
			txt_file.close()
		time.sleep(1)
	except Exception,e:
		print id+"----------^^ ",e

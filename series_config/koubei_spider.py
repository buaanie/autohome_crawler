#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by ACT-NJ on 2017/5/14.
import urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup
import time,os,sys,re

reload(sys)
sys.setdefaultencoding('utf-8')
# head0= {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}
# head1= {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36'}
urls=[]
prefix = 'http://k.autohome.com.cn/'
filepathw = os.getcwd()
filepathw = os.path.join(filepathw, 'kb')
replace_reg = re.compile('<[^>]+>[\s\S]*?<[^>]+>')
# filepathr=('murl.txt')
# with open(filepathr,"r") as filer:
# 	string = filer.readline()
# 	urls = string.split(',')
# filer.close
# print len(urls)
urls.append("3038")
for id in urls:
	url = prefix+id+'/'
	for i in range(1,12):
		filepathw2 = os.path.join(filepathw, id + '-' + str(i) + '.txt')
		if i==9:
			continue
		url2 = url+"ge"+str(i)
		print url2
		try:
			req = urllib2.Request(url2)#None, head1
			page = urllib2.urlopen(req).read()  # 进入口碑详情页面
			# page = urlopen(url3).read()  # 进入口碑详情页面
			page_gbk = page.decode('gbk', 'ignore')
			bsObj = BeautifulSoup(page_gbk, 'html.parser')

			if len(bsObj.select('div.revision-impress')) == 0:
				break
			if "impress-small" in bsObj.select('div.revision-impress')[-1]['class']:
				if bsObj.select('span.page-item-info'):
					page_num = bsObj.select('span.page-item-info')[0].contents[0][1:-1]
				else:
					page_num = 1
				seriesid = url2.split('/')[3]
				for j in range(1, int(page_num) + 1):#http://k.autohome.com.cn/4247/ge8/#dataList
					if '#' in url2:
						kbits = url2.split('#')[0]+'index_'+str(j)+'.html?'+url2.split("#")[1]
					else:
						kbits = url2+'/'+'index_'+str(j)+'.html'
					print kbits
					bsObj = BeautifulSoup(urlopen(kbits).read().decode('gbk', 'ignore'), 'html.parser')  # 分析单独每一项
					time.sleep(1)
					text_c = bsObj.find_all('div', class_='text-con')
					with open(filepathw2, 'a') as txt_file:
						for k in range(len(text_c)):
							cont = "#" + str(seriesid) + "@" + '-' + "@" + '-' + "@" + '-' + "@"
							for child in text_c[k].descendants:
								cont = cont + re.sub('\s', '', str(child)).replace('查看完整口碑', '')
							txt_file.write(cont + '\n')
					txt_file.close()
			else:
				for car in bsObj.select('div.revision-impress')[-1].select('a'):
					if "java" in car['href']:
						continue
					seriesid = car['href'].split("/")[1] #车的系列型号，另外i表示具体的口碑项 1-9表示外观到性价比
					summaryid = car['href'].split("=")[1].split("&")[0] #评价的key id
					summarykey = str(car.contents[0])#评价的key
					kbit = 'http://k.autohome.com.cn' + car['href']
					judge = 'pos' #评价的正负面
					if "dust" in car['class']:
						judge = 'neg'
					req = urllib2.Request(kbit)
					bsObj = BeautifulSoup(urllib2.urlopen(req).read().decode('gbk', 'ignore'), 'html.parser')  # 分析单独每一项
					# bsObj = BeautifulSoup(urlopen(kbit).read().decode('utf-8', 'ignore'), 'html.parser')#分析单独每一项
					if bsObj.select('span.page-item-info'):
						page_num = bsObj.select('span.page-item-info')[0].contents[0][1:-1]
					else:
						page_num =1
					for j in range(1, int(page_num)+1):
						kbits = kbit.split("?")[0]+'index_'+str(j)+'.html?'+kbit.split("?")[1]
						print kbits
						bsObj = BeautifulSoup(urlopen(kbits).read().decode('gbk', 'ignore'), 'html.parser')  # 分析单独每一项
						time.sleep(1)
						text_c = bsObj.find_all('div',class_='text-con')
						with open(filepathw2, 'a') as txt_file:
							for k in range(len(text_c)):
								cont = "#"+str(seriesid)+"@"+str(summaryid)+"@"+str(summarykey)+"@"+judge+"@"
								for child in text_c[k].descendants:
									cont = cont+re.sub('\s','',str(child)).replace('查看完整口碑','')
								txt_file.write(cont+'\n')
						txt_file.close()
			time.sleep(1)
		except Exception, e:
			print e,"*******************", url2
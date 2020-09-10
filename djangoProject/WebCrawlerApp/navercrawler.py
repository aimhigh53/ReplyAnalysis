import json
import sys
import os
import time
import requests


from bs4 import BeautifulSoup
# from .models import search

from django.views import View
from django.http import HttpResponse,JsonResponse
from django_pandas.io import read_frame
from django.forms.models import model_to_dict
from django.shortcuts import render

import pandas as pd

import pandas_csv
import numpy as np

from WebCrawlerApp.chromedriver import generate_chrome
from datetime import datetime, timedelta


PROJECT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = f'{PROJECT_DIR}/src'
driver_path = f'{PROJECT_DIR}/lib/webDriver/'
platform = sys.platform


if platform == 'darwin':
    print('System platform : Darwin')
    driver_path += 'chromedriver'
elif platform == 'linux':
    print('System platform : Linux')
    driver_path += 'chromedriverLinux'
elif platform == 'win32':
    print('System platform : Window')
    driver_path += 'chromedriverWindow'
else:
    print(f'[{sys.platform}] not supported. Check your system platform.')
    raise Exception()

# 크롬 드라이버 인스턴스 생성
chrome = generate_chrome(
    driver_path=driver_path,
    headless=False,
    download_path=DOWNLOAD_DIR)


# 페이지 요청
url = 'https://news.naver.com/main/ranking/popularDay.nhn'
chrome.get(url)
time.sleep(3)

html = chrome.page_source
soup = BeautifulSoup(html, 'lxml')

def loadPage():
    html = chrome.page_source
    soup = BeautifulSoup(html, 'lxml')

def backToMainPage():
    chrome.get(url)


def getTopFive(i):
    loadPage()
    elements=soup.select('#wrap > table > tbody > tr > td.content > div > div:nth-child('+str(i)+') > ol> li')
    titlelist=[]

    cnt=0
    for element in elements:

        title = element.select_one('dl > dt > a').text

        if element.select_one('dl > dd > span.lede'):
            title=title+element.select_one('dl > dd > span.lede').text

        titlelist.append(title)

    return titlelist


#top5 댓글 가져오기

def getReply(i,j):
    replylist=[]
    collecttime = str(datetime.utcnow().replace(microsecond=0) + timedelta(hours=9))[:16]

    clicknews=chrome.find_element_by_xpath('//*[@id="wrap"]/table/tbody/tr/td[2]/div/div['+str(i)+']/ol/li['+str(j)+']/dl/dt/a')
    clicknews.click()
    time.sleep(1)

    loadPage()

    identify=chrome.find_element_by_xpath('//*[@id="cbox_module"]/div/div[6]/div[1]/div/ul/li[1]')
    identify.click()
    time.sleep(1)

    more = chrome.find_element_by_xpath('//*[@id="cbox_module"]/div/div[9]/a/span[1]')
    more.click()
    time.sleep(1)

    contents = chrome.find_elements_by_css_selector('span.u_cbox_contents')
    likes = chrome.find_elements_by_css_selector('em.u_cbox_cnt_recomm')
    hates = chrome.find_elements_by_css_selector('em.u_cbox_cnt_unrecomm')
    cnt = 0

    for content,like,hate in zip(contents,likes,hates):
        cnt += 1
        print('[', cnt, ']번째')
        print(content.text,like.text,hate.text)
        replylist.append([cnt,collecttime,content.text,like.text,hate.text])
    backToMainPage()
    return replylist

    # for reply in replys:
    #     replycontent = reply
    #     print(replycontent)

    time.sleep(2)



#return list
# print(getTopFive(5))

#   replylist.append(['[', cnt, ']번째',collecttime,content.text,like.text,hate.text]) list반환
# print(getReply(5,1))

# df = pd.DataFrame({'Title': ['None'], 'ReplyIdx': ['None'],'CrawlingTime':['None'],'Content':['None'],'like':['None'],'hate':['None']})
df=pd.DataFrame(np.array([[None,None,None,None,None,None]]),columns=['Title','ReplyIndex','CrawlingTime','Content','Like','Hate'])
s=0
for i in range(5,10):
    titlelist=getTopFive(i)
    print(titlelist)
    for j in range(1,6):
        replylist=getReply(i,j)
        sorted(replylist,key=lambda replylist:replylist[0])
        title=titlelist[j-1]


        for replyone in replylist:
            addrow=[str(title),str(replyone[0]),str(replyone[1]),str(replyone[2]),str(replyone[3]),str(replyone[4])]
            df.loc[s] = addrow
            s+=1


df.to_csv("/Users/ins25k/Desktop/pycharm/djangoProject/WebCrawlerApp/Data/NaverReplyList.csv", mode='a', header=False,encoding='utf-8')









# for i in range(5,10):
#     titledic = getTopFive(i)
#     replylist=[]
#     Data=df(data={'title':['null'],'reply':['null']})
#     for j in range(1,6):
#         replylist.append(getReply(i,j))
#         backToMainPage()
#         for title, replys in zip(titledic.values(), replylist):
#             s=0
#             for k in replys:
#                 Data.loc[s]=title+str(k)
#                 s+=1
#         print(Data)
#
        #dataframe을 만든 뒤 csv파일에 넣음
        #df를 먼저짜봐야,,,
        # for index,title,replys in zip(titledic,titledic.values(),replylist):


    # to_es.to_elastic(insertdata)

    #5개 top section, 5개 기사의 리플 가져오기










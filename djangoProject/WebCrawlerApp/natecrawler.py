import json
import sys
import os
import time
import requests
from datetime import date

from bs4 import BeautifulSoup
# from .models import search

from django.views import View
from django.http import HttpResponse,JsonResponse
from django_pandas.io import read_frame
from django.forms.models import model_to_dict
from django.shortcuts import render

import pandas as pd
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

daydate=str(datetime.today().strftime('%Y-%m-%d').replace("-",""))

# 페이지 요청
url = 'https://news.nate.com/rank/interest?sc=sisa&p=day&date='+daydate
print(url)
chrome.get(url)
time.sleep(3)

html = chrome.page_source
soup = BeautifulSoup(html, 'lxml')

def loadPage():
    html = chrome.page_source
    soup = BeautifulSoup(html, 'lxml')

def backToMainPage():
    chrome.get(url)

def getTtile(i):
    loadPage()

    title=soup.select_one('#newsContents > div > div.postRankSubjectList.f_clear '
                          '> div:nth-child('+str(i)+') > div > a > span.tb > strong').text

    return title


#top3 댓글 가져오기

def getReply(i):
    replylist=[]
    collecttime = str(datetime.utcnow().replace(microsecond=0) + timedelta(hours=9))[:16]

    clicknews=chrome.find_element_by_xpath('//*[@id="newsContents"]/div/div[2]/div['+str(i)+']/div/a/span[2]/strong')
    clicknews.click()
    time.sleep(1)

    loadPage()

    ###여기가안된
    contents = soup.select('#best_cmtcontent_215014350')
    likes = soup.select('')
    hates = chrome.find_elements_by_css_selector('strong#cmt_x_cnt_214818821')
    ###다

    cnt = 0
    print(contents,likes,hates)
    time.sleep(1)


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

titlelist=[]
s=0
for i in range(1,6):
    title=getTtile(i)
    replylist=getReply(i)
    sorted(replylist, key=lambda replylist: replylist[0])
    print(title,replylist)
    for replyone in replylist:
        addrow=[str(title),str(replyone[0]),str(replyone[1]),str(replyone[2]),str(replyone[3]),str(replyone[4])]
        df.loc[s] = addrow
        print(df)
        s+=1

#     for j in range(1,6):
#         replylist=getReply(i,j)
#         sorted(replylist,key=lambda replylist:replylist[0])
#         title=titlelist[j-1]
#
#
#         for replyone in replylist:
#             addrow=[str(title),str(replyone[0]),str(replyone[1]),str(replyone[2]),str(replyone[3]),str(replyone[4])]
#             df.loc[s] = addrow
#             s+=1
#
#
# df.to_csv("/Users/ins25k/Desktop/pycharm/djangoProject/WebCrawlerApp/Data/NaverReplyList.csv", mode='a', header=False,encoding='utf-8')







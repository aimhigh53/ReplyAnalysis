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
from selenium.common.exceptions import NoSuchElementException

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


# 페이지 요청
url = 'https://news.daum.net/ranking/popular/news'
chrome.get(url)
time.sleep(3)

html = chrome.page_source
soup = BeautifulSoup(html, 'lxml')
collecttime = str(datetime.utcnow().replace(microsecond=0) + timedelta(hours=9))[:16]

def loadPage():
    html = chrome.page_source
    soup = BeautifulSoup(html, 'lxml')

def backToMainPage():
    chrome.get(url)


def getTitle(i):
    # mArticle > div.rank_news > ul.list_news2 > li:nth-child(1) > div.cont_thumb > strong > a
    # mArticle > div.rank_news > ul.list_news2 > li:nth-child(2) > div.cont_thumb > strong > a
    title=soup.select_one('#mArticle > div.rank_news > ul.list_news2 > li:nth-child('+str(i)+') > div.cont_thumb > strong > a').text

    return title



#top5 댓글 가져오기

def getReply(i):
    replylist=[]

    clicknews=chrome.find_element_by_xpath('// *[ @ id = "mArticle"] / div[2] / ul[3] / li['+str(i)+'] / div[2] / strong / a')
    clicknews.click()
    time.sleep(1)

    loadPage()




    descsort=chrome.find_element_by_xpath('//*[@id="alex-area"]/div/div/div/div[3]/ul[1]/li[2]/button/span/span')
    descsort.click()
    time.sleep(1)

    more = chrome.find_element_by_xpath('//*[@id="alex-area"]/div/div/div/div[3]/div[2]/button')
    more.click()
    time.sleep(1)
    # // *[ @ id = "alex-area"] / div / div / div / div[3] / div[2] / button
    loadPage()

    try:
        more = chrome.find_element_by_xpath('//*[@id="alex-area"]/div/div/div/div[3]/div[2]/button')
        more.click()
    except NoSuchElementException:
        print("No Found")

    time.sleep(1)



    cnt=1
    for reply in range(1,21):
        try:
            cnt += 1

            content=chrome.find_element_by_xpath('/ html / body / div[2] / div[3] / div[2] / div[1] / div[2] / div[6] / div / div / div / div / div[3] / ul[2] / li['+str(reply)+'] / div /p')
            Like=chrome.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[6]/div/div/div/div/div[3]/ul[2]/li['+str(reply)+']/div/div/span[2]/button[1]/span[2]')
            Hate=chrome.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[6]/div/div/div/div/div[3]/ul[2]/li['+str(reply)+']/div/div/span[2]/button[2]/span[2]')

            replylist.append([cnt,collecttime,content.text,Like.text,Hate.text])
        except NoSuchElementException:
            print("No Data")

    # for content,like,hate in zip(contents,likes,hates):
    #     cnt += 1
    #     print('[', cnt, ']번째')
    #     print(content.text,like.text,hate.text)
    #     replylist.append([cnt,collecttime,content.text,like.text,hate.text])
    backToMainPage()
    return replylist


    time.sleep(2)


s=0
df=pd.DataFrame(np.array([[None,None,None,None,None,None]]),columns=['Title','ReplyIndex','CrawlingTime','Content','Like','Hate'])


for i in range(1,51):

    title=getTitle(i)
    replylist=getReply(i)
    for replyone in replylist:
        addrow=[str(title),str(replyone[0]),str(replyone[1]),str(replyone[2]),str(replyone[3]),str(replyone[4])]
        df.loc[s] = addrow
        s+=1
    ##연예란 예외처리해야함!

    print(df)

df.to_csv("/Users/ins25k/Desktop/pycharm/djangoProject/WebCrawlerApp/Data/DaumReplyList"+collecttime+".csv", mode='a', header=['Title','ReplyIndex','CrawlingTime','Content','Like','Hate'],encoding='utf-8-sig')


# s=0
# for i in range(1,51):
#     titlelist=getTitle(i)
#     print(titlelist)
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


#df.to_csv("/Users/ins25k/Desktop/pycharm/djangoProject/WebCrawlerApp/Data/NaverReplyList"+collecttime+".csv", mode='a', header=['Title','ReplyIndex','CrawlingTime','Content','Like','Hate'],encoding='utf-8-sig')





